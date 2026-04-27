from flask import Blueprint, request, jsonify
from models.graph import Graph
from services import graph_service
from utils.data_generator import generate_graph

graph_bp = Blueprint("graph", __name__, url_prefix="/graph")


@graph_bp.route("/route", methods=["POST"])
def route():
    body = request.get_json(silent=True) or {}

    graph_data = body.get("graph")
    if graph_data:
        g = Graph.from_dict(graph_data)
    else:
        num_nodes = int(body.get("num_nodes", 10))
        g = generate_graph(num_nodes=num_nodes)

    src = int(body.get("src", 0))
    dst = int(body.get("dst", g.num_nodes - 1))

    result = graph_service.route(g, src, dst)
    result["graph"] = g.to_dict()
    return jsonify({"status": "ok", "result": result})
