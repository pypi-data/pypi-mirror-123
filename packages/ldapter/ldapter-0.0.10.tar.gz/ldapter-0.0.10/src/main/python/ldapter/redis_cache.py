import json
from typing import Callable, List, Optional, Tuple

import redis

from .cache import CacheListener
from .directory import DirectoryCache, Scope, DistinguishedName


class RedisDirectoryCache(DirectoryCache):

    NEGATIVE_RESULT = {"NONE"}
    SEARCH_KEY = "s:{base}:{scope}:{search_filter}"
    ENTRY_KEY = "e:{dn}"

    def __init__(self, host="localhost", port=6379, db=0,
                 search_ttl = 900,
                 entry_ttl: dict = None,
                 entry_classifier: Callable[[dict], str] = lambda entry: entry["objectClass"][0],
                 cache_listener: CacheListener = CacheListener()):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.search_ttl = search_ttl
        self.entry_ttl = entry_ttl
        self.entry_classifier = entry_classifier
        self.cache_listener = cache_listener

    def _get_entry_ttl(self, entry):
        if self.entry_ttl is not None:
            classifier = self.entry_classifier(entry)
            return self.entry_ttl[classifier] if classifier in self.entry_ttl else self.search_ttl
        return self.search_ttl

    def _stringify(self, entry):
        return {k: json.dumps(v) for k, v in entry.items()}

    def _destringify(self, entry):
        return {k: json.loads(v) for k, v in entry.items()}

    def get_entry(self, dn: DistinguishedName) -> Tuple[DistinguishedName, dict]:
        key = self.ENTRY_KEY.format(dn=str(dn))
        pairs = self._redis.hgetall(key)
        if len(pairs) > 0:
            entry = self._destringify({k: v for k, v in pairs.items()})
            self.cache_listener.on_entry_hit(dn, entry)
            return dn, entry

        self.cache_listener.on_entry_miss(dn)

    def get_search(self, base: DistinguishedName, scope: Scope, search_filter: str) \
            -> Optional[List[Tuple[DistinguishedName, dict]]]:
        k = self.SEARCH_KEY.format(base=str(base), scope=scope.name, search_filter=search_filter)
        dns = self._redis.smembers(k)
        if dns != self.NEGATIVE_RESULT:
            dns = [DistinguishedName(dn) for dn in dns]

        if len(dns) == 0:
            self.cache_listener.on_search_miss(base, scope, search_filter)
            return None

        if dns == self.NEGATIVE_RESULT:
            dns = []

        self.cache_listener.on_search_hit(base, scope, search_filter, dns)

        entries = []
        for dn in dns:
            pair = self.get_entry(dn)
            if pair is not None:
                entries.append(pair)
            else:
                entries.append((dn, None))

        return entries

    def put_entry(self, dn: DistinguishedName, entry):
        k = self.ENTRY_KEY.format(dn=str(dn))
        self._redis.hset(k, mapping=self._stringify(entry))
        entry_ttl = self._get_entry_ttl(entry)
        self._redis.expire(k, entry_ttl)

        self.cache_listener.on_entry_fill(dn, entry, entry_ttl)

    def put_search(self, base: DistinguishedName, scope: Scope, search_filter: str,
                   entries: List[Tuple[DistinguishedName, dict]]):
        search_ttl = self.search_ttl
        with self._redis.pipeline() as pipe:
            dns = []
            for dn, entry in entries:
                self.put_entry(dn, entry)
                dns.append(dn)

            self.cache_listener.on_search_fill(base, scope, search_filter, dns, search_ttl)

            if len(dns) == 0:
                dns = self.NEGATIVE_RESULT

            k = self.SEARCH_KEY.format(base=str(base), scope=scope.name, search_filter=search_filter)
            self._redis.sadd(k, *[str(dn) for dn in dns])
            self._redis.expire(k, search_ttl)
            pipe.execute()


    def clear(self):
        object_keys = self._redis.keys(self.ENTRY_KEY.format(dn="*"))
        if len(object_keys) > 0:
            self._redis.delete(*object_keys)

        search_keys = self._redis.keys(self.SEARCH_KEY.format(base="*", scope="*", search_filter="*"))
        if len(search_keys) > 0:
            self._redis.delete(*search_keys)
