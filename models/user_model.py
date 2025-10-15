from extension import db
from datetime import datetime
import uuid


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(255),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()) 
    )
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    expenses = db.relationship("ExpenseModel", back_populates="user", cascade="all, delete-orphan")

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
            "username": self.username,
            "email": self.email,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None,
        }
