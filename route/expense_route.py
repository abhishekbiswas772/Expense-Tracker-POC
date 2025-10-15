from flask_smorest import Blueprint
from service.expense_service import ExpenseService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

expense_service = ExpenseService()

api_version = os.getenv("CURRENT_API_VERSION", "/api/v1")

expense_blp = Blueprint("Expense", __name__, description="Expense Service")

@expense_blp.route(f"{api_version}/filter-expense", methods = ["GET"])
@jwt_required()
def filter_expense():
    user_email = get_jwt_identity()
    expense_filter_category = request.args.get("filter_category")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    try:
        expenses = expense_service.filter_expense(
            user_email=user_email,
            expense_filter_category=expense_filter_category,
            from_date=from_date,
            to_date=to_date
        )
        return jsonify({
            "status": True,
            "data": [expense.to_dict() for expense in expenses],
            "count": len(expenses)
        }), 200
    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@expense_blp.route(f"{api_version}/delete-expense", methods = ["DELETE"])
@jwt_required(fresh=True)
def delete_expense():
    expense_data = request.get_json()
    expense_id = expense_data.get("expense_id")
    if not expense_id:
        return jsonify({
            "status" : False,
            "error" : "expense id not found, please send the valid one"
        }), 400
    try:
        expense = expense_service.remove_expense(expense_id=expense_id)
        if not expense:
            return jsonify({
                "status" : False,
                "error" : "expense is not found associated with this id"
            }), 404
        return jsonify(expense.to_dict()), 200
    except Exception as e:
        return jsonify({
            "status" : False,
            "error" : str(e)
        }), 500
    

@expense_blp.route(f"{api_version}/update-expense", methods = ["PUT"])
@jwt_required(fresh=True)
def update_expense():
    expense_data = request.get_json()
    expense_id = expense_data.get("expense_id")
    title = expense_data.get("title")
    amount = expense_data.get("amount")
    category = expense_data.get("category")
    description = expense_data.get("description")

    if not expense_id:
        return jsonify({
            "status" : False,
            "error" : "expense id is missing"
        }), 400
    
    try:
        expense = expense_service.update_expense(
            expense_id=expense_id,
            title=title,
            amount=amount,
            description=description,
            category=category
        )
        if not expense:
            return jsonify({
                "status" : False,
                "error" : "expense not found man... please check"
            }), 404
        return jsonify(expense.to_dict()), 200
    except Exception as e:
        return jsonify({
            "status" : False,
            "error" : str(e)
        }), 500


@expense_blp.route(f"{api_version}/create-expense", methods = ["POST"])
@jwt_required(fresh=True)
def create_expense():
    user_email = get_jwt_identity()
    expense_data = request.get_json()
    title = expense_data.get("title")
    amount = expense_data.get("amount")
    category = expense_data.get("category")
    description = expense_data.get("description")

    if not title:
        return jsonify({
            "status" : False,
            "error" : "title is missing"
        }), 400

    if not amount:
        return jsonify({
            "status" : False,
            "error" : "amount is missing"
        }), 400

    if not category:
        return jsonify({
            "status" : False,
            "error" : "Category is missing"
        }), 400

    try:
        expense = expense_service.create_expense(
            user_email=user_email,
            title=title,
            category=category,
            description=description,
            amount=amount
        )
        if not expense:
            return jsonify({
                "status" :  False,
                "error" : "error in making expense..."
            }), 404
        return jsonify(expense.to_dict())
    except Exception as e:
        return jsonify({
            "status" : False,
            "error" : str(e)
        }), 500    
