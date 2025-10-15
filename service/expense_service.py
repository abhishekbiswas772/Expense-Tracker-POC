from enum import Enum
from extension import db
from models.expense_model import ExpenseModel
from models.user_model import UserModel
from datetime import datetime, timedelta
from copy import deepcopy

class Category(Enum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"


class ExpenseFilter(Enum):
    PAST_WEEK = "past_week"
    PAST_MONTH = "past_month"
    LAST_THREE_MONTH = "last_three_month"
    CUSTOM = "custom"

class ExpenseService:
    def __init__(self):
        self.db = db

    class ExpenseException(Exception):
        pass

    def check_assign_category(self, category : str) -> str:
        if category.lower() == Category.CLOTHING.value.lower():
            return Category.CLOTHING.value
        elif category.lower() == Category.GROCERIES.value.lower():
            return Category.GROCERIES.value.lower()
        elif category.lower() == Category.LEISURE.value.lower():
            return Category.LEISURE.value.lower()
        elif category.lower() == Category.ELECTRONICS.value.lower():
            return Category.ELECTRONICS.value.lower()
        elif category.lower() == Category.UTILITIES.value.lower():
            return Category.UTILITIES.value.lower()
        elif category.lower() == Category.HEALTH.value.lower():
            return Category.HEALTH.value.lower()
        else:
            return Category.OTHERS.value.lower()
        
    def check_assign_expense_filter(self, filter_category: str) -> str:
        if filter_category.lower() == ExpenseFilter.PAST_WEEK.value.lower():
            return ExpenseFilter.PAST_WEEK.value
        elif filter_category.lower() == ExpenseFilter.PAST_MONTH.value.lower():
            return ExpenseFilter.PAST_MONTH.value
        elif filter_category.lower() == ExpenseFilter.LAST_THREE_MONTH.value.lower():
            return ExpenseFilter.LAST_THREE_MONTH.value
        elif filter_category.lower() == ExpenseFilter.CUSTOM.value.lower():
            return ExpenseFilter.CUSTOM.value
        else:
            return ExpenseFilter.PAST_WEEK.value
        
    def filter_expense(self, user_email: str, expense_filter_category: str = None, from_date: str = None, to_date: str = None):
        if not user_email:
            raise self.ExpenseException("user email is missing")

        try:
            user = UserModel.query.filter_by(email=user_email).first()
            if not user:
                raise self.ExpenseException("user not found")

            if not expense_filter_category:
                expense_filter_category = ExpenseFilter.PAST_WEEK.value

            expense_filter_category = self.check_assign_expense_filter(filter_category=expense_filter_category)

            now = datetime.utcnow()

            if expense_filter_category == ExpenseFilter.PAST_WEEK.value:
                start_date = now - timedelta(days=7)
                end_date = now
            elif expense_filter_category == ExpenseFilter.PAST_MONTH.value:
                start_date = now - timedelta(days=30)
                end_date = now
            elif expense_filter_category == ExpenseFilter.LAST_THREE_MONTH.value:
                start_date = now - timedelta(days=90)
                end_date = now
            elif expense_filter_category == ExpenseFilter.CUSTOM.value:
                if not from_date or not to_date:
                    raise self.ExpenseException("from_date and to_date are required for custom filter")
                try:
                    start_date = datetime.fromisoformat(from_date)
                    end_date = datetime.fromisoformat(to_date)
                except ValueError:
                    raise self.ExpenseException("Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
            else:
                start_date = now - timedelta(days=7)
                end_date = now

            expenses = ExpenseModel.query.filter(
                ExpenseModel.user_id == user.id,
                ExpenseModel.createdAt >= start_date,
                ExpenseModel.createdAt <= end_date
            ).order_by(ExpenseModel.createdAt.desc()).all()

            return expenses

        except Exception as e:
            raise self.ExpenseException(f"Failed to filter expenses: {str(e)}")

        
    def remove_expense(self, expense_id : str) -> ExpenseModel:
        if not expense_id:
            raise self.ExpenseException("expense id is missing, please send valid one")
        
        try:
            expense = ExpenseModel.query.filter_by(id = expense_id).first()
            if not expense:
                raise self.ExpenseException("expense not found")
            expense_cpy = deepcopy(expense)
            self.db.session.delete(expense)
            self.db.session.commit()
            return expense_cpy
        except Exception as e:
            self.db.session.rollback()
            raise self.ExpenseException(str(e))
    

    def update_expense(
        self,
        expense_id: str,
        title: str = None,
        amount: float = None,
        description: str = None,
        category: str = None,
    ) -> ExpenseModel:
        if not expense_id:
            raise self.ExpenseException("Expense ID is missing. Please provide a valid one.")

        try:
            expense = ExpenseModel.query.filter_by(id=expense_id).first()
            if not expense:
                raise self.ExpenseException("Expense not found for the given ID.")

            if title:
                expense.title = title
            if amount is not None:  
                expense.amount = amount
            if description:
                expense.description = description
            if category:
                expense.category = self.check_assign_category(category)

            if float(amount) < 0:
                raise self.ExpenseException("amnount cannot less than 0")

            expense.updatedAt = datetime.utcnow()
            self.db.session.commit()

            return expense

        except Exception as e:
            self.db.session.rollback()
            raise self.ExpenseException(f"Failed to update expense: {str(e)}")


    def create_expense(
        self, title : str,
        amount : float, category : str,
        description : str, user_email : str
    ) -> ExpenseModel:
        if not title:
            raise self.ExpenseException("expense title is missing..")
        
        if not amount:
            raise self.ExpenseException("amount is missing")
        
        if float(amount) < 0:
            raise self.ExpenseException("amnount cannot less than 0")
        
        if not category:
            raise self.ExpenseException("category of expense is missing")
        
        if not description:
            raise self.ExpenseException("description is missing")
        
        if not user_email:
            raise self.ExpenseException("user email is missing")

        try:
            user = UserModel.query.filter_by(email=user_email).first()
            if not user:
                raise self.ExpenseException("user not found, cannot add expense...")
            expense = ExpenseModel(
                title = title,
                amount = amount,
                category = self.check_assign_category(category=category),
                description = description,
                user_id = user.id,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            self.db.session.add(expense)
            self.db.session.commit()
            return expense
        except Exception as e:
            self.db.session.rollback()
            raise self.ExpenseException(str(e))        
