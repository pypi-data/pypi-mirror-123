import os
from typing import List, Tuple

import ldap.sasl
import ldap.controls

from .ldap_provider import LdapProvider, LdapError
from .schema import DistinguishedName
from .scope import Scope


class OpenLdapProvider(LdapProvider):

    def __init__(self, **kwargs):
        self.uri = None
        self._kwargs = kwargs
        self._ldap = None

    def set_option(self, name, value):
        ldap.set_option(name, value)

    def connect(self, uri):
        try:
            if not self.is_connected():
                self.uri = uri
                self._ldap = ldap.initialize(self.uri, **self._kwargs)
                self._ldap.protocol_version = ldap.VERSION3
        except ldap.LDAPError as err:
            raise LdapError(str(err))

    def is_connected(self) -> bool:
        return self._ldap is not None

    def start_tls(self):
        try:
            self._ldap.start_tls_s()
        except ldap.LDAPError as err:
            raise LdapError(str(err))

    def bind_simple(self, dn: DistinguishedName, password: str):
        try:
            self._ldap.simple_bind_s(str(dn), password)
        except ldap.LDAPError as err:
            raise LdapError(str(err))

    def bind_sasl_external(self):
        try:
            self._ldap.sasl_interactive_bind_s("", ldap.sasl.external())
        except ldap.LDAPError as err:
            raise LdapError(str(err))

    def search(self, base: DistinguishedName, scope: Scope, search_filter: str = None, max_entries=0) \
            -> List[Tuple[DistinguishedName, dict]]:
        try:
            server_controls = []
            if max_entries > 0:
                server_controls.append(ldap.controls.SimplePagedResultsControl(size=max_entries, cookie=''))

            results = self._ldap.search_ext(str(base), scope.value, search_filter, None, serverctrls=server_controls)
            result_type, result_data = self._ldap.result(results, 1)

            if 0 < max_entries < len(result_data):
                result_data = result_data[0:max_entries]

            return result_data
        except ldap.LDAPError as err:
            raise LdapError(str(err))

