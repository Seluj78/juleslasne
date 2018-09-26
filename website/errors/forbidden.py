# -*- coding: utf-8 -*-

"""
    The OpenApprentice Foundation and its website OpenApprentice.org
    Copyright (C) 2018 The OpenApprentice Foundation - contact@openapprentice.org

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

    @apiDefine error403

    @apiError (Error 403) {String} name        Error name
    @apiError (Error 403) {String} message     Error description
    @apiError (Error 403) {String} solution    Error solution
    @apiError (Error 403) {String} status_code HTTP status code

    @apiErrorExample {json} Error 403 JSON
         HTTP/1.1 403 Forbidden Error

         {
             "name": "Forbidden Error",
             "message": "The server refused to execute what you wanted.",
             "solution": "Logging in will not fix the issue. Please contact the administrator if this is a bug.",
             "status_code": 403
         }
"""

from website import application
from website.errors.template import generate_error_json


class ForbiddenError(Exception):
    """
    This is the ForbiddenError class for the Exception.
    """
    def __init__(self, msg: str, solution: str) -> None:
        self.name = "Forbidden Error"
        self.msg = msg
        self.solution = solution
        self.status_code = 403
    pass


@application.errorhandler(ForbiddenError)
def generate_forbidden(error: ForbiddenError) -> dict:
    """
    This is the 403 response creator. It will create a 403 response along with
    a custom message and the 403 code

    :param error: The error body
    :return: Returns the response formatted
    """

    return generate_error_json(error, 403)
