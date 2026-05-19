from flask import Blueprint, jsonify
from services.spremembe_service import get_all_spremembe_service

spremembe_bp = Blueprint("spremembe", __name__)


@spremembe_bp.route("/spremembe", methods=["GET"])
def get_all():
    return jsonify(get_all_spremembe_service())