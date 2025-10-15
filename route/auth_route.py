from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from service.auth_service import AuthManager
from dotenv import load_dotenv
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt, get_jwt_identity, 
    jwt_required
)
import os

load_dotenv()

auth_blp = Blueprint("Auth", __name__, description="Auth Routes")
auth_service = AuthManager()

api_version = os.getenv("CURRENT_API_VERSION", "/api/v1")
BLOCKLIST = set()

@auth_blp.route(f"{api_version}/refresh-token", methods = ["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"access_token": new_token}, 200


@auth_blp.route(f"{api_version}/login")
class UserLoginRoute(MethodView):
    def post(self):
        user_data = request.get_json() or {}
        password = user_data.get("password")
        email = user_data.get("email")

        if not email:
            return jsonify({"status": False, "error": "email not found"}), 400
        if not password:
            return jsonify({"status": False, "error": "password not found"}), 400

        try:
            result = auth_service.login_user(password=password, email=email)
            access_token = create_access_token(identity=str(result.email), fresh=True)
            refresh_token = create_refresh_token(result.email)
            return jsonify({
                "status": True, 
                "data": result.to_dict(), 
                "access_token": access_token, 
                "refresh_token": refresh_token
            }), 200
        except Exception as e:
            return jsonify({"status": False, "error": str(e)}), 400


@auth_blp.route(f"{api_version}/signup")
class UserSignupRoute(MethodView):
    def post(self):
        user_data = request.get_json() or {}

        username = user_data.get("username")
        password = user_data.get("password")
        email = user_data.get("email")

        if not username:
            return jsonify({"status": False, "error": "username not found"}), 400
        if not password:
            return jsonify({"status": False, "error": "password not found"}), 400
        if not email:
            return jsonify({"status": False, "error": "email not found"}), 400

        try:
            result = auth_service.create_user(username=username, email=email, password=password)
            return jsonify({"status": True, "data": result.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": False, "error": str(e)}), 400
