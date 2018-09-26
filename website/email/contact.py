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

from website.email.contact_copy import copy_generate_html_email
from website.utils.email import send_email


def contact_generate_html_email(email: str, text: str, name: str) -> str:
    """
    Generates a contact email ("You've received a message from X")

    :param email: The email who sent it
    :param text: The body of the message
    :param name: The name of the sender

    :return: Returns the rendered HTML template
    """

    return render_template("email/contact.html",
                           email=email,
                           text=text,
                           timestamp=datetime.datetime.utcnow(),
                           name=name,
                           mail_title="New message received through juleslasne.com"
                           )


def contact_send_mail(email: str, text: str, name: str, send_copy=False) -> None:
    """
    Sends the new message email.

    :param email: The person who sent the email
    :param text: The body of the email
    :param name: The name of the person who sent the email
    :param send_copy: If true, send a copy to the sender.
    """

    html_email = contact_generate_html_email(
        email=email,
        text=text,
        name=name
    )
    send_email("noreply@juleslasne.com", "New message from {}".format(name), html_email)
    if send_copy:
        copy_email = copy_generate_html_email(
            email=email,
            text=text,
            name=name,
        )
        send_email(email, "Copy of the message sent to Jules Lasne", copy_email)
