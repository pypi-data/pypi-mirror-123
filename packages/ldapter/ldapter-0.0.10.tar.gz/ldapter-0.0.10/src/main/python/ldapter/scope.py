from enum import Enum

import ldap


class Scope(Enum):
    BASE = ldap.SCOPE_BASE
    SUBTREE = ldap.SCOPE_SUBTREE
    ONELEVEL = ldap.SCOPE_ONELEVEL
    SUBORDINATE = ldap.SCOPE_SUBORDINATE


