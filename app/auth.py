"""
API Authentication Middleware.
Provides a simple decorator to protect REST endpoints using an X-API-Key.
"""

"""
API key authentication middleware.
"""

import os
from functools import wraps
from flask import request, jsonify

API_KEY = os.environ.get("API_KEY", "dev-secret-key-change-in-prod")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            #Returns 401 Unauthorized if the key is missing or incorrect.
            return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401
        return f(*args, **kwargs)
    return decorated