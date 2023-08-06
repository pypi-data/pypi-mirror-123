# comanage_api/_coorgidentitylinks.py

"""
CoOrgIdentityLink API - https://spaces.at.internet2.edu/display/COmanage/CoOrgIdentityLink+API

Methods
-------
coorg_identity_links_add() -> dict
    ### NOT IMPLEMENTED ###
    Add a new CO Org Identity Link.
    A person must have an Org Identity and a CO Person record before they can be linked.
    Note that invitations are a separate operation.
coorg_identity_links_delete() -> bool
    ### NOT IMPLEMENTED ###
    Remove a CO Org Identity Link.
coorg_identity_links_edit() -> bool
    ### NOT IMPLEMENTED ###
    Edit an existing CO Identity Link.
coorg_identity_links_view_all() -> dict
    Retrieve all existing CO Identity Links.
coorg_identity_links_view_by_identity(identifier_id: int) -> dict
    Retrieve all existing CO Identity Links for a CO Person or an Org Identity.
coorg_identity_links_view_one(org_identity_id: int) -> dict
    Retrieve an existing CO Identity Link.
"""

import json


def coorg_identity_links_add(self) -> dict:
    """
    ### NOT IMPLEMENTED ###
    Add a new CO Org Identity Link.
    A person must have an Org Identity and a CO Person record before they can be linked.
    Note that invitations are a separate operation.

    :param self:
    :return
        501 Server Error: Not Implemented for url: mock://not_implemented_501.local:
    """
    url = self._MOCK_501_URL
    resp = self._mock_session.get(
        url=url
    )
    if resp.status_code == 201:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coorg_identity_links_delete(self) -> bool:
    """
    ### NOT IMPLEMENTED ###
    Remove a CO Org Identity Link.

    :param self:
    :return
        501 Server Error: Not Implemented for url: mock://not_implemented_501.local:
    """
    url = self._MOCK_501_URL
    resp = self._mock_session.get(
        url=url
    )
    if resp.status_code == 200:
        return True
    else:
        resp.raise_for_status()


def coorg_identity_links_edit(self) -> bool:
    """
    ### NOT IMPLEMENTED ###
    Edit an existing CO Identity Link.

    :param self:
    :return
        501 Server Error: Not Implemented for url: mock://not_implemented_501.local:
    """
    url = self._MOCK_501_URL
    resp = self._mock_session.get(
        url=url
    )
    if resp.status_code == 200:
        return True
    else:
        resp.raise_for_status()


def coorg_identity_links_view_all(self) -> dict:
    """
    Retrieve all existing CO Identity Links.

    :param self:
    :return
        {
            "ResponseType":"CoOrgIdentityLinks",
            "Version":"1.0",
            "CoOrgIdentityLinks":
            [
                {
                    "Version":"1.0",
                    "Id":"<Id>",
                    "CoPersonId":"<CoPersonId>",
                    "OrgIdentityId":"<OrgIdentityId>",
                    "Created":"<CreateTime>",
                    "Modified":"<ModTime>"
                },
                {...}
            ]
        }:

    Response Format
        HTTP Status         Response Body                   Description
        200 OK              CoOrgIdentityLink Response      CoOrgIdentityLinks returned
        401 Unauthorized                                    Authentication required
        500 Other Error                                     Unknown error
    """
    url = self._CO_API_URL + '/co_org_identity_links.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()



def coorg_identity_links_view_by_identity(self, identity_type: str, identity_id: int) -> dict:
    """
    Retrieve all existing CO Identity Links for a CO Person or an Org Identity.

    :param self:
    :param identity_type:
    :param identity_id:
    :return
       {
            "ResponseType":"CoOrgIdentityLinks",
            "Version":"1.0",
            "CoOrgIdentityLinks":
            [
                {
                    "Version":"1.0",
                    "Id":"<Id>",
                    "CoPersonId":"<CoPersonId>",
                    "OrgIdentityId":"<OrgIdentityId>",
                    "Created":"<CreateTime>",
                    "Modified":"<ModTime>"
                },
                {...}
            ]
        }:

    Response Format
        HTTP Status                 Response Body                   Description
        200 OK                      CoOrgIdentityLink Response      CoOrgIdentityLinks returned
        401 Unauthorized                                            Authentication required
        404 CO Person Unknown                                       copersonid not found
        404 Org Identity Unknown                                    orgidentityid not found
        500 Other Error                                             Unknown error
    """
    if not identity_type:
        identity_type = 'copersonid'
    else:
        identity_type = str(identity_type).lower()
    if identity_type not in self.PERSON_OPTIONS:
        raise TypeError("Invalid Fields 'identity_type'")
    url = self._CO_API_URL + '/co_org_identity_links.json'
    params = {str(identity_type): str(identity_id)}
    resp = self._s.get(
        url=url,
        params=params
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coorg_identity_links_view_one(self, coorg_identity_link_id: int) -> dict:
    """
    Retrieve an existing CO Identity Link.

    :param self:
    :param coorg_identity_link_id:
    :return
        {
            "ResponseType":"CoOrgIdentityLinks",
            "Version":"1.0",
            "CoOrgIdentityLinks":
            [
                {
                    "Version":"1.0",
                    "Id":"<Id>",
                    "CoPersonId":"<CoPersonId>",
                    "OrgIdentityId":"<OrgIdentityId>",
                    "Created":"<CreateTime>",
                    "Modified":"<ModTime>"
                }
            ]
        }:

    Response Format
        HTTP Status                     Response Body                   Description
        200 OK                          CoOrgIdentityLink Response      CoOrgIdentityLinks returned
        401 Unauthorized                                                Authentication required
        404 CoOrgIdentityLink Unknown                                   id not found
        500 Other Error                                                 Unknown error
    """
    url = self._CO_API_URL + '/co_org_identity_links/' + str(coorg_identity_link_id) + '.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()
