# /update endpoint logic
from flask import Blueprint, request, jsonify
from datetime import datetime

from utils.regex_utils import extract_shipment_fields
from models.shipment_schema import build_shipment_payload
from services.forward_service import forward_shipment_data

shipment_bp = Blueprint("shipment",__name__)

@shipment_bp.route("/update",methods=["POST"])
def update_shipment():
    data=request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"status":"error","message":"Missing 'message' field"}),400

    message = data["message"]
    if not isinstance(message,str) or not message.strip():
        return jsonify({"status":"error","message":"Message must be a non-empty string"}),400

    fields=extract_shipment_fields(message)

    order_id = fields["order_id"]
    shipment_id = fields["shipment_id"]
    delivery_date = fields["delivery_date"]

    if not order_id or not shipment_id or not delivery_date:
        return jsonify({"status": "error", "message": "Could not extract required shipment fields"}), 422
    
    try:
        datetime.strptime(delivery_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid delivery_date format"}), 422

    payload = build_shipment_payload(order_id, shipment_id, delivery_date, message)
    forward_result = forward_shipment_data(payload)

    return jsonify({
    "status": "success",
    "order_id": order_id,
    "shipment_id": shipment_id,
    "delivery_date": delivery_date,
    "forwarded": forward_result["forwarded"]
    }), 200