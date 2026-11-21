from flask import Blueprint, Flask, Response, jsonify, request


def create_app() -> Flask:
    """Create an isolated Flask app with /health, /api/items Blueprint, and JSON 404 handler."""
    app = Flask(__name__)
    store: dict[int, dict[str, object]] = {}
    next_id = 1

    @app.get("/health")
    def health() -> tuple[Response, int]:
        return jsonify({"status": "ok"}), 200

    items_bp = Blueprint("items", __name__, url_prefix="/api/items")

    @items_bp.get("")
    def list_items() -> tuple[Response, int]:
        return jsonify({"items": list(store.values())}), 200

    @items_bp.post("")
    def create_item() -> tuple[Response, int]:
        nonlocal next_id
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "JSON object required"}), 400

        name = payload.get("name")
        qty = payload.get("qty")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "name must be a non-empty string"}), 400
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            return jsonify({"error": "qty must be a positive integer"}), 400

        item: dict[str, object] = {"id": next_id, "name": name.strip(), "qty": qty}
        store[next_id] = item
        next_id += 1
        return jsonify(item), 201

    @items_bp.get("/<int:item_id>")
    def get_item(item_id: int) -> tuple[Response, int]:
        item = store.get(item_id)
        if item is None:
            return jsonify({"error": "item not found"}), 404
        return jsonify(item), 200

    app.register_blueprint(items_bp)

    @app.errorhandler(404)
    def handle_404(_err: Exception) -> tuple[Response, int]:
        return jsonify({"error": "not found"}), 404

    return app
