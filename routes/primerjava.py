from flask import Blueprint, request, jsonify
from services.primerjava_service import primerjava_service

primerjava_bp = Blueprint("primerjava", __name__)

@primerjava_bp.route("/primerjava", methods=["GET"])
def primerjava():
    t1 = request.args.get("tekmovalec1")
    t2 = request.args.get("tekmovalec2")
    return jsonify(primerjava_service(t1, t2))