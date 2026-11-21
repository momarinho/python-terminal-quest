## Concept: Python Web Frameworks — Flask vs. Django & Modular Blueprints

Python web backends traditionally split along two philosophies:

| Dimension | **Flask** (Micro-framework) | **Django** (Batteries-included) |
| :--- | :--- | :--- |
| Architecture | Minimal core (`Werkzeug` + `Jinja2`), bring your own ORM/auth | **MTV** (Model–Template–View) with built-in ORM, migrations & Admin |
| Modularity | `Blueprint` modules registered on an app factory | Reusable Django `apps` with `urls.py` & `models.py` |
| Best Fit | Focused APIs, microservices, custom ML wrappers | Full-stack CRUD platforms, admin portals, rapid relational apps |

*(Later in the curriculum, you'll also build async OpenAPI-first services with **FastAPI**!)*

### Flask App Factory & `Blueprint`
```python
from flask import Blueprint, Flask, jsonify

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")

@catalog_bp.get("/ping")
def ping():
    return jsonify({"pong": True}), 200

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(catalog_bp)
    return app
```

### Challenge
Implement `create_app()` in `flask_service.py` with:
* `GET /health` -> `200` `{"status": "ok"}`
* `items_bp` (`Blueprint` mounted at `/api/items`) with `GET /api/items`, `POST /api/items` (validating non-empty `name` and integer `qty > 0`, returning `201` or `400`), and `GET /api/items/<item_id>` (`200` or `404` JSON error).
* A `@app.errorhandler(404)` returning JSON `{"error": "not found"}` with status `404`.
