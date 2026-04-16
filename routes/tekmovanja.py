from flask import Blueprint, jsonify
from services.tekmovanja_service import (
    get_all_tekmovanja_service,
    get_one_tekmovanje_service,
    get_rezultati_za_tekmovanje_service
)

tekmovanja_bp = Blueprint("tekmovanja", __name__)

@tekmovanja_bp.route("/tekmovanja", methods=["GET"])
def get_tekmovanja():
    data = get_all_tekmovanja_service()
    return jsonify(data)

@tekmovanja_bp.route("/tekmovanja/<int:tekmovanje_id>", methods=["GET"])
def get_one_tekmovanje(tekmovanje_id):
    return jsonify(get_one_tekmovanje_service(tekmovanje_id))

@tekmovanja_bp.route("/tekmovanja/<int:tekmovanje_id>/rezultati", methods=["GET"])
def get_rezultati_tekmovanja(tekmovanje_id):
    data = get_rezultati_za_tekmovanje_service(tekmovanje_id)
    return jsonify(data)