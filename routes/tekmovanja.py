from flask import Blueprint, jsonify
from services.tekmovanja_service import *

tekmovanja_bp = Blueprint("tekmovanja", __name__)

@tekmovanja_bp.route("/tekmovanja", methods=["GET"])
def get_all():
    return jsonify(get_all_tekmovanja_service())

@tekmovanja_bp.route("/tekmovanja/<int:id>", methods=["GET"])
def get_one(id):
    return jsonify(get_one_tekmovanje_service(id))

@tekmovanja_bp.route("/tekmovanja/<int:id>/rezultati", methods=["GET"])
def get_rezultati(id):
    return jsonify(get_rezultati_tekmovanja_service(id))