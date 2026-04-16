from flask import Blueprint, request, jsonify
from services.rezultati_service import (
    create_rezultat_service,
    update_rezultat_service,
    delete_rezultat_service
)

rezultati_bp = Blueprint("rezultati", __name__)

@rezultati_bp.route("/rezultati", methods=["POST"])
def create_rezultat():
    data = request.get_json()
    result = create_rezultat_service(data)
    return jsonify(result), 201

@rezultati_bp.route("/rezultati/<int:rezultat_id>", methods=["PUT"])
def update_rezultat(rezultat_id):
    data = request.get_json()
    result = update_rezultat_service(rezultat_id, data)
    return jsonify(result)

@rezultati_bp.route("/rezultati/<int:rezultat_id>", methods=["DELETE"])
def delete_rezultat(rezultat_id):
    result = delete_rezultat_service(rezultat_id)
    return jsonify(result)