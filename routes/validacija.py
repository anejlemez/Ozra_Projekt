from flask import Blueprint, jsonify
from services.validacija_service import *

validacija_bp = Blueprint("validacija", __name__)

@validacija_bp.route("/validacija/nepopolni", methods=["GET"])
def nepopolni():
    return jsonify(get_nepopolni_service())

@validacija_bp.route("/validacija/duplikati", methods=["GET"])
def duplikati():
    return jsonify(get_duplikati_service())