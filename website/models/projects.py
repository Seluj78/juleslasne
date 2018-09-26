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

import uuid
import datetime

from peewee import CharField, BooleanField, DateTimeField, TextField, Model, DoesNotExist

from website import jl_db
from website.utils.string import decode_bytes
from website.errors import notfound


class Project(Model):
    """
    This is the user model used in the DB
    """
    # Required:
    uuid = CharField(
        primary_key=True,
        default=str(uuid.uuid4()),
        help_text="The user's unique identifier",
        verbose_name="Unique Identifier"
    )
    name = CharField(
        help_text="The project's name",
        verbose_name="Project Name"
    )
    description = TextField(
        help_text="The project's description",
        verbose_name="Project's Description"
    )
    date_added = DateTimeField(
        default=datetime.datetime.utcnow(),
        help_text="When the project was added to this website",
        verbose_name="Date Added"
    )
    is_ongoing = BooleanField(
        help_text="Is the project ongoing ?",
        verbose_name="Project Ongoing"
    )
    # Can't upload images yet so when creating a new project it will have to be given a link
    image_url = TextField(
        help_text="The project's image link",
        verbose_name="Image URL"
    )

    class Meta:
        """
        This model uses the "jl_db.db" database.
        """
        database = jl_db  # type: ignore


def create_project(name, description, is_ongoing, image_url=None):

    if not image_url:
        image_url = \
            "https://s3.pixers.pics/pixers/700/FO/13/98/82/33/700_FO13988233_8ddc36e94d8ca57cc55441763480390f.jpg"

    return Project.create(
        uuid=str(uuid.uuid4()),
        name=name,
        description=description,
        is_ongoing=is_ongoing,
        image_url=image_url
    )


def get_project(identifier):
    not_found = 0
    found_project = None

    try:
        project = Project.get(Project.uuid == decode_bytes(identifier))
    except DoesNotExist:
        not_found += 1
    else:
        found_project = project
    try:
        project = Project.get(Project.name == identifier)
    except DoesNotExist:
        not_found += 1
    else:
        found_project = project

    if not_found == 2:
        raise notfound.NotFoundError(
            "Project {} not found.".format(identifier),
            "Check the identifier given and try again."
        )
    return found_project


def get_project_dict(project):
    output = dict()
    output['uuid'] = project.uuid
    output['name'] = project.name
    output['description'] = project.description
    output['date_added'] = project.date_added.strftime("%Y-%m-%d %H:%M:%S")
    output['is_ongoing'] = project.is_ongoing
    output['image_url'] = project.image_url
    return output
