# pm_app/models/user_history.py
from pm_app import db
from datetime import datetime

class UserHistory(db.Model):
    """
    Model class for user history.

    Attributes:
        id (int): Unique identifier for the user history.
        ip_address (str): IP address of the user.
        user_agent (str): User agent used by the user.
        timestamp (datetime): Timestamp when the user activity was recorded.
        requested_url (str): URL requested by the user.
        referrer_url (str): Referrer URL.

        user_id (int): Foreign key reference to the user who performed the activity.
    """
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    requested_url = db.Column(db.String(256))
    referrer_url = db.Column(db.String(256))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))