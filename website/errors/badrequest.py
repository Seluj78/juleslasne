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


class BadRequestError(Exception):
    """
    This is the BadRequestError class for the Exception.
    """
    def __init__(self, msg: str, solution: str) -> None:
        self.name = "Bad Request"
        self.msg = msg
        self.solution = solution
        self.status_code = 400
    pass


@application.errorhandler(BadRequestError)
def generate_badrequest(error: BadRequestError) -> dict:
    """
    This is the 400 response creator. It will create a 400 response along with
    a custom message and the 400 code

    :param error: The error body
    :return: Returns the response formatted
    """
    return generate_error_json(error, 400)


"""
    @apiDefine error400

    @apiError (Error 400) {String} name        Error name
    @apiError (Error 400) {String} message     Error description
    @apiError (Error 400) {String} solution    Error solution
    @apiError (Error 400) {String} status_code HTTP status code

    @apiErrorExample {json} Error 400 JSON
         HTTP/1.1 400 Bad request

         {
             "name": "Bad Request",
             "message": "The server couldn't understand your request based on the data sent",
             "solution": "Please check the data and try again.",
             "status_code": 400
         }
"""
"""
    @apiDefine error400malformedjson

    @apiError (Error 400) {String} name        Error name
    @apiError (Error 400) {String} message     Error description
    @apiError (Error 400) {String} solution    Error solution
    @apiError (Error 400) {String} status_code HTTP status code

    @apiErrorExample {json} Error 400 Malformed JSON
         HTTP/1.1 400 Bad request

         {
             "name": "Bad Request",
             "message": "The JSON Body is malformed.",
             "solution": "Please check the JSON data and try again.",
             "status_code": 400
         }
"""
"""
    @apiDefine error400emptyjson

    @apiError (Error 400) {String} name        Error name
    @apiError (Error 400) {String} message     Error description
    @apiError (Error 400) {String} solution    Error solution
    @apiError (Error 400) {String} status_code HTTP status code

    @apiErrorExample {json} Error 400 Empty JSON
         HTTP/1.1 400 Bad request

         {
             "name": "Bad Request",
             "message": "The JSON Body is empty.",
             "solution": "Please check the JSON data and try again.",
             "status_code": 400
         }

"""
