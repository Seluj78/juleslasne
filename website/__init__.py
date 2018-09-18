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

if "RECAPTCHA_SECRET_KEY" not in os.environ:
    raise EnvironmentError("RECAPTCHA_SECRET_KEY is not set in the server's environment.")

application = Flask(__name__)
application.debug = os.environ.get("FLASK_DEBUG", 1)
application.secret_key = os.environ.get("FLASK_SECRET_KEY", "ThisIsADevelopmentKey")


# Email configutation
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USERNAME'] = 'jules@juleslasne.com'
application.config['MAIL_PASSWORD'] = os.environ.get("JL_NOREPLY_PASSWORD")
application.config['MAIL_DEFAULT_SENDER'] = 'noreply@juleslasne.com'
mail = Mail(application)

from website.routes.views.home import home_bp

application.register_blueprint(home_bp)
