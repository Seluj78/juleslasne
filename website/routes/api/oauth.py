"""
    Source of juleslasne.com/.net/.me/.fr
    Copyright (C) 2018-2019 Jules Lasne - <jules@juleslasne.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import time
import os

from datetime import datetime, timedelta

from flask import request

from flask_jwt_extended import create_access_token

import jwt

from website import application

from website.errors.badrequest import BadRequestError
from website.errors.unauthorized import UnauthorizedError
from website.errors.notfound import NotFoundError

from website.models.api_users import get_apiuser, ApiUser

from website.success.new_token import SuccessNewToken
from website.success.token_info import SuccessTokenInfo

from website.utils.string import convert_dict


def generate_access_token(uuid: str, scope: str) -> str:
    """
    Generates a new token from a uuid and a scope

    :param uuid: The user's uuid (uuid4)
    :param scope: The user's access scope

    :return: Returns the new access token
    """

    payload = {
        # The uuid of the user.
        'uuid': uuid,
        # The issued_at notice.
        'iat': datetime.utcnow(),
        # The expire date and time.
        'exp': datetime.utcnow() + timedelta(minutes=120),  # each token expires after two hours
        # The issuer notice.
        'iss': 'jl:server',
        # The scope the user cas access with this token.
        'scope': scope
    }
    # Create and encode the token with all the info contained in the payload
    access_token = create_access_token(
        identity=payload,
        fresh=timedelta(minutes=120),
        expires_delta=timedelta(minutes=120)
    )
    return access_token


def check_sent_data(data):
    """
    This function checks the request form sent by the user when they want to generate a token.

    :param data: The dict containing the needed info for the token to be tested.

    :return: Returns nothing if successful, otherwise raises an appropriate error.
    """

    # The required keys inside the dict.
    req_keys = ['uuid', 'client_secret', 'grant_type']

    for key in req_keys:
        # If one is missing, throw an error
        if key not in data.keys():
            raise BadRequestError(
                "Missing {} in request for /oauth/token.".format(key),
                "To generate a token, you need to supply {}.".format(req_keys)
            )

    # Check if the grant type is set correctly
    if data['grant_type'] != 'client_credentials':
        raise BadRequestError(
            "`grant_type` should be set to `client_credentials`",
            "Set `grant_type` to `client_credentials`"
        )

    # Check if uuid is not empty
    if data['uuid'] is None or data['uuid'] == "":
        raise BadRequestError(
            "`uuid` should not be empty",
            "Set `uuid` with your uuid"
        )

    # Check if client_secret is not empty
    if data['client_secret'] is None or data['client_secret'] == "":
        raise BadRequestError(
            "`client_secret` should not be empty",
            "Set `client_secret` with your client_secret."
        )


def check_id_secret(data):
    """
    Checks the uuid and the secret to see if they match
    :param data: The data containing the uuid and secret
    :return: Returns nothing if ok, raise an error otherwise
    """

    # Get the apiuser object
    apiuser = get_apiuser(data['uuid'])
    # If the apiuser's secret isn't the same than the one in data
    if apiuser.secret != data['client_secret']:
        raise BadRequestError(
            "Can't generate oauth token: `client_secret` {} not found for `uuid` {}.".format(data['client_secret'],
                                                                                                  data['uuid']),
            "Check the `client_secret` and try again"
        )


@application.route('/oauth/token', methods=['POST'])
def generate_token():
    """
    This view is the one called by a apiuser when he wants to generate a token.

    :return: Returns a success message when the token is generated. An appropriate error is thrown otherwise.
    """

    # Get the data from the request
    data = request.form

    # Check the data sent by the apiuser
    check_sent_data(data)
    # Check if the id and secret sent by the apiuser are ok
    check_id_secret(data)
    # Create a payload containing all info required to generate the token

    apiuser = get_apiuser(data['uuid'])
    apiuser.access_count += 1
    apiuser.dt_last_access = datetime.utcnow()
    # Save the modified fields
    apiuser.save(only=[ApiUser.access_count, ApiUser.dt_last_access])

    # TODO: Store tokens ?
    access_token = generate_access_token(apiuser.uuid, apiuser.scope)
    return SuccessNewToken(
        "New token successfully generated for {}.".format(apiuser.name),
        access_token
    )


@application.route('/oauth/token/info', methods=['GET'])
def get_token_info():
    """
    This view is called when a user requests info on the token he's currently holding.

    :return: Returns all the info on the token after the token has been decoded successfully.
    Otherwise, throws the appropriate error.
    """

    # Decode and test the token given in the headers.
    payload = decode_and_test_token(request.headers)

    apiuser = get_apiuser(payload['uuid'])
    apiuser.access_count += 1
    apiuser.dt_last_access = datetime.utcnow()
    # Save the modified fields
    apiuser.save(only=[ApiUser.access_count, ApiUser.dt_last_access])

    # If the decode_and_test function hasn't returned any error, create a json with all the info contained in the token
    returned_json = {
        'uuid': payload['uuid'],
        'issued_at': payload['iat'],
        'expires_at': payload['exp'],
        'expires_in': payload['exp'] - int(time.time()),
        'scope': payload['scope']
    }
    # Return the json dict
    return SuccessTokenInfo("Token info issued", returned_json)


def decode_and_test_token(request_headers: dict):
    """
    This function will test and decode a given token. It will throw appropriate
    errors or return the payload contained inside the token.

    :param request_headers: The headers containing the token.

    :return: Returns the payload contained inside the token.
    """

    # Try to get the token from the headers. If not here, it will throw an Unauthorized error.
    try:
        user_token = str(request_headers['Authorization'].split(' ')[1])
    except KeyError:
        raise UnauthorizedError(
            "Missing oauth token in request header.",
            "You need to specify your token in the header as the "
            "authorization bearer."
        )
    # Try to decode the token.
    try:
        payload = jwt.decode(
            user_token,
            os.environ.get("FLASK_SECRET_KEY"),
            leeway=30,
            issuer='jl:server',
            algorithms='HS256'
        )
    # If the token is expired, throw an appropriate error.
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(
            "Unauthorized: Token expired.",
            "Please issue a new one at /oauth/token"
        )
    # If the token is malformed, throw an appropriate error.
    except jwt.DecodeError:
        raise BadRequestError(
            "Malformed token: {}.".format(user_token),
            "Check your token and try again"
        )

    # Check if the user who issued the payload is still present in DB. If not,
    # Throw an appropriate error.
    try:
        get_apiuser(payload['uuid'])
    except NotFoundError:
        raise NotFoundError(
            "The user who created this token doesn't exist anymore in the DB.",
            "Try again as another user"
        )
    # Return the payload (converted from unicode objects to strings.)
    return convert_dict(payload)