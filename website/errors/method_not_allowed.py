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

from flask import jsonify

from website import application


@application.errorhandler(405)
def method_not_allowed(e):
    """
    This will return an appropriate error when a method not allowed is raised.\\

    :param e: The error thrown

    :return: Will return the error in json form
    """

    error = {
        "message": "Sorry, but this method is not allowed on this endpoint.",
        "solution": "Try again with another method or contact the administrator if this is an error.",
        "status_code": 405,
        "success": False,
        "name": e.__class__.__name__,
    }

    return jsonify(error), 405
