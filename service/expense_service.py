from enum import Enum
from extension import db

class Category(Enum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"

class ExpenseService:
    def __init__(self):
        self.db = db

    def create_expense(
        self,
        title : str,
        amount : float,
        category : Category,
        description : str,
        user_email : str
    ):
        pass
