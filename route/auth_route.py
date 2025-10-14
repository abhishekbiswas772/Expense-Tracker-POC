from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from service.auth_service import AuthManager


auth_blp = Blueprint("Auth", __name__, description="Auth Routes")
auth_service = AuthManager()


@auth_blp.route("/api/v1/login")
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
            return jsonify({"status": True, "data": result.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": False, "error": str(e)}), 400


@auth_blp.route("/api/v1/signup")
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
