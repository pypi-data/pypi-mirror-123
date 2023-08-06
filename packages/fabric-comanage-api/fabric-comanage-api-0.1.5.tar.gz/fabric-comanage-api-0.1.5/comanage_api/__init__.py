import requests_mock
from requests import Session

from ._coorgidentitylinks import coorg_identity_links_add, coorg_identity_links_delete, coorg_identity_links_edit, \
    coorg_identity_links_view_all, coorg_identity_links_view_by_identity, coorg_identity_links_view_one
from ._copeople import copeople_add, copeople_delete, copeople_edit, copeople_find, copeople_match, \
    copeople_view_all, copeople_view_per_co, copeople_view_per_identifier, copeople_view_one
from ._copersonroles import coperson_roles_add, coperson_roles_delete, coperson_roles_edit, coperson_roles_view_all, \
    coperson_roles_view_per_coperson, coperson_roles_view_per_cou, coperson_roles_view_one
from ._cous import cous_add, cous_delete, cous_edit, cous_view_all, cous_view_per_co, cous_view_one
from ._emailaddresses import email_addresses_add, email_addresses_delete, email_addresses_edit, \
    email_addresses_view_all, email_addresses_view_per_person, email_addresses_view_one
from ._identifiers import identifiers_add, identifiers_assign, identifiers_delete, identifiers_edit, \
    identifiers_view_all, identifiers_view_per_entity, identifiers_view_one
from ._names import names_add, names_delete, names_edit, names_view_all, names_view_per_person, names_view_one
from ._orgidentities import org_identities_add, org_identities_delete, org_identities_edit, org_identities_view_all, \
    org_identities_view_per_co, org_identities_view_per_identifier, org_identities_view_one
from ._sshkeys import ssh_keys_add, ssh_keys_delete, ssh_keys_edit, ssh_keys_view_all, ssh_keys_view_per_coperson, \
    ssh_keys_view_one

# fabric-comanage-api version
__VERSION__ = "0.1.5"


class ComanageApi(object):
    """
    fabric-comanage-api:

    Provide a limited Python 3 client implementation (wrapper) for
    COmanage REST API v1: https://spaces.at.internet2.edu/display/COmanage/REST+API+v1


    Attributes
    ----------
    co_api_url: str
        COmanage registry URL (required)
    co_api_user: str
        COmanage API username (required)
    co_api_pass: str
        COmanage API password (required)
    co_api_org_id: int
        COmanage Org ID (required)
    co_api_org_name: str
        COmanage Org Name (required)
    co_ssh_key_authenticator_id: int = None
        SSH Authenticator Plugin ID (optional)
    """

    def __init__(self, co_api_url: str, co_api_user: str, co_api_pass: str, co_api_org_id: int,
                 co_api_org_name: str, co_ssh_key_authenticator_id: int = None):
        # COmanage API user and pass
        self._CO_API_USER = str(co_api_user)
        self._CO_API_PASS = str(co_api_pass)
        # COmanage CO information
        self._CO_API_ORG_NAME = str(co_api_org_name)
        self._CO_API_ORG_ID = int(co_api_org_id)
        # COmanage Registry URL
        if str(co_api_url).endswith('/'):
            self._CO_API_URL = str(co_api_url)[:-1]
        else:
            self._CO_API_URL = str(co_api_url)
        # COmanage SshKeyAuthenticatorId
        if co_ssh_key_authenticator_id:
            self._CO_SSH_KEY_AUTHENTICATOR_ID = int(co_ssh_key_authenticator_id)
        else:
            self._CO_SSH_KEY_AUTHENTICATOR_ID = 0
        # Status Type options
        self.STATUS_OPTIONS = ['Active', 'Approved', 'Confirmed', 'Declined', 'Deleted', 'Denied', 'Duplicate',
                               'Expired',
                               'GracePeriod', 'Invited', 'Pending', 'PendingApproval', 'PendingConfirmation',
                               'Suspended']
        # Affiliation Type options
        self.AFFILIATION_OPTIONS = ['affiliate', 'alum', 'employee', 'faculty', 'member', 'staff', 'student']
        # EmailAddress Type options
        self.EMAILADDRESS_OPTIONS = ['codeptid', 'copersonid', 'organizationid', 'orgidentityid']
        # Entity Type options
        self.ENTITY_OPTIONS = ['codeptid', 'cogroupid', 'copersonid', 'organizationid', 'orgidentityid']
        # Person Type options
        self.PERSON_OPTIONS = ['copersonid', 'orgidentityid']
        # SSH Key Type options
        self.SSH_KEY_OPTIONS = ['ssh-dss', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384', 'ecdsa-sha2-nistp521',
                                'ssh-ed25519', 'ssh-rsa', 'ssh-rsa1']
        # create mock response session
        self._mock_session = Session()
        self._adapter = requests_mock.Adapter()
        self._mock_session.mount('mock://', self._adapter)
        # add mock adapters
        self._MOCK_501_URL = 'mock://not_implemented_501.local'
        self._adapter.register_uri('GET', self._MOCK_501_URL, reason='Not Implemented', status_code=501)
        # create comanage_api session
        self._s = Session()
        self._s.headers = {'Content-Type': 'application/json'}
        self._s.auth = (self._CO_API_USER, self._CO_API_PASS)

    # CoOrgIdentityLink API
    def coorg_identity_links_add(self):
        return coorg_identity_links_add(self)

    def coorg_identity_links_delete(self):
        return coorg_identity_links_delete(self)

    def coorg_identity_links_edit(self):
        return coorg_identity_links_edit(self)

    def coorg_identity_links_view_all(self):
        return coorg_identity_links_view_all(self)

    def coorg_identity_links_view_by_identity(self, identity_type: str, identity_id: int):
        return coorg_identity_links_view_by_identity(self, identity_type=identity_type, identity_id=identity_id)

    def coorg_identity_links_view_one(self, coorg_identity_link_id: int):
        return coorg_identity_links_view_one(self, coorg_identity_link_id=coorg_identity_link_id)

    # COperson API
    def copeople_add(self):
        return copeople_add(self)

    def copeople_delete(self):
        return copeople_delete(self)

    def copeople_edit(self):
        return copeople_edit(self)

    def copeople_find(self):
        return copeople_find(self)

    def copeople_match(self, given: str = None, family: str = None, mail: str = None, distinct_by_id: bool = True):
        return copeople_match(self, given=given, family=family, mail=mail, distinct_by_id=distinct_by_id)

    def copeople_view_all(self):
        return copeople_view_all(self)

    def copeople_view_per_co(self):
        return copeople_view_per_co(self)

    def copeople_view_per_identifier(self, identifier: str, distinct_by_id: bool = True):
        return copeople_view_per_identifier(self, identifier=identifier, distinct_by_id=distinct_by_id)

    def copeople_view_one(self, coperson_id: int):
        return copeople_view_one(self, coperson_id=coperson_id)

    # COPersonRoles API
    def coperson_roles_add(self, coperson_id: int, cou_id: int, status: str = None, affiliation: str = None):
        return coperson_roles_add(self, coperson_id=coperson_id, cou_id=cou_id, status=status, affiliation=affiliation)

    def coperson_roles_delete(self, coperson_role_id: int):
        return coperson_roles_delete(self, coperson_role_id=coperson_role_id)

    def coperson_roles_edit(self, coperson_role_id: int, coperson_id: int = None, cou_id: int = None,
                            status: str = None, affiliation: str = None):
        return coperson_roles_edit(self, coperson_role_id=coperson_role_id, coperson_id=coperson_id, cou_id=cou_id,
                                   status=status, affiliation=affiliation)

    def coperson_roles_view_all(self):
        return coperson_roles_view_all(self)

    def coperson_roles_view_per_coperson(self, coperson_id: int):
        return coperson_roles_view_per_coperson(self, coperson_id=coperson_id)

    def coperson_roles_view_per_cou(self, cou_id: int):
        return coperson_roles_view_per_cou(self, cou_id=cou_id)

    def coperson_roles_view_one(self, coperson_role_id: int):
        return coperson_roles_view_one(self, coperson_role_id=coperson_role_id)

    # COU API
    def cous_add(self, name: str, description: str, parent_id: int = None):
        return cous_add(self, name=name, description=description, parent_id=parent_id)

    def cous_delete(self, cou_id: int):
        return cous_delete(self, cou_id=cou_id)

    def cous_edit(self, cou_id: int, name: str = None, description: str = None, parent_id: int = None):
        return cous_edit(self, cou_id=cou_id, name=name, description=description, parent_id=parent_id)

    def cous_view_all(self):
        return cous_view_all(self)

    def cous_view_per_co(self):
        return cous_view_per_co(self)

    def cous_view_one(self, cou_id: int):
        return cous_view_one(self, cou_id=cou_id)

    # EmailAddress API
    def email_addresses_add(self):
        return email_addresses_add(self)

    def email_addresses_delete(self):
        return email_addresses_delete(self)

    def email_addresses_edit(self):
        return email_addresses_edit(self)

    def email_addresses_view_all(self):
        return email_addresses_view_all(self)

    def email_addresses_view_per_person(self, person_type: str, person_id: int):
        return email_addresses_view_per_person(self, person_type=person_type, person_id=person_id)

    def email_addresses_view_one(self, email_address_id: int):
        return email_addresses_view_one(self, email_address_id=email_address_id)

    # Indentifier API
    def identifiers_add(self):
        return identifiers_add(self)

    def identifiers_assign(self):
        return identifiers_assign(self)

    def identifiers_delete(self):
        return identifiers_delete(self)

    def identifiers_edit(self):
        return identifiers_edit(self)

    def identifiers_view_all(self):
        return identifiers_view_all(self)

    def identifiers_view_per_entity(self, entity_type: str, entity_id: int):
        return identifiers_view_per_entity(self, entity_type=entity_type, entity_id=entity_id)

    def identifiers_view_one(self, identifier_id: int):
        return identifiers_view_one(self, identifier_id=identifier_id)

    # Name API
    def names_add(self):
        return names_add(self)

    def names_delete(self):
        return names_delete(self)

    def names_edit(self):
        return names_edit(self)

    def names_view_all(self):
        return names_view_all(self)

    def names_view_per_person(self, person_type: str, person_id: int):
        return names_view_per_person(self, person_type=person_type, person_id=person_id)

    def names_view_one(self, name_id: int):
        return names_view_one(self, name_id=name_id)

    # OrgIdentity API
    def org_identities_add(self):
        return org_identities_add(self)

    def org_identities_delete(self):
        return org_identities_delete(self)

    def org_identities_edit(self):
        return org_identities_edit(self)

    def org_identities_view_all(self):
        return org_identities_view_all(self)

    def org_identities_view_per_co(self):
        return org_identities_view_per_co(self)

    def org_identities_view_per_identifier(self, identifier_id: int):
        return org_identities_view_per_identifier(self, identifier_id=identifier_id)

    def org_identities_view_one(self, org_identity_id: int):
        return org_identities_view_one(self, org_identity_id=org_identity_id)

    # SshKey API
    def ssh_keys_add(self, coperson_id: int, ssh_key: str, key_type: str, comment: str = None,
                     ssh_key_authenticator_id: int = None):
        return ssh_keys_add(self, coperson_id=coperson_id, ssh_key=ssh_key, key_type=key_type, comment=comment,
                            ssh_key_authenticator_id=ssh_key_authenticator_id)

    def ssh_keys_delete(self, ssh_key_id: int):
        return ssh_keys_delete(self, ssh_key_id=ssh_key_id)

    def ssh_keys_edit(self, ssh_key_id: int, coperson_id: int = None, ssh_key: str = None, key_type: str = None,
                      comment: str = None, ssh_key_authenticator_id: int = None):
        return ssh_keys_edit(self, ssh_key_id=ssh_key_id, coperson_id=coperson_id, ssh_key=ssh_key, key_type=key_type,
                             comment=comment, ssh_key_authenticator_id=ssh_key_authenticator_id)

    def ssh_keys_view_all(self):
        return ssh_keys_view_all(self)

    def ssh_keys_view_per_coperson(self, coperson_id: int):
        return ssh_keys_view_per_coperson(self, coperson_id=coperson_id)

    def ssh_keys_view_one(self, ssh_key_id: int):
        return ssh_keys_view_one(self, ssh_key_id=ssh_key_id)
