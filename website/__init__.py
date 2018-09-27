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

import os

from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager

import peewee

# TODO: Change developement key when in live server. Check if running in wsgi and if yes then ask for new dev key

if os.environ.get("FLASK_ENV", None) == "development":
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['FLASK_SECRET_KEY'] = "ThisIsADevelopmentKey"

if "FLASK_DEBUG" not in os.environ:
    raise EnvironmentError("Debug bool is not set in the server's environment. Please fix and restart the server.")

if "FLASK_SECRET_KEY" not in os.environ:
    raise EnvironmentError("Secret key is not set in the server's environment. Please fix and restart the server.")

if "JL_NOREPLY_PASSWORD" not in os.environ:
    raise EnvironmentError("noreply@juleslasne.com's password is not set in the server's environment.")

if "JL_DB_USER" not in os.environ:
    raise EnvironmentError("JL_DB_USER should be set with the user used to access the DB")

if "JL_DB_PASSWORD" not in os.environ:
    raise EnvironmentError("JL_DB_PASSWORD should be set with the password used to access the DB")


application = Flask(__name__)
application.debug = os.environ.get("FLASK_DEBUG", 1)
application.secret_key = os.environ.get("FLASK_SECRET_KEY", "ThisIsADevelopmentKey")


# Email configuration
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USERNAME'] = 'jules@juleslasne.com'
application.config['MAIL_PASSWORD'] = os.environ.get("JL_NOREPLY_PASSWORD")
application.config['MAIL_DEFAULT_SENDER'] = 'noreply@juleslasne.com'
mail = Mail(application)

jl_db = peewee.MySQLDatabase(
    "juleslasne",
    password=os.environ.get("JL_DB_PASSWORD", None),
    user=os.environ.get("JL_DB_USER", None)
)

application.config['JWT_SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
jwt = JWTManager(application)

# TODO: Send an email when tables are created, as a warning.
from website.models.projects import Project
from website.models.api_users import ApiUser

if not Project.table_exists():
    Project.create_table()

if not ApiUser.table_exists():
    ApiUser.create_table()


from website.routes.views.home import home_bp

application.register_blueprint(home_bp)

from website.routes.api import projects
from website.routes.api import oauth


# TODO: Add a new entry in the error classes to put a link to the doc