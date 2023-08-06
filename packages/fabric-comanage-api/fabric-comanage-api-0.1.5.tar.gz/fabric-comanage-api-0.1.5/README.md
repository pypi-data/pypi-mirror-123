# python-comanage-api

Provide a limited Python 3 client implementation (wrapper) for COmanage REST API v1: [https://spaces.at.internet2.edu/display/COmanage/REST+API+v1](https://spaces.at.internet2.edu/display/COmanage/REST+API+v1)

Available at PyPi: [https://pypi.org/project/fabric-comanage-api/](https://pypi.org/project/fabric-comanage-api/)

**DISCLAIMER: The code herein may not be up to date nor compliant with the most recent package and/or security notices. The frequency at which this code is reviewed and updated is based solely on the lifecycle of the project for which it was written to support, and is not actively maintained outside of that scope. Use at your own risk.**

## Table of contents

- [TL;DR](#tldr)
- [API endpoints](#endpoints)
    - [CoOrgIdentityLink](#coorgidentitylinks)
    - [CoPerson](#coperson)
    - [CoPersonRole](#copersonrole)
    - [Cou](#cou)
    - [EmailAddress](#emailaddress)
    - [Identifier](#identifier)
    - [Name](#name)
    - [OrgIdentity](#orgidentity)
    - [SshKey](#sshkey)
- [Usage](#usage)
- [SSH Key Authenticator Plugin in COmanage](#sshplugin)
- [References](#reference)

## <a name="tldr"></a>TL;DR

Install the latest version from PyPi

```console
pip install fabric-comanage-api
```

Create a COmanage API connection

```python
from comanage_api import ComanageApi

api = ComanageApi(
    co_api_url=COMANAGE_API_URL,
    co_api_user=COMANAGE_API_USER,
    co_api_pass=COMANAGE_API_PASS,
    co_api_org_id=COMANAGE_API_CO_ID,
    co_api_org_name=COMANAGE_API_CO_NAME,
    co_ssh_key_authenticator_id=COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID
)
```

Get some data! (example using `cous_view_per_co()` which retrieves all COUs attached to a given CO)

```python
$ python
Python 3.9.6 (v3.9.6:db3ff76da1, Jun 28 2021, 11:49:53)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> from comanage_api import ComanageApi
>>>
>>> api = ComanageApi(
...     co_api_url='https://FQDN_OF_REGISTRY',
...     co_api_user='co_123.api-user-name',
...     co_api_pass='xxxx-xxxx-xxxx-xxxx',
...     co_api_org_id='123',
...     co_api_org_name='RegistryName',
...     co_ssh_key_authenticator_id='123'
... )
>>>
>>> cous = api.cous_view_per_co()
>>>
>>> print(cous)
{'ResponseType': 'Cous', 'Version': '1.0', 'Cous': [{'Version': '1.0', 'Id': '38', 'CoId': '123', 'Name': 'enrollment-approval', 'Description': 'Enrollment Approval Personnel - can approve or deny new registry members', 'Lft': '66', 'Rght': '67', 'Created': '2021-09-10 14:33:11', 'Modified': '2021-09-10 14:33:11', 'Revision': '0', 'Deleted': False, 'ActorIdentifier': 'http://cilogon.org/serverA/users/242181'}, {'Version': '1.0', 'Id': '39', 'CoId': '123', 'Name': 'impact-users', 'Description': "ImPACT Users - Registering with the ImPACT site will add new user's to this group", 'Lft': '68', 'Rght': '69', 'Created': '2021-09-10 14:44:09', 'Modified': '2021-09-10 14:44:09', 'Revision': '0', 'Deleted': False, 'ActorIdentifier': 'http://cilogon.org/serverA/users/242181'}]}
>>>
>>> import json
>>> print(json.dumps(cous, indent=2))
{
  "ResponseType": "Cous",
  "Version": "1.0",
  "Cous": [
    {
      "Version": "1.0",
      "Id": "38",
      "CoId": "123",
      "Name": "enrollment-approval",
      "Description": "Enrollment Approval Personnel - can approve or deny new registry members",
      "Lft": "66",
      "Rght": "67",
      "Created": "2021-09-10 14:33:11",
      "Modified": "2021-09-10 14:33:11",
      "Revision": "0",
      "Deleted": false,
      "ActorIdentifier": "http://cilogon.org/serverA/users/242181"
    },
    {
      "Version": "1.0",
      "Id": "39",
      "CoId": "123",
      "Name": "impact-users",
      "Description": "ImPACT Users - Registering with the ImPACT site will add new user's to this group",
      "Lft": "68",
      "Rght": "69",
      "Created": "2021-09-10 14:44:09",
      "Modified": "2021-09-10 14:44:09",
      "Revision": "0",
      "Deleted": false,
      "ActorIdentifier": "http://cilogon.org/serverA/users/242181"
    }
  ]
}
>>>
```

## <a name="endpoints"></a>API endpoints

Return types based on implementation status of wrapped API endpoints

- Implemented:
    - `-> dict`: Data is returned as a Python [Dictionary](https://docs.python.org/3/c-api/dict.html) object
    - `-> bool`: Success/Failure is returned as Python [Boolean](https://docs.python.org/3/c-api/bool.html) object
- Not Implemented (`### NOT IMPLEMENTED ###`): 
    - `-> dict`: raise exception (`HTTPError - 501 Server Error: Not Implemented for url: mock://not_implemented_501.local`)
    - `-> bool`: raise exception (`HTTPError - 501 Server Error: Not Implemented for url: mock://not_implemented_501.local`)

### <a name="coorgidentitylink"></a>[CoOrgIdentityLink API](https://spaces.at.internet2.edu/display/COmanage/CoOrgIdentityLink+API) (COmanage v4.0.0+)

- `coorg_identity_links_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new CO Org Identity Link.
    - A person must have an Org Identity and a CO Person record before they can be linked.
    - Note that invitations are a separate operation.
- `coorg_identity_links_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove a CO Org Identity Link.
- `coorg_identity_links_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing CO Identity Link.
- `coorg_identity_links_view_all() -> dict`
    - Retrieve all existing CO Identity Links.
- `coorg_identity_links_view_by_identity(identifier_id: int) -> dict`
    - Retrieve all existing CO Identity Links for a CO Person or an Org Identity.
- `coorg_identity_links_view_one(org_identity_id: int) -> dict`
    - Retrieve an existing CO Identity Link.

**NOTE**: when provided, valid values for `identity_type` as follows:

```python
IDENTITY_OPTIONS = ['copersonid', 'orgidentityid']
```

### <a name="coperson"></a>[CoPerson API](https://spaces.at.internet2.edu/display/COmanage/CoPerson+API) (COmanage v3.3.0+)

- `copeople_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new CO Person. A person must have an OrgIdentity before they can be added to a CO.
    - Note that linking to an OrgIdentity and invitations are separate operations.
- `copeople_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove a CO Person. This method will also delete related data, such as `CoPersonRoles`, `EmailAddresses`,
and `Identifiers`. 
    - A person must be removed from any COs (CoPerson records must be deleted)
before the OrgIdentity record can be removed.
- `copeople_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing CO Person.
- `copeople_find() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Search for existing CO Person records.
    - When too many records are found, a message may be returned rather than specific records.
- `copeople_match(given: str = None, family: str = None, mail: str = None, distinct_by_id: bool = True) -> dict`
    - Attempt to match existing CO Person records.
    - Note that matching is not performed on search criteria of less than 3 characters,
    or for email addresses that are not syntactically valid.
- `copeople_view_all() -> dict`
    - Retrieve all existing CO People.
- `copeople_view_per_co() -> dict`
    - Retrieve all existing CO People for the specified CO.
- `copeople_view_per_identifier(identifier: str, distinct_by_id: bool = True) -> dict`
    - Retrieve all existing CO People attached to the specified identifier.
    - Note the specified identifier must be attached to a CO Person, not an Org Identity.
- `copeople_view_one(coperson_id: int) -> dict`
    - Retrieve an existing CO Person.

### <a name="copersonrole"></a>[CoPersonRole API](https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API) (COmanage v3.3.0+)

- `coperson_roles_add(coperson_id: int, cou_id: int, status: str = None, affiliation: str = None) -> dict`
    - Add a new CO Person Role.
- `coperson_roles_delete(coperson_role_id: int) -> bool`
    - Remove a CO Person Role.
- `coperson_roles_edit(coperson_role_id: int, coperson_id: int = None, cou_id: int = None, status: str = None, affiliation: str = None) -> bool`
    - Edit an existing CO Person Role.
- `coperson_roles_view_all() -> dict`
    - Retrieve all existing CO Person Roles.
- `coperson_roles_view_per_coperson(coperson_id: int) -> dict`
    - Retrieve all existing CO Person Roles for the specified CO Person. Available since Registry v2.0.0.
- `coperson_roles_view_per_cou(cou_id: int) -> dict`
    - Retrieve all existing CO Person Roles for the specified COU.
- `coperson_roles_view_one(coperson_role_id: int) -> dict`
    - Retrieve an existing CO Person Role.

**NOTE**: when provided, valid values for `status` and `affiliation` as follows:

```python
STATUS_OPTIONS = ['Active', 'Approved', 'Confirmed', 'Declined', 'Deleted', 'Denied', 'Duplicate', 
'Expired', 'GracePeriod', 'Invited', 'Pending', 'PendingApproval', 'PendingConfirmation', 'Suspended']
AFFILIATION_OPTIONS = ['affiliate', 'alum', 'employee', 'faculty', 'member', 'staff', 'student']
```

### <a name="cou"></a>[COU API](https://spaces.at.internet2.edu/display/COmanage/COU+API) (COmanage v3.3.0+)

- `cous_add(name: str, description: str, parent_id: int = None) -> dict`
    - Add a new Cou.
- `cous_delete(cou_id: int) -> bool`
    - Remove a Cou.
- `cous_edit(cou_id: int, name: str = None, description: str = None, parent_id: int = None) -> bool`
    - Edit an existing Cou.
- `cous_view_all() -> dict`
    - Retrieve all existing Cous.
- `cous_view_per_co() -> dict`
    - Retrieve Cou attached to a CO.
- `cous_view_one(cou_id: int) -> dict`
    - Retrieve an existing Cou.

**NOTE**: `cous_edit` has a special case where setting `parent_id=0` will reset the value of the `parent_id` of the COU to be None (have no parent)

### <a name="emailaddress"></a>[EmailAddress API](https://spaces.at.internet2.edu/display/COmanage/EmailAddress+API) (COmanage v3.3.0+)

- `email_addresses_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new EmailAddress.
- `email_addresses_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove an EmailAddress.
- `email_addresses_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing EmailAddress.
- `email_addresses_view_all() -> dict`
    - Retrieve all existing EmailAddresses.
- `email_addresses_view_per_person(person_type: str, person_id: int) -> dict`
    - Retrieve EmailAddresses attached to a CO Department, CO Person, or Org Identity.
- `email_addresses_view_one(email_address_id: int) -> dict`
    - Retrieve an existing EmailAddress.

**NOTE**: when provided, valid values for `person_type` as follows:

```python
EMAILADDRESS_OPTIONS = ['codeptid', 'copersonid', 'organizationid', 'orgidentityid']
```

### <a name="identifier"></a>[Identifier API](https://spaces.at.internet2.edu/display/COmanage/Identifier+API) (COmanage v3.3.0+)

- `identifiers_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new Identifier.
- `identifiers_assign() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Assign Identifiers for a CO Person.
- `identifiers_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove an Identifier.
- `identifiers_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing Identifier.
- `identifiers_view_all() -> dict`
    - Retrieve all existing Identifiers.
- `identifiers_view_per_entity(entity_type: str, entity_id: int) -> dict`
    - Retrieve Identifiers attached to a CO Department, Co Group, CO Person, or Org Identity.
- `identifiers_view_one(identifier_id: int) -> dict`
    - Retrieve an existing Identifier.   

**NOTE**: when provided, valid values for `entity_type` as follows:

```python
ENTITY_OPTIONS = ['codeptid', 'cogroupid', 'copersonid', 'organizationid', 'orgidentityid']
```   

### <a name="name"></a>[Name API](https://spaces.at.internet2.edu/display/COmanage/Name+API) (COmanage v3.3.0+)

- `names_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new Name.
- `names_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove a Name.
- `names_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing Name.
- `names_view_all() -> dict`
    - Retrieve all existing Names.
- `names_view_per_person(person_type: str, person_id: int) -> dict`
    - Retrieve Names attached to a CO Person or Org Identity.
- `names_view_one(name_id: int) -> dict`
    - Retrieve Names attached to a CO Person or Org Identity.
 
**NOTE**: when provided, valid values for `person_type` as follows:

```python
PERSON_OPTIONS = ['copersonid', 'orgidentityid']
```

### <a name="orgidentity"></a>[OrgIdentity API](https://spaces.at.internet2.edu/display/COmanage/OrgIdentity+API) (COmanage v3.3.0+)

- `org_identities_add() -> dict`
    - `### NOT IMPLEMENTED ###`
    - Add a new Organizational Identity. A person must have an `OrgIdentity` before they can be added to a CO.
- `org_identities_delete() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Remove an Organizational Identity.
    - The person must be removed from any COs (`CoPerson`) before the OrgIdentity record can be removed.
    - This method will also delete related data, such as `Addresses`, `EmailAddresses`, and `TelephoneNumbers`.
- `org_identities_edit() -> bool`
    - `### NOT IMPLEMENTED ###`
    - Edit an existing Organizational Identity.
- `org_identities_view_all() -> dict`
    - Retrieve all existing Organizational Identities.
- `org_identities_view_per_co(person_type: str, person_id: int) -> dict`
    - Retrieve all existing Organizational Identities for the specified CO.
- `org_identities_view_per_identifier(identifier_id: int) -> dict`
    - Retrieve all existing Organizational Identities attached to the specified identifier.
    - Note the specified identifier must be attached to an Org Identity, not a CO Person.
- `org_identities_view_one(org_identity_id: int) -> dict`
    - Retrieve an existing Organizational Identity.


### <a name="sshkey"></a>[SshKey API](https://spaces.at.internet2.edu/display/COmanage/SshKey+API) (COmanage v4.0.0+)

**REQUIRES**: The [SSH Key Authenticator plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin) which manages SSH Public Keys for CO People.

- `ssh_keys_add(coperson_id: int, ssh_key: str, key_type: str, comment: str = None, ssh_key_authenticator_id: int = None) -> dict`
    - Add a new SSH Key.
- `ssh_keys_delete(ssh_key_id: int) -> bool`
    - Remove an SSH Key.
- `ssh_keys_edit(ssh_key_id: int, coperson_id: int = None, ssh_key: str = None, key_type: str = None, comment: str = None, ssh_key_authenticator_id: int = None) -> bool`
    - Edit an exiting SSH Key.
- `ssh_keys_view_all() -> dict`
    - Retrieve all existing SSH Keys.
- `ssh_keys_view_per_coperson(coperson_id: int) -> dict`
    - Retrieve all existing SSH Keys for the specified CO Person.
- `ssh_keys_view_one(ssh_key_id: int) -> dict`
    - Retrieve an existing SSH Key.

**NOTE**: when provided, valid values for `ssh_key_type` as follows:

```python
SSH_KEY_OPTIONS = ['ssh-dss', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384', 
'ecdsa-sha2-nistp521', 'ssh-ed25519', 'ssh-rsa', 'ssh-rsa1']
```

## <a name="usage"></a>Usage

Set up a virtual environment (`virtualenv` is used in these examples)

```console
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
```

### Install supporting packages

Install from PyPi

```console
pip install fabric-comanage-api
```

**OR** 

Install for Local Development

```console
pip install -r requirements.txt
```

### Configure your environment

Create a `.env` file from the included template if you don't want to put the API credentials in your code. Example code makes use of [python-dotenv](https://pypi.org/project/python-dotenv/)

```console
cp template.env .env
```

Configure `.env` based on your COmanage Registry settings

```env
# COmanage API user and pass
COMANAGE_API_USER=co_123.api-user-name
COMANAGE_API_PASS=xxxx-xxxx-xxxx-xxxx
# COmanage CO Information
COMANAGE_API_CO_NAME=RegistryName
COMANAGE_API_CO_ID=123
# COmanage registry URL
COMANAGE_API_URL=https://FQDN_OF_REGISTRY
# COmanage SshKeyAuthenticatorId (optional)
COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID=123
```

### Example Code

See code in [examples](examples/) for a demonstration of how to use each endpoint

## <a name="sshplugin"></a>SSH Key Authenticator Plugin

The [SSH Key Authenticator plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin) manages SSH Public Keys for CO People.

- The SSH Key Authenticator plugin is available as of Registry v3.3.0. Prior to this version, SSH Key management is available via the CO Person canvas.

After registration you can find the value for `COMANAGE_API_SSH_KEY_AUTHENTICATOR_ID` in the URL for editing the Authenticator:

- It would be **3** in this example URL: [https://registry.cilogon.org/registry/authenticators/edit/3]()

**NOTE**:

- Experimental
    - The SshKey API is implemented via the SSH Key Authenticator Plugin.
      REST APIs provided by plugins are currently considered Experimental, and as such this interface may change
      without notice between minor releases.

- Implementation Notes
    - Only JSON format is supported. XML format is not supported.
    - Note the URLs for this API use plugin syntax. (There is an extra component to the path.)
    - As defined in the SshKey Schema, an SSH Key Authenticator ID is required as part of the request.
      This refers to the Authenticator instantiated for the CO.
    - Authenticators that are locked cannot be managed by the API.

### Adding a new SSH Key Authenticator in COmanage

To create a new SSH Key Authenticator first select the "Authenticators" option from the COmanage configuraiton page

![](./imgs/SshKeyAuthenticator_1.png)

Next select the "Add Authenticator" option

![](./imgs/SshKeyAuthenticator_2.png)

Populate the required fields and set Status to "Active" and "Add" the Authenticator

![](./imgs/SshKeyAuthenticator_3.png)

Upon success a green box will denote the new Authenticator has been added

![](./imgs/SshKeyAuthenticator_4.png)

Now when choosing the "Authenicators" option from the COmanage configuration page you should see your newly created Authenticator

![](./imgs/SshKeyAuthenticator_5.png)

Pressing the "Edit" option will display the fields for the Authenticator along with its `SshKeyAuthenticatorId` value in the URL (**3** in this example)

![](./imgs/SshKeyAuthenticator_6.png)

## <a name="reference"></a>References

- COmanage REST API v1: [https://spaces.at.internet2.edu/display/COmanage/REST+API+v1](https://spaces.at.internet2.edu/display/COmanage/REST+API+v1)
- CoOrgIdentityLink API: [https://spaces.at.internet2.edu/display/COmanage/CoOrgIdentityLink+API](https://spaces.at.internet2.edu/display/COmanage/CoOrgIdentityLink+API)
- COU API: [https://spaces.at.internet2.edu/display/COmanage/COU+API](https://spaces.at.internet2.edu/display/COmanage/COU+API)
- CoPerson API: [https://spaces.at.internet2.edu/display/COmanage/CoPerson+API](https://spaces.at.internet2.edu/display/COmanage/CoPerson+API)
- CoPersonRole API: [https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API](https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API)
- EmailAddress API: [https://spaces.at.internet2.edu/display/COmanage/EmailAddress+API](https://spaces.at.internet2.edu/display/COmanage/EmailAddress+API)
- Identifier API: [https://spaces.at.internet2.edu/display/COmanage/Identifier+API](https://spaces.at.internet2.edu/display/COmanage/Identifier+API)
- Name API: [https://spaces.at.internet2.edu/display/COmanage/Name+API](https://spaces.at.internet2.edu/display/COmanage/Name+API)
- OrgIdentity API: [https://spaces.at.internet2.edu/display/COmanage/OrgIdentity+API](https://spaces.at.internet2.edu/display/COmanage/OrgIdentity+API)
- SsHKey API: [https://spaces.at.internet2.edu/display/COmanage/SshKey+API](https://spaces.at.internet2.edu/display/COmanage/SshKey+API)
- SSH Key Authenticator Plugin: [https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin](https://spaces.at.internet2.edu/display/COmanage/SSH+Key+Authenticator+Plugin)
- PyPi: [https://pypi.org](https://pypi.org)
