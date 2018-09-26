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
"""

from website import application
from website.errors.template import generate_error_json


class NotFoundError(Exception):
    """
    This is the NotFoundError class for the Exception.
    """
    def __init__(self, msg: str, solution: str) -> None:
        self.name = "Not Found Error"
        self.msg = msg
        self.solution = solution
        self.status_code = 404
    pass


@application.errorhandler(NotFoundError)
def generate_notfound(error: NotFoundError) -> dict:
    """
    This is the 404 response creator. It will create a 404 response with
    a custom message and the 404 code.

    :param error: The error body
    :return: Returns the response formatted
    """

    return generate_error_json(error, 404)


"""
    @apiDefine error404

    @apiError (Error 404) {String} name        Error name
    @apiError (Error 404) {String} message     Error description
    @apiError (Error 404) {String} solution    Error solution
    @apiError (Error 404) {String} status_code HTTP status code

    @apiErrorExample {json} Error 404 JSON
         HTTP/1.1 404 Not Found Error

         {
             "name": "Not Found Error",
             "message": "The resource you asked for could not be found",
             "solution": "Please check your syntax and try again.",
             "status_code": 404
         }
"""
"""
    @apiDefine error404noproject

    @apiError (Error 404) {String} name        Error name
    @apiError (Error 404) {String} message     Error description
    @apiError (Error 404) {String} solution    Error solution
    @apiError (Error 404) {String} status_code HTTP status code

    @apiErrorExample {json} Error 404 JSON Not Found
         HTTP/1.1 404 Not Found Error

         {
             "name": "Not Found Error",
             "message": "The project requested doesn't exist.",
             "solution": "Please check your syntax and try again.",
             "status_code": 404
         }
"""
