from flask import Blueprint, request, jsonify
from models.delivery import DeliveryRequest
from models.vehicle import Vehicle
from models.graph import Graph
from services import greedy_service, dp_service, pipeline_service
from utils.data_generator import generate_deliveries, generate_vehicles, generate_graph
from utils.performance import run_all as run_benchmarks

optimization_bp = Blueprint("optimization", __name__)


@optimization_bp.route("/greedy/assign", methods=["POST"])
def greedy_assign():
    body = request.get_json(silent=True) or {}
    raw = body.get("deliveries")
    deliveries = [DeliveryRequest.from_dict(d) for d in raw] if raw else generate_deliveries(int(body.get("count", 10)))
    capacity = float(body.get("capacity", 500))
    result = greedy_service.assign(deliveries, capacity=capacity)
    return jsonify({"status": "ok", "result": result})


@optimization_bp.route("/dp/optimize", methods=["POST"])
def dp_optimize():
    body = request.get_json(silent=True) or {}
    raw = body.get("deliveries")
    deliveries = [DeliveryRequest.from_dict(d) for d in raw] if raw else generate_deliveries(int(body.get("count", 10)))

    graph_data = body.get("graph")
    g = Graph.from_dict(graph_data) if graph_data else generate_graph(int(body.get("num_nodes", 10)))

    capacity = int(body.get("capacity", 100))
    src = int(body.get("src", 0))
    dst = int(body.get("dst", g.num_nodes - 1))

    result = dp_service.optimize(deliveries, g, capacity=capacity, src=src, dst=dst)
    return jsonify({"status": "ok", "result": result})


@optimization_bp.route("/pipeline/run", methods=["POST"])
def pipeline_run():
    body = request.get_json(silent=True) or {}
    raw = body.get("deliveries")
    n = int(body.get("count", 10))
    deliveries = [DeliveryRequest.from_dict(d) for d in raw] if raw else generate_deliveries(n)

    num_nodes = int(body.get("num_nodes", 10))
    graph_data = body.get("graph")
    g = Graph.from_dict(graph_data) if graph_data else generate_graph(num_nodes)

    v_count = int(body.get("vehicle_count", 3))
    vehicles = generate_vehicles(v_count)

    capacity = int(body.get("capacity", 100))
    result = pipeline_service.run_pipeline(deliveries, vehicles, g, capacity=capacity)
    return jsonify({"status": "ok", "result": result})


@optimization_bp.route("/benchmark", methods=["GET"])
def benchmark():
    result = run_benchmarks()
    return jsonify({"status": "ok", "result": result})
