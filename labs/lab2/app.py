from apispec import APISpec
from apispec_fromfile import FromFilePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from apispec_fromfile import from_file
from flask import Flask, json, jsonify
from flasgger import Swagger
from students.model import StudentSchema

spec = APISpec(
    title="SJSU Student Registration API",
    version="0.0.1",
    openapi_version="3.0.3",
    plugins=[
        # FromFilePlugin("resource"),
        FlaskPlugin(),
        MarshmallowPlugin()
    ],
)

app = Flask(__name__)
swagger = Swagger(app)  # localhost:5000/apidocs

# API endpoints

# @from_file("spec/api.yml")


@app.route("/")
def index():
    # return {"OK"}
    return jsonify({"foo": "bar"})

# @from_file("spec/api.yml")


@app.route("/spec")
def get_apispec():
    return jsonify(spec.to_dict())


@app.route("/students")
def get_students():
    """
    Get all SJSU students
    ---
    get:
        description: Get all students
        responses:
            200:
                content:
                    application/json:
                        schema: StudentSchema
    """
    # students = StudentSchema().dump()
    student = dict(first_name="Foo", last_name="Bar",
                   sjsu_id="12345", email="test@sjsu.edu")

    return StudentSchema().dump(student)


with app.test_request_context():
    spec.path(view=index)
    spec.path(view=get_students)
