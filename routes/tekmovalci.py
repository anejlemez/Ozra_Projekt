from flask import Blueprint, request, jsonify
from services.tekmovalci_service import search_tekmovalci_service

tekmovalci_bp = Blueprint("tekmovalci", __name__)

@tekmovalci_bp.route("/tekmovalci/iskanje", methods=["GET"])
def search_tekmovalci():
    ime = request.args.get("ime", "")
    data = search_tekmovalci_service(ime)
    return jsonify(data)