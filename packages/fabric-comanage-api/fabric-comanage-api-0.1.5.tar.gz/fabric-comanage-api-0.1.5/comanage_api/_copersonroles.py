# comanage_api/_copersonroles.py

"""
CoPersonRole API - https://spaces.at.internet2.edu/display/COmanage/CoPersonRole+API

Methods
-------
coperson_roles_add(coperson_id: int, cou_id: int, status: str = None, affiliation: str = None) -> dict
    Add a new CO Person Role.
coperson_roles_delete(coperson_role_id: int) -> bool
    Remove a CO Person Role.
coperson_roles_edit(coperson_role_id: int, coperson_id: int = None, cou_id: int = None, status: str = None,
                   affiliation: str = None) -> bool
    Edit an existing CO Person Role.
coperson_roles_view_all() -> dict
    Retrieve all existing CO Person Roles.
coperson_roles_view_per_coperson(coperson_id: int) -> dict
    Retrieve all existing CO Person Roles for the specified CO Person. Available since Registry v2.0.0.
coperson_roles_view_per_cou(cou_id: int) -> dict
    Retrieve all existing CO Person Roles for the specified COU.
coperson_roles_view_one(coperson_role_id: int) -> dict
    Retrieve an existing CO Person Role.
"""

import json


def coperson_roles_add(self, coperson_id: int, cou_id: int, status: str = None, affiliation: str = None) -> dict:
    """
    Add a new CO Person Role.

    :param self:
    :param affiliation:
    :param coperson_id:
    :param cou_id:
    :param status:

    :return
        {
            "ResponseType":"NewObject",
            "Version":"1.0",
            "ObjectType":"CoPersonRole",
            "Id":"<ID>"
        }:

    Request Format
        {
          "RequestType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Person":
              {
                "Type":"CO",
                "Id":"<coperson_id>"
              },
              "CouId":"<cou_id>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|
                  "GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            }
          ]
        }

    Response Format
        HTTP Status             Response Body                       Description
        201 Added               NewObjectResponse with ObjectType   CoPersonRole created
        400 Bad Request                                             CoPersonRole Request not provided in POST body
        400 Invalid Fields      ErrorResponse with details in       An error in one or more provided fields
                                InvalidFields element
        401 Unauthorized                                            Authentication required
        403 COU Does Not Exist                                      The specified COU does not exist
        500 Other Error                                             Unknown error
    """
    post_body = {
        'RequestType': 'CoPersonRoles',
        'Version': '1.0',
        'CoPersonRoles': [
            {
                'Version': '1.0',
                'Person':
                    {
                        'Type': 'CO',
                        'Id': str(coperson_id)
                    },
                'CouId': str(cou_id),
                'O': str(self._CO_API_ORG_NAME)
            }
        ]
    }
    if status:
        if status not in self.STATUS_OPTIONS:
            raise TypeError("Invalid Fields 'status'")
        post_body['CoPersonRoles'][0]['Status'] = str(status)
    else:
        post_body['CoPersonRoles'][0]['Status'] = 'Active'
    if affiliation:
        affiliation = str(affiliation).lower()
        if affiliation not in self.AFFILIATION_OPTIONS:
            raise TypeError("Invalid Fields 'affiliation'")
        post_body['CoPersonRoles'][0]['Affiliation'] = str(affiliation)
    else:
        post_body['CoPersonRoles'][0]['Affiliation'] = 'member'
    post_body = json.dumps(post_body)
    url = self._CO_API_URL + '/co_person_roles.json'
    resp = self._s.post(
        url=url,
        data=post_body
    )
    if resp.status_code == 201:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coperson_roles_delete(self, coperson_role_id: int) -> bool:
    """
    Remove a CO Person Role.

    :param self:
    :param coperson_role_id:
    :return:

    Response Format
        HTTP Status                 Response Body       Description
        200 Deleted                                     CoPersonRole deleted
        400 Invalid Fields                              id not provided
        401 Unauthorized                                Authentication required
        404 CoPersonRole Unknown                        id not found
        500 Other Error                                 Unknown error
    """
    url = self._CO_API_URL + '/co_person_roles/' + str(coperson_role_id) + '.json'
    resp = self._s.delete(
        url=url
    )
    if resp.status_code == 200:
        return True
    else:
        resp.raise_for_status()


def coperson_roles_edit(self, coperson_role_id: int, coperson_id: int = None, cou_id: int = None, status: str = None,
                       affiliation: str = None) -> bool:
    """
    Edit an existing CO Person Role.

    :param self:
    :param coperson_role_id:
    :param affiliation:
    :param coperson_id:
    :param cou_id:
    :param status:

    :return:

    Request Format
        {
          "RequestType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Person":
              {
                "Type":"CO",
                "Id":"<coperson_id>"
              },
              "CouId":"<cou_id>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|
                  "GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            }
          ]
        }

    Response Format
        HTTP Status                 Response Body                       Description
        200 OK                                                          CoPersonRole updated
        400 Bad Request                                                 CoPersonRole Request not provided in POST body
        400 Invalid Fields          ErrorRespons with details in        An error in one or more provided fields
                                    InvalidFields element
        401 Unauthorized                                                Authentication required
        403 COU Does Not Exist                                          The specified COU does not exist
        404 CoPersonRole Unknown                                        id not found
        500 Other Error                                                 Unknown error
    """
    coperson_role = coperson_roles_view_one(self, coperson_role_id)
    post_body = {
        'RequestType': 'CoPersonRoles',
        'Version': '1.0',
        'CoPersonRoles': [
            {
                'Version': '1.0',
                'Person':
                    {
                        'Type': 'CO'
                    },
                'O': str(self._CO_API_ORG_NAME)
            }
        ]
    }
    if coperson_id:
        post_body['CoPersonRoles'][0]['Person']['Id'] = str(coperson_id)
    else:
        post_body['CoPersonRoles'][0]['Person']['Id'] = str(
            coperson_role.get('CoPersonRoles')[0].get('Person').get('Id'))
    if cou_id:
        post_body['CoPersonRoles'][0]['CouId'] = str(cou_id)
    else:
        post_body['CoPersonRoles'][0]['CouId'] = str(coperson_role.get('CoPersonRoles')[0].get('CouId'))
    if status:
        if status not in self.STATUS_OPTIONS:
            raise TypeError("Invalid Fields 'status'")
        post_body['CoPersonRoles'][0]['Status'] = str(status)
    else:
        post_body['CoPersonRoles'][0]['Status'] = coperson_role.get('CoPersonRoles')[0].get('Status')
    if affiliation:
        affiliation = str(affiliation).lower()
        if affiliation not in self.AFFILIATION_OPTIONS:
            raise TypeError("Invalid Fields 'affiliation'")
        post_body['CoPersonRoles'][0]['Affiliation'] = str(affiliation)
    else:
        post_body['CoPersonRoles'][0]['Affiliation'] = coperson_role.get('CoPersonRoles')[0].get('Affiliation')
    post_body = json.dumps(post_body)
    url = self._CO_API_URL + '/co_person_roles/' + str(coperson_role_id) + '.json'
    resp = self._s.put(
        url=url,
        data=post_body
    )
    if resp.status_code == 200:
        return True
    else:
        resp.raise_for_status()


def coperson_roles_view_all(self) -> dict:
    """
    Retrieve all existing CO Person Roles.

    :param self:
    :return
        {
          "ResponseType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Id":"<Id>",
              "Person":
              {
                "Type":"CO",
                "Id":"<ID>"
              },
              "CouId":"<CouId>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|"GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status             Response Body                       Description
        200 OK                  CoPersonRole Response               CoPersonRoles returned
        401 Unauthorized                                            Authentication required
        500 Other Error                                             Unknown error
    """
    url = self._CO_API_URL + '/co_person_roles.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coperson_roles_view_per_coperson(self, coperson_id: int) -> dict:
    """
    Retrieve all existing CO Person Roles for the specified CO Person. Available since Registry v2.0.0.

    :param self:
    :param coperson_id:
    :return
        {
          "ResponseType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Id":"<Id>",
              "Person":
              {
                "Type":"CO",
                "Id":"<ID>"
              },
              "CouId":"<CouId>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|"GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status             Response Body                       Description
        200 OK                  CoPersonRole Response               CoPersonRoles returned
        401 Unauthorized                                            Authentication required
        404 CO Person Unknown                                       id not found
        500 Other Error                                             Unknown error
    """
    url = self._CO_API_URL + '/co_person_roles.json'
    params = {'copersonid': int(coperson_id)}
    resp = self._s.get(
        url=url,
        params=params
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coperson_roles_view_per_cou(self, cou_id: int) -> dict:
    """
    Retrieve all existing CO Person Roles for the specified COU.

    :param self:
    :param cou_id:
    :return
        {
          "ResponseType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Id":"<Id>",
              "Person":
              {
                "Type":"CO",
                "Id":"<ID>"
              },
              "CouId":"<CouId>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|"GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status             Response Body                       Description
        200 OK                  CoPersonRole Response               CoPersonRoles returned
        401 Unauthorized                                            Authentication required
        404 COU Unknown                                             id not found
        500 Other Error                                             Unknown error
    """
    url = self._CO_API_URL + '/co_person_roles.json'
    params = {'couid': int(cou_id)}
    resp = self._s.get(
        url=url,
        params=params
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()


def coperson_roles_view_one(self, coperson_role_id: int) -> dict:
    """
    Retrieve an existing CO Person Role.

    :param self:
    :param coperson_role_id:
    :return
        {
          "ResponseType":"CoPersonRoles",
          "Version":"1.0",
          "CoPersonRoles":
          [
            {
              "Version":"1.0",
              "Id":"<Id>",
              "Person":
              {
                "Type":"CO",
                "Id":"<ID>"
              },
              "CouId":"<CouId>",
              "Affiliation":"<Affiliation>",
              "Title":"<Title>",
              "O":"<O>",
              "Ordr":"<Order>",
              "Ou":"<Ou>",
              "Status":("Active"|"Approved"|"Confirmed"|"Declined"|"Deleted"|"Denied"|"Duplicate"|"Expired"|"GracePeriod"|"Invited"|"Pending"|"PendingApproval"|"PendingConfirmation"|"Suspended"),
              "ValidFrom":"<ValidFrom>",
              "ValidThrough":"<ValidThrough>",
              "Created":"<CreateTime>",
              "Modified":"<ModTime>",
              "ExtendedAttributes":
              {
                "<Attribute>":"<Value>",
                {...}
              }
            },
            {...}
          ]
        }:

    Response Format
        HTTP Status                 Response Body                       Description
        200 OK                      CoPersonRole Response               CoPersonRoles returned
        401 Unauthorized                                                Authentication required
        404 CoPersonRole Unknown                                        id not found
        500 Other Error                                                 Unknown error
    """
    url = self._CO_API_URL + '/co_person_roles/' + str(coperson_role_id) + '.json'
    resp = self._s.get(
        url=url
    )
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        resp.raise_for_status()
