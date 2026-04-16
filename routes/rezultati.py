from flask import Blueprint, request, jsonify
from services.rezultati_service import *

rezultati_bp = Blueprint("rezultati", __name__)

@rezultati_bp.route("/rezultati", methods=["POST"])
def create():
    return jsonify(create_rezultat_service(request.json)), 201

@rezultati_bp.route("/rezultati/<int:id>", methods=["GET"])
def get_one(id):
    return jsonify(get_rezultat_service(id))

@rezultati_bp.route("/rezultati/<int:id>", methods=["PUT"])
def update(id):
    return jsonify(update_rezultat_service(id, request.json))

@rezultati_bp.route("/rezultati/<int:id>", methods=["DELETE"])
def delete(id):
    return jsonify(delete_rezultat_service(id))