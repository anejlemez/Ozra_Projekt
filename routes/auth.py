from flask import Blueprint, request, jsonify
from services.auth_service import login_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    return jsonify(login_service(request.json))