# comanage_api/_identifiers.py

"""
Identifier API - https://spaces.at.internet2.edu/display/COmanage/Identifier+API

Methods
-------
identifiers_add() -> dict
    ### NOT IMPLEMENTED ###
    Add a new Identifier.
identifiers_assign() -> bool
    ### NOT IMPLEMENTED ###
    Assign Identifiers for a CO Person.
identifiers_delete() -> bool
    ### NOT IMPLEMENTED ###
    Remove an Identifier.
identifiers_edit() -> bool
    ### NOT IMPLEMENTED ###
    Edit an existing Identifier.
identifiers_view_all() -> dict
    Retrieve all existing Identifiers.
identifiers_view_per_entity(entity_type: str, entity_id: int) -> dict
    Retrieve Identifiers attached to a CO Department, Co Group, CO Person, or Org Identity.
identifiers_view_one(identifier_id: int) -> dict
    Retrieve an existing Identifier.
"""

import json


def identifiers_add(self) -> dict:
    """
    ### NOT IMPLEMENTED ###
    Add a new Identifier.

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


def identifiers_assign(self) -> bool:
    """
    ### NOT IMPLEMENTED ###
    Assign Identifiers for a CO Person.

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


def identifiers_delete(self) -> bool:
    """
    ### NOT IMPLEMENTED ###
    Remove an Identifier.

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


def identifiers_edit(self) -> bool:
    """
    ### NOT IMPLEMENTED ###
    Edit an existing Identifier.

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


def identifiers_view_all(self) -> dict:
    """
    Retrieve all existing Identifiers.

    :param self:
    :return
        {
          "ResponseType":"Identifiers",
          "Version":"1.0",
          "Identifiers":
          [
            {
              "Version":"1.0",
              "Id":"<ID>",
              "Type":"<Type>",
              "Identifier":"<Identifier>",
              "Login":true|false,
              "Person":{"Type":("CO"|"Dept"|"Group"|"Org"|"Organization"),"ID":"<ID>"},
              "CoProvisioningTargetId":"<CoProvisioningTargetId>",
              "Status":"Active"|"Deleted",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>"
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status         Response Body           Description
        200 OK              Identifier Response     Identifiers returned
        401 Unauthorized                            Authentication required
        500 Other Error                             Unknown error
    """
    url = self._CO_API_URL + '/identifiers.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def identifiers_view_per_entity(self, entity_type: str, entity_id: int) -> dict:
    """
    Retrieve Identifiers attached to a CO Department, Co Group, CO Person, or Org Identity.

    :param self:
    :param entity_type:
    :param entity_id:
    :return
        {
          "ResponseType":"Identifiers",
          "Version":"1.0",
          "Identifiers":
          [
            {
              "Version":"1.0",
              "Id":"<ID>",
              "Type":"<Type>",
              "Identifier":"<Identifier>",
              "Login":true|false,
              "Person":{"Type":("CO"|"Dept"|"Group"|"Org"|"Organization"),"ID":"<ID>"},
              "CoProvisioningTargetId":"<CoProvisioningTargetId>",
              "Status":"Active"|"Deleted",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>"
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status                 Response Body           Description
        200 OK                      Identifier Response     Identifier returned
        204 CO Department                                   The requested CO Department was found,
            Has No Identifier                                   but has no identifiers attached
        204 CO Group                                        The requested CO Group was found,
            Has No Identifier                                   but has no identifiers attached
        204 CO Person                                       The requested CO Person was found,
            Has No Identifier                                   but has no identifiers attached
        204 Organization                                    The requested Organization was found,
            Has No Identifier                                   but has no identifiers attached
        204 Org Identity                                    The requested Org Identity was found,
            Has No Identifier                                   but has no identifiers attached
        401 Unauthorized                                    Authentication required
        404 CO Department Unknown                           id not found for CO Department
        404 CO Group Unknown                                id not found for CO Group
        404 CO Person Unknown                               id not found for CO Person
        404 Organization Unknown                            id not found for Organization
        404 Org Identity Unknown                            id not found for Org Identity
        500 Other Error                                     Unknown error
    """
    if not entity_type:
        entity_type = 'copersonid'
    else:
        entity_type = str(entity_type).lower()
    if entity_type not in self.ENTITY_OPTIONS:
        raise TypeError("Invalid Fields 'entity_type'")
    url = self._CO_API_URL + '/identifiers.json'
    params = {str(entity_type): str(entity_id)}
    resp = self._s.get(
        url=url,
        params=params
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def identifiers_view_one(self, identifier_id: int) -> dict:
    """
    Retrieve an existing Identifier.

    :param self:
    :param identifier_id:
    :return
        {
          "ResponseType":"Identifiers",
          "Version":"1.0",
          "Identifiers":
          [
            {
              "Version":"1.0",
              "Id":"<ID>",
              "Type":"<Type>",
              "Identifier":"<Identifier>",
              "Login":true|false,
              "Person":{"Type":("CO"|"Dept"|"Group"|"Org"|"Organization"),"ID":"<ID>"},
              "CoProvisioningTargetId":"<CoProvisioningTargetId>",
              "Status":"Active"|"Deleted",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>"
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status                 Response Body           Description
        200 OK                      Identifier Response     Identifiers returned
        401 Unauthorized                                    Authentication required
        404 Identifier Unknown                              id not found
        500 Other Error                                     Unknown error
    """
    url = self._CO_API_URL + '/identifiers/' + str(identifier_id) + '.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()
