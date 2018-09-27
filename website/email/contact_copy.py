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

import datetime

from flask import render_template

# TODO: Add the preview_text


def copy_generate_html_email(email: str, text: str, name: str) -> str:
    """
    Generates the message copy email.

    :param email: The email of the sender
    :param text: The body of the message
    :param name: The name of the sender

    :return: Returns the generated copy of the message email in HTML form.
    """

    return render_template("email/contact_copy.html",
                           email=email,
                           text=text,
                           timestamp=datetime.datetime.utcnow(),
                           name=name,
                           email_title="Copy of the message sent from juleslasne.com"
                           )
