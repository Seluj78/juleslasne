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

import uuid
import datetime
import os

from binascii import hexlify

from peewee import CharField, DateTimeField, TextField, IntegerField, Model, DoesNotExist

from website import jl_db
from website.utils.string import decode_bytes
from website.errors import notfound


class ApiUser(Model):
    """
    This is the ApiUser model used in the DB
    """
    # TODO: Add a bool field called `can_track`
    # Where users, if they click on the link when receiving their codes choose to opt out of me tracking their number
    #  of times they accessed the api and the last time they did

    uuid = CharField(
        primary_key=True,
        default=str(uuid.uuid4()),
        help_text="The user's unique identifier",
        verbose_name="Unique Identifier"
    )
    name = CharField(
        help_text="The ApiUser's name",
        verbose_name="ApiUser Name"
    )
    email = CharField(
        help_text="The ApiUser's email",
        verbose_name="ApiUser Email"
    )
    reason = TextField(
        help_text="The ApiUser's reason",
        verbose_name="ApiUser Reason"
    )
    secret = CharField(
        help_text="ApiUser's secret key used to access the API",
        verbose_name="ApiUser Secret"
    )
    dt_created = DateTimeField(
        default=datetime.datetime.utcnow(),
        help_text="When the ApiUser was created",
        verbose_name="Date Created"
    )
    dt_last_access = DateTimeField(
        default=datetime.datetime.utcnow(),
        help_text="When the ApiUser last accessed the API",
        verbose_name="Date of Last Access"
    )
    access_count = IntegerField(
        default=0,
        help_text="Number of times the user accessed the API",
        verbose_name="Access Count"
    )
    scope = CharField(
        default="user",
        help_text="Scope/access level of ApiUser",
        verbose_name="ApiUser Scope"
    )

    class Meta:
        """
        This model uses the "jl_db.db" database.
        """
        database = jl_db  # type: ignore


def create_apiuser(name: str, email: str, reason: str) -> ApiUser:
    """
    Creates a new ApiUser object and adds it to the DB.

    :param name: The name of the ApiUser to be added
    :param email: The email of the ApiUser
    :param reason: The reason of the ApiUser

    :return: Returns the newly created ApiUser object
    """

    return ApiUser.create(
        name=name,
        email=email,
        reason=reason,
        secret=decode_bytes(hexlify(os.urandom(16)))
    )


def get_apiuser(identifier: str) -> ApiUser:
    """
    Will get a ApiUser from it's name or uuid, or raise a NotFound error.

    :param identifier: The email or uuid of the ApiUser to be fetched

    :return: Will return the fetched ApiUser, otherwise will raise a NotFound error.
    """

    not_found = 0
    found_user = ApiUser()  # Done to shush mypy

    try:
        user = ApiUser.get(ApiUser.uuid == decode_bytes(identifier))
    except DoesNotExist:
        not_found += 1
    else:
        found_user = user
    try:
        user = ApiUser.get(ApiUser.name == identifier)
    except DoesNotExist:
        not_found += 1
    else:
        found_user = user

    if not_found == 2:
        raise notfound.NotFoundError(
            "ApiUser {} not found.".format(identifier),
            "Check the identifier given and try again."
        )
    return found_user


def apiuser_to_dict(user: ApiUser) -> dict:
    """
    Converts a ApiUser object to a dict

    :param user: The ApiUser to convert

    :return: Returns a dict containing all the info on a ApiUser
    """

    output = dict()
    output['uuid'] = user.uuid
    output['name'] = user.name
    output['email'] = user.email
    output['reason'] = user.reason
    output['secret'] = user.secret
    output['dt_created'] = user.dt_created.strftime("%Y-%m-%d %H:%M:%S")
    output['dt_last_access'] = user.dt_last_access.strftime("%Y-%m-%d %H:%M:%S")
    output['access_count'] = user.access_count
    return output
