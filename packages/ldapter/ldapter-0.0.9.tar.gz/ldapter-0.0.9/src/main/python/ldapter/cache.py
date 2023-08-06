from abc import ABC
from typing import Tuple, List

from .schema import DistinguishedName
from .scope import Scope


class DirectoryCache(ABC):

    def get_entry(self, dn: DistinguishedName) -> Tuple[DistinguishedName, dict]:
        pass

    def get_search(self, base: DistinguishedName, scope: Scope, search_filter: str) \
            -> List[Tuple[DistinguishedName, dict]]:
        pass

    def put_entry(self, dn: DistinguishedName, entry: dict):
        pass

    def put_search(self, base: DistinguishedName, scope: Scope, search_filter: str,
                   objs: List[Tuple[DistinguishedName, dict]]):
        pass


class CacheListener(ABC):

    def on_entry_fill(self, dn, entry, ttl):
        pass

    def on_entry_hit(self, dn, entry):
        pass

    def on_entry_miss(self, dn):
        pass

    def on_search_fill(self, base, scope, search_filter, dns, ttl):
        pass

    def on_search_hit(self, base, scope, search_filter, dns):
        pass

    def on_search_miss(self, base, scope, search_filter):
        pass
