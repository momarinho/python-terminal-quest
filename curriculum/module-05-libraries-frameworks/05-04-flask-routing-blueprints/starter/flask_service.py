from flask import Blueprint, Flask, jsonify, request


def create_app() -> Flask:
    """Create an isolated Flask app with /health, /api/items Blueprint, and JSON 404 handler."""
    app = Flask(__name__)
    _ = (Blueprint, jsonify, request)

    # TODO: mount GET /health, items_bp (/api/items), and @app.errorhandler(404)
    return app
