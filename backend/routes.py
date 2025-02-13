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
    """Return all pictures in JSON format"""
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if not new_picture or "id" not in new_picture:
        return jsonify({"Message": "Invalid request data"}), 400
    
    if any(p["id"] == new_picture["id"] for p in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    response = jsonify(new_picture)
    response.status_code = 201
    response.headers["Content-Type"] = "application/json"  # <-- Agregado para cumplir los tests
    return response

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()

    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        picture.update(updated_picture)
        return jsonify(picture), 200
    
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        data.remove(picture)
        return '', 204
    
    return jsonify({"message": "Picture not found"}), 404
