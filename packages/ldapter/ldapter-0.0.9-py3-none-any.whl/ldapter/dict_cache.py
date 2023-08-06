from typing import List, Tuple, Optional
from .cache import DirectoryCache, CacheListener
from .directory import DistinguishedName, Scope


class DictDirectoryCache(DirectoryCache):

    def __init__(self, cache_listener: CacheListener = CacheListener()):
        self._entries = {}
        self._searches = {}
        self.cache_listener = cache_listener

    def get_entry(self, dn: DistinguishedName) -> Tuple[DistinguishedName, dict]:
        if dn in self._entries:
            entry = self._entries[dn]
            self.cache_listener.on_entry_hit(dn, entry)
            return dn, entry

        self.cache_listener.on_entry_miss(dn)

    def get_search(self, base: DistinguishedName, scope: Scope, search_filter: str) \
            -> Optional[List[Tuple[DistinguishedName, dict]]]:
        key = (base, scope, search_filter)
        if key in self._searches:
            dns = self._searches[key]
            self.cache_listener.on_search_hit(base, scope, search_filter, dns)
            return [(dn, self._entries[dn]) for dn in dns]

        self.cache_listener.on_search_miss(base, scope, search_filter)

    def put_entry(self, dn: DistinguishedName, entry: dict):
        self._entries[dn] = entry
        self.cache_listener.on_entry_fill(dn, entry, None)

    def put_search(self, base: DistinguishedName, scope: Scope, search_filter: str,
                   entries: List[Tuple[DistinguishedName, dict]]):
        dns = []
        for dn, entry in entries:
            self.put_entry(dn, entry)
            dns.append(dn)
        self._searches[(base, scope, search_filter)] = dns
        self.cache_listener.on_search_fill(base, scope, search_filter, dns, None)

    def clear(self):
        self._entries = {}
        self._searches = {}
