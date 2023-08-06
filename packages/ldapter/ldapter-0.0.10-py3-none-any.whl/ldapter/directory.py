import logging
import os
from typing import List, Optional, Union, Tuple

from .cache import DirectoryCache
from .ldap_provider import LdapProvider
from .openldap_provider import OpenLdapProvider
from .schema import Schema, ObjectClass, DistinguishedName

from .scope import Scope

logger = logging.getLogger(__name__)


class DirectoryError(BaseException):
    pass


class TooManyResultsError(DirectoryError):
    pass


class Entry:

    def __init__(self, object_class: ObjectClass, attrs: dict):
        self._object_class = object_class
        self._attrs = attrs

    def __len__(self):
        return len(self._attrs)

    def __contains__(self, attr_name):
        return attr_name in self._attrs

    def __getitem__(self, attr_name):
        if attr_name not in self._attrs:
            raise KeyError(f"no {attr_name} in entry")
        if attr_name not in self._object_class:
            raise KeyError(f"attribute `{attr_name}` not defined for object type `{self._object_class.name}`")
        attr_type = self._object_class[attr_name]
        return attr_type.transform(self._attrs[attr_name])

    def __repr__(self):
        return f"Entry(obj_type={self._object_class.name}, attrs={self._attrs}"

    def keys(self):
        return self._attrs.keys()

    def items(self):
        return [(k, self[k]) for k in self._attrs.keys()]

    def attrs(self):
        return self._attrs

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False
        return self._object_class == other._object_class and self._attrs == other._attrs

    def __hash__(self):
        return 19*hash(self._object_class) + hash(self._attrs)


class Directory:
    def __init__(self,
                 schema: Schema,
                 uri: str = os.environ.get("LDAPURI"),
                 provider: LdapProvider = None,
                 cache: DirectoryCache = None,
                 start_tls: bool = True, simple_bind: bool = False,
                 bind_dn: Union[str, DistinguishedName] = None, bind_password: str = None):
        if uri is None:
            raise ValueError("URI is required")
        self.uri = uri
        self.schema = schema
        self.start_tls = start_tls
        self.simple_bind = simple_bind
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.cache = cache
        self.provider = provider if provider is not None else OpenLdapProvider()

    def connect(self):
        if not self.provider.is_connected():
            self.provider.connect(self.uri)
            if self.start_tls:
                self.provider.start_tls()
            if self.simple_bind:
                self.provider.bind_simple(self.bind_dn, self.bind_password)
            else:
                self.provider.bind_sasl_external()

    def _decode(self, dn, entry):
        decoded = {}
        for k, v in entry.items():
            decoded[k] = [e.decode("UTF-8") for e in v]
        return DistinguishedName(dn), decoded

    def _to_entry(self, dn: DistinguishedName, attrs: dict):
        obj_class_name = attrs["objectClass"][0]
        obj_type = self.schema.object_classes[obj_class_name]
        return dn, Entry(obj_type, attrs)

    def _refetch(self, dn, attrs):
        if attrs is None:
            logger.debug("refetch: %s", dn)
            results = self.provider.search(dn, Scope.BASE)
            results = [self._decode(*r) for r in results]
            if len(results) == 0:
                raise KeyError(f"refetch {dn} produced no result")
            attrs = results[0][1]
            self.cache.put_entry(dn, attrs)

        return dn, attrs

    def _fetch(self, base: Union[str, DistinguishedName], scope: Scope, search_filter, max_entries) \
            -> List[Tuple[DistinguishedName, Entry]]:
        if isinstance(base, str):
            base = DistinguishedName(base)
        self.connect()
        if self.cache is not None:
            if scope is Scope.BASE and search_filter is None:
                pair = self.cache.get_entry(base)
                if pair is not None:
                    logger.debug("cache hit: entry %s", base)
                    return [self._to_entry(*pair)]

            pairs = self.cache.get_search(base, scope, search_filter)
            if pairs is not None:
                logger.debug("cache hit: search %s %s %s", base, scope.name, search_filter)
                if 0 < max_entries < len(pairs):
                    logger.debug("trim results: %d down to %d", len(pairs), max_entries)
                    pairs = pairs[0:max_entries]
                return [self._to_entry(*self._refetch(*pair)) for pair in pairs]

        logger.debug("cache miss: search %s %s %s", base, scope.name, search_filter)
        results = self.provider.search(base, scope, search_filter, max_entries)
        pairs = [self._decode(*r) for r in results]

        entries = [self._to_entry(*pair) for pair in pairs]
        if self.cache is not None:
            logger.debug("cache fill: search %s %s %s: %d entries", base, scope.name, search_filter, len(entries))
            self.cache.put_search(base, scope, search_filter, [(dn, entry.attrs()) for dn, entry in entries])
        return entries

    def fetch_all(self, base: Union[str, DistinguishedName], scope: Scope, search_filter: Optional[str] = None,
                  max_entries: int = 0):
        return self._fetch(base, scope, search_filter, max_entries)

    def fetch_one(self, base: Union[str, DistinguishedName], scope: Scope, search_filter: Optional[str] = None):
        # max_entries == 2 so we can detect when the search returns more than one entry
        results = self._fetch(base, scope, search_filter, max_entries=2)
        if len(results) > 1:
            raise TooManyResultsError()

        return results[0] if len(results) > 0 else None
