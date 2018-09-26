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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.\

"""

import json

from flask import request

from werkzeug.exceptions import BadRequest


from website import application
from website.models.projects import Project, project_to_dict, create_project, get_project
from website.errors.badrequest import BadRequestError
from website.success.created import SuccessCreated
from website.success.deleted import SuccessDeleted


@application.route("/projects", methods=['GET'])
def projects():
    # TODO: Include @apiPermission
    """
    @api {get} /projects Lists all projects

    @apiName GetProjects
    @apiGroup Projects

    @apiDescription This route will return all of the projects available.

    @apiExample {bash} CURL example
        curl -i https://juleslasne.com/projects

    @apiExample {py} Python example
        # Using requests module
        import requests
        # Make the request
        r = requests.get(url='https://juleslasne.com/projects')
        # Extract the data in json format to be used
        data = r.json()
        # ...

    @apiSuccess {Object}    list              List of all projects
    @apiSuccess {Number}    status              200

    @apiSuccessExample {json} Example successful response
        HTTP/1.1 200 OK
        [
            {
                "uuid": "0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d",
                "name": "TestProject",
                "description": "This is a test project which doesn't even exist in the DB",
                "date_added": "2018-01-1 00:00:00",
                "is_ongoing": false,
                "image_url": "https://www.gstatic.com/webp/gallery3/1.sm.png"
            },
            ...
        ]
    """

    output = []
    projs = Project.select()
    for project in projs:
        output.append(project_to_dict(project))

    response = application.response_class(
        response=json.dumps(output),
        status=200,
        mimetype='application/json'
    )
    return response


@application.route("/projects", methods=['POST'])
def project_create():
    """
    # TODO: Add checks if x entry is missing.
    @api {post} /projects Create a project

    @apiName CreateProject
    @apiGroup Projects

    @apiDescription This route create a new project

    @apiParam {String} name The new project's name.
    @apiParam {String} description The new project's description.
    @apiParam {Boolean} is_ongoing=false Is the project currently being worked on ?
    @apiParam {String} image_url=None The project's image url to represent it.

    @apiParamExample {json} JSON request body example
        {
            "name": "Test Project",
            "description": "Test Project's description",
            "is_ongoing": False,
            "image_url": "https://www.gstatic.com/webp/gallery3/1.sm.png"
        }

    @apiExample {bash} CURL example
        curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"name":"Test Project","description":"Test Project description", "is_ongoing": false, \
        "image_url": "https://www.gstatic.com/webp/gallery3/1.sm.png"}' \
        https://juleslasne.com/projects

    @apiExample {py} Python example
        # Using requests module
        import requests

        # Create the dict containing the project's info you will send
        project_info = {
            "name": "Test Project",
            "description": "Test Project's description",
            "is_ongoing": False,
            "image_url": "https://www.gstatic.com/webp/gallery3/1.sm.png"
        }

        # Make the request
        r = requests.get(url='https://juleslasne.com/projects')

        # Extract the data in json format to be used
        data = r.json()
        # ...

    @apiSuccess {Message} message New project PROJECT_NAME created.
    @apiSuccess {Status} status  201

    @apiSuccessExample {json} Example successful response
        HTTP/1.1 201 CREATED
        {
            "success": true,
            "message": "New project Test Project created.",
            "code": 201
        }

    @apiUse error400malformedjson
    @apiUse error400emptyjson
    """

    try:
        data = request.get_json()
    except BadRequest:
        raise BadRequestError(
            "The Json Body is malformatted",
            "Please check it and try again"
        )

    # If the data dict is empty
    if not data:
        raise BadRequestError(
            "Missing json body.",
            "Please fill the json body and try again"
        )

    create_project(
        data['name'],
        data['description'],
        data['is_ongoing'],
        data['image_url']
    )

    return SuccessCreated(
        "New project {} created".format(data['name'])
    )


@application.route("/projects/<uuid>", methods=['DELETE'])
def project_delete(uuid):
    """
    @api {delete} /projects/:uuid Delete a project

    @apiName DeleteProject
    @apiGroup Projects

    @apiDescription This route deletes a given project

    @apiParam {Number} uuid Project's unique ID.

    @apiParamExample {bash} CURL example
        curl -X "DELETE" https://juleslasne.com/projects/0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d

    @apiParamExample {py} Python example
        # Using requests module
        import requests

        project_uuid = "0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d"
        r = requests.delete(url='https://juleslasne.com/projects/' + project_uuid)

    @apiUse error404noproject

    @apiSuccess {Status} status  204
    """

    get_project(uuid).delete_instance()
    return SuccessDeleted(
        "Successfully deleted {}".format(uuid)
    )
