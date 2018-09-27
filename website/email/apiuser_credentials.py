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

from flask import render_template

from website.models.api_users import ApiUser
from website.utils.email import send_email
from website.statics import DOC_LINK


def apiuser_generate_new_credentials_email(name: str, uuid: str, secret: str) -> str:
    """
    Generates the message new ApiUser email.

    :param name: The name of the new ApiUser
    :param uuid: The uuid of the new ApiUser
    :param secret: The secret of the new ApiUser

    :return: Returns the generated email in HTML form.
    """

    return render_template("email/apiuser_credentials.html",
                           email_title="JulesLasne.com API Credentials",
                           name=name,
                           uuid=uuid,
                           secret=secret,
                           preview_text="Here are your credentials for JulesLasne.com!",
                           doc_link=DOC_LINK
                           )


def apiuser_send_credentials_email(new_apiuser: ApiUser) -> None:
    """
    Sends the new message email.

    :param new_apiuser: The newly added user
    """

    html_email = apiuser_generate_new_credentials_email(new_apiuser.name, new_apiuser.uuid, new_apiuser.secret)

    send_email(new_apiuser.email, "JulesLasne.com API Credentials", html_email)
