from abc import ABC
from typing import Tuple, List

from .schema import DistinguishedName
from .scope import Scope


class LdapError(BaseException):
    pass


class LdapProvider(ABC):

    def set_option(self, name, value):
        pass

    def connect(self, uri):
        pass

    def is_connected(self) -> bool:
        pass

    def start_tls(self):
        pass

    def bind_simple(self, dn: DistinguishedName, password: str):
        pass

    def bind_sasl_external(self):
        pass

    def search(self, base: DistinguishedName, scope: Scope, search_filter: str = None, max_entries: int = 0) \
            -> List[Tuple[DistinguishedName, dict]]:
        pass

