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

    This file contains the app.run() necessary to test the application.
"""

import os
import logging

from website import application


def setup_logging():
    """
    Defines the logging configuration and prints a logging start message.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%d-%m-%Y:%H:%M:%S')

    logging.info("************************************************************")
    logging.info("*********Starting new instance of juleslasne.com************")
    logging.info("************************************************************")


if __name__ == '__main__':
    # Get the port defined in env if defined, otherwise sets it to 5000
    port = int(os.environ.get('FLASK_PORT', '5000'))
    # Default debug is true
    debug = True
    # Sets up the logging
    setup_logging()
    # Runs the main loop
    application.run(host='127.0.0.1', port=port, debug=debug)
