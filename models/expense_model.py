from extension import db
import uuid
from datetime import datetime

class ExpenseModel(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.String(255), nullable = False, primary_key = True, default = lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.String(255), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="expenses")
    createdAt = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updatedAt = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "user_id": self.user_id,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }
