from flask import Blueprint, request, jsonify
from services.auth_service import login_admin_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    result = login_admin_service(data)
    return jsonify(result)