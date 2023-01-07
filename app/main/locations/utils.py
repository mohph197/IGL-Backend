from app.models import *
from flask import jsonify

def get_communes(wilaya):
    results = Location.query.filter_by(wilaya_name_ascii=wilaya).all()
    return jsonify([location.to_dict() for location in results]),200