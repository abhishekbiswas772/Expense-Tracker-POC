from models.user_model import UserDBModel
from extension import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class AuthManager:
    def __init__(self):
        self.db = db

    class UserExceptions(Exception):
        pass

    def login_user(self, password: str, email: str) -> UserDBModel:
        if not email:
            raise self.UserExceptions("User cannot be logged in — email is missing.")
        if not password:
            raise self.UserExceptions("User cannot be logged in — password is missing.")

        existing_user = UserDBModel.query.filter_by(email=email).first()
        if not existing_user:
            raise self.UserExceptions("User does not exist — please sign up first.")

        if not check_password_hash(existing_user.password, password):
            raise self.UserExceptions("Password is incorrect.")

        existing_user.updatedAt = datetime.utcnow()
        self.db.session.commit()  
        return existing_user

    def create_user(self, username: str, password: str, email: str) -> UserDBModel:
        if not username:
            raise self.UserExceptions("User cannot be created — username is missing.")
        if not password:
            raise self.UserExceptions("User cannot be created — password is missing.")
        if not email:
            raise self.UserExceptions("User cannot be created — email is missing.")

        existing_user = UserDBModel.query.filter_by(email=email).first()
        if existing_user:
            raise self.UserExceptions("User already exists — please log in instead.")

        try:
            hashed_password = generate_password_hash(password)
            user = UserDBModel(
                username=username,
                email=email,
                password=hashed_password,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )

            self.db.session.add(user)
            self.db.session.commit()

            return user
        except Exception as e:
            self.db.session.rollback()
            raise self.UserExceptions(f"Error creating user: {str(e)}")
