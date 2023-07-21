# pm_app/models/user.py
from pm_app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError

class User(UserMixin, db.Model):
    """
    User Model Class for storing user information

    :param UserMixin: Flask-Login mixin class for adding user authentication properties
    :param db.Model: SQLAlchemy class for creating models

    Attributes:
        id (int): Unique identifier for the user.
        firstname (str): First name of the user.
        lastname (str): Last name of the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        phonenumber (str): Phone number of the user.
        password_hash (str): Hashed password of the user.
        user_activity (relationship): Relationship to the user activity history.
        projects (relationship): Relationship to the projects owned by the user.
        tasks (relationship): Relationship to the tasks assigned to the user.
    """
    # User Model Fields/Attributes
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phonenumber = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(128))
    user_activity = db.relationship('UserHistory', backref='user', lazy='dynamic')

    # User Model Relationships
    projects = db.relationship("Project", backref="owner", lazy="dynamic")
    tasks = db.relationship("Task", backref="user", lazy="dynamic")

    # User Model Methods
    def set_password(self, password: str) -> None:
        """Hashes and sets the user password

        :param password: string, the user's plain text password

        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the given password matches the user's hashed password

        :param password: string, the user's plain text password
        :return: bool, True if the password matches, False otherwise

        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Represents the User object as a string

        :return: string, representation of the User object

        """
        return f'<User {self.username}>'

    def validate_username(self, username: str) -> None:
        """Validates the username against username length requirements and uniqueness

        :param username: string, the username to validate
        :raise ValidationError: if the username is not unique or does not meet length requirements

        """
        if User.query.filter_by(username=username).first():
            raise ValidationError('Please use a different username.')
        if len(username) < 4 or len(username) > 20:
            raise ValidationError('Username must be between 4 and 20 characters.')

@login.user_loader
def load_user(user_id: int) -> User:
    """Loads the user object based on the user ID stored in the Flask session

    :param user_id: integer, the ID of the user to load
    :return: User object, the user associated with the given ID

    """
    return db.session.get(User, int(user_id))