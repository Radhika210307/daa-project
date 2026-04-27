from flask import Blueprint, request, jsonify
from models.delivery import DeliveryRequest
from services import sorting_service
from utils.data_generator import generate_deliveries

sorting_bp = Blueprint("sorting", __name__, url_prefix="/sorting")


@sorting_bp.route("/prioritize", methods=["POST"])
def prioritize():
    body = request.get_json(silent=True) or {}
    raw = body.get("deliveries")

    if raw:
        deliveries = [DeliveryRequest.from_dict(d) for d in raw]
    else:
        n = int(body.get("count", 10))
        deliveries = generate_deliveries(n)

    result = sorting_service.prioritize(deliveries)
    return jsonify({"status": "ok", "result": result})
