define({ "api": [  {    "type": "post",    "url": "/projects",    "title": "Create a new project",    "name": "CreateProject",    "group": "Projects",    "description": "<p>This route create a new project</p>",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "name",            "description": "<p>The new project's name.</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "description",            "description": "<p>The new project's description.</p>"          },          {            "group": "Parameter",            "type": "Boolean",            "optional": false,            "field": "is_ongoing",            "defaultValue": "false",            "description": "<p>Is the project currently being worked on ?</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "image_url",            "defaultValue": "None",            "description": "<p>The project's image url to represent it.</p>"          }        ]      },      "examples": [        {          "title": "JSON request body example",          "content": "{\n    \"name\": \"Test Project\",\n    \"description\": \"Test Project's description\",\n    \"is_ongoing\": False,\n    \"image_url\": \"https://www.gstatic.com/webp/gallery3/1.sm.png\"\n}",          "type": "json"        }      ]    },    "examples": [      {        "title": "CURL example",        "content": "curl --header \"Content-Type: application/json\" \\\n--request POST \\\n--data '{\"name\":\"Test Project\",\"description\":\"Test Project description\", \"is_ongoing\": false, \\\n\"image_url\": \"https://www.gstatic.com/webp/gallery3/1.sm.png\"}' \\\nhttps://juleslasne.com/projects",        "type": "bash"      },      {        "title": "Python example",        "content": "# Using requests module\nimport requests\n\n# Create the dict containing the project's info you will send\nproject_info = {\n    \"name\": \"Test Project\",\n    \"description\": \"Test Project's description\",\n    \"is_ongoing\": False,\n    \"image_url\": \"https://www.gstatic.com/webp/gallery3/1.sm.png\"\n}\n\n# Make the request\nr = requests.get(url='https://juleslasne.com/projects')\n\n# Extract the data in json format to be used\ndata = r.json()\n# ...",        "type": "py"      }    ],    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "Message",            "optional": false,            "field": "message",            "description": "<p>New project PROJECT_NAME created.</p>"          },          {            "group": "Success 200",            "type": "Status",            "optional": false,            "field": "status",            "description": "<p>201</p>"          }        ]      },      "examples": [        {          "title": "Example successful response",          "content": "HTTP/1.1 201 CREATED\n{\n    \"success\": true,\n    \"message\": \"New project Test Project created.\",\n    \"code\": 201\n}",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "./website/routes/api/projects.py",    "groupTitle": "Projects",    "error": {      "fields": {        "Error 400": [          {            "group": "Error 400",            "type": "String",            "optional": false,            "field": "name",            "description": "<p>Error name</p>"          },          {            "group": "Error 400",            "type": "String",            "optional": false,            "field": "message",            "description": "<p>Error description</p>"          },          {            "group": "Error 400",            "type": "String",            "optional": false,            "field": "solution",            "description": "<p>Error solution</p>"          },          {            "group": "Error 400",            "type": "String",            "optional": false,            "field": "status_code",            "description": "<p>HTTP status code</p>"          }        ]      },      "examples": [        {          "title": "Error 400 Malformed JSON",          "content": "HTTP/1.1 400 Bad request\n\n{\n    \"name\": \"Bad Request\",\n    \"message\": \"The JSON Body is malformed.\",\n    \"solution\": \"Please check the JSON data and try again.\",\n    \"status_code\": 400\n}",          "type": "json"        },        {          "title": "Error 400 Empty JSON",          "content": "HTTP/1.1 400 Bad request\n\n{\n    \"name\": \"Bad Request\",\n    \"message\": \"The JSON Body is empty.\",\n    \"solution\": \"Please check the JSON data and try again.\",\n    \"status_code\": 400\n}",          "type": "json"        }      ]    }  },  {    "type": "delete",    "url": "/projects/:uuid",    "title": "Delete a project",    "name": "DeleteProject",    "group": "Projects",    "description": "<p>This route deletes a given project</p>",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "uuid",            "description": "<p>Project's unique ID.</p>"          }        ]      },      "examples": [        {          "title": "CURL example",          "content": "curl -X \"DELETE\" https://juleslasne.com/projects/0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d",          "type": "bash"        },        {          "title": "Python example",          "content": "# Using requests module\nimport requests\n\nproject_uuid = \"0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d\"\nr = requests.delete(url='https://juleslasne.com/projects/' + project_uuid)",          "type": "py"        }      ]    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "Status",            "optional": false,            "field": "status",            "description": "<p>204</p>"          }        ]      }    },    "version": "0.0.0",    "filename": "./website/routes/api/projects.py",    "groupTitle": "Projects",    "error": {      "fields": {        "Error 404": [          {            "group": "Error 404",            "type": "String",            "optional": false,            "field": "name",            "description": "<p>Error name</p>"          },          {            "group": "Error 404",            "type": "String",            "optional": false,            "field": "message",            "description": "<p>Error description</p>"          },          {            "group": "Error 404",            "type": "String",            "optional": false,            "field": "solution",            "description": "<p>Error solution</p>"          },          {            "group": "Error 404",            "type": "String",            "optional": false,            "field": "status_code",            "description": "<p>HTTP status code</p>"          }        ]      },      "examples": [        {          "title": "Error 404 JSON Not Found",          "content": "HTTP/1.1 404 Not Found Error\n\n{\n    \"name\": \"Not Found Error\",\n    \"message\": \"The project requested doesn't exist.\",\n    \"solution\": \"Please check your syntax and try again.\",\n    \"status_code\": 404\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/projects",    "title": "Lists all projects",    "name": "GetProjects",    "group": "Projects",    "description": "<p>This route will return all of the projects available.</p>",    "examples": [      {        "title": "CURL example",        "content": "curl -i https://juleslasne.com/projects",        "type": "bash"      },      {        "title": "Python example",        "content": "# Using requests module\nimport requests\n# Make the request\nr = requests.get(url='https://juleslasne.com/projects')\n# Extract the data in json format to be used\ndata = r.json()\n# ...",        "type": "py"      }    ],    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "Object",            "optional": false,            "field": "list",            "description": "<p>List of all projects</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "status",            "description": "<p>200</p>"          }        ]      },      "examples": [        {          "title": "Example successful response",          "content": "HTTP/1.1 200 OK\n[\n    {\n        \"uuid\": \"0cf1b4f7-6d87-476c-9a8f-6e3dcfe3bc7d\",\n        \"name\": \"TestProject\",\n        \"description\": \"This is a test project which doesn't even exist in the DB\",\n        \"date_added\": \"2018-01-1 00:00:00\",\n        \"is_ongoing\": false,\n        \"image_url\": \"https://www.gstatic.com/webp/gallery3/1.sm.png\"\n    },\n    ...\n]",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "./website/routes/api/projects.py",    "groupTitle": "Projects"  },  {    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "optional": false,            "field": "varname1",            "description": "<p>No type.</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "varname2",            "description": "<p>With type.</p>"          }        ]      }    },    "type": "",    "url": "",    "version": "0.0.0",    "filename": "./docs/main.js",    "group": "_Users_jlasne_juleslasne_docs_main_js",    "groupTitle": "_Users_jlasne_juleslasne_docs_main_js",    "name": ""  }] });
