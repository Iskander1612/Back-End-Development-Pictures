from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item['id'] == id), None)
    if picture is None:
        abort(404)
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not isinstance(picture, dict) or not isinstance(picture.get('id'), int):
        return jsonify(message='A picture with an integer id is required'), 400
    if any(item['id'] == picture['id'] for item in data):
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302
    data.append(picture.copy())
    response = jsonify(picture)
    response.status_code = 201
    response.headers['Location'] = url_for('get_picture_by_id', id=picture['id'])
    return response

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    index = next((i for i, item in enumerate(data) if item['id'] == id), None)
    if index is None:
        abort(404)
    picture = request.get_json()
    if not isinstance(picture, dict):
        return jsonify(message='A picture object is required'), 400
    if 'id' in picture and picture['id'] != id:
        return jsonify(message='Picture id must match the URL'), 400
    data[index] = {**data[index], **picture, 'id': id}
    return jsonify(data[index]), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    index = next((i for i, item in enumerate(data) if item['id'] == id), None)
    if index is None:
        abort(404)
    data.pop(index)
    return '', 204
