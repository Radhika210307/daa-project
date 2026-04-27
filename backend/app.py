from flask import Flask, send_from_directory
from flask_cors import CORS
import os, sys

# Ensure backend root is on path
sys.path.insert(0, os.path.dirname(__file__))

from routes.sorting_routes import sorting_bp
from routes.graph_routes import graph_bp
from routes.optimization_routes import optimization_bp

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "../frontend/templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "../frontend/static"),
)
CORS(app)

app.register_blueprint(sorting_bp)
app.register_blueprint(graph_bp)
app.register_blueprint(optimization_bp)


@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index.html")


@app.route("/dashboard")
def dashboard():
    return send_from_directory(app.template_folder, "dashboard.html")


@app.route("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
