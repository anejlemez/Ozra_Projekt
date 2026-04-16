from flask import Blueprint, request, jsonify
from services.tekmovalci_service import *

tekmovalci_bp = Blueprint("tekmovalci", __name__)

@tekmovalci_bp.route("/tekmovalci/iskanje", methods=["GET"])
def search():
    ime = request.args.get("ime", "")
    return jsonify(search_tekmovalci_service(ime))

@tekmovalci_bp.route("/tekmovalci/<int:id>", methods=["GET"])
def get_one(id):
    return jsonify(get_tekmovalec_service(id))

@tekmovalci_bp.route("/tekmovalci/<int:id>/nastopi", methods=["GET"])
def nastopi(id):
    return jsonify(get_nastopi_service(id))

@tekmovalci_bp.route("/tekmovalci/<int:id>/najboljsi-cas", methods=["GET"])
def najboljsi(id):
    return jsonify(get_najboljsi_cas_service(id))