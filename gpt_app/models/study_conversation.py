# gpt_app/models/study_conversation.py
from pm_app import db


class StudyConversation(db.Model):
    """
    This class represents a study conversation in the project management web app.

    Attributes:
    id (int): The primary key of the study conversation.
    name (str): The name of the study conversation.
    keywords (str): The keywords associated with the study conversation.
    seed_prompt (str): The seed prompt for the study conversation.
    study_histories (relationship): The relationship between the study conversation and its study histories.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text)
    seed_prompt = db.Column(db.Text)
    study_histories = db.relationship("StudyQuestion", backref="study_conversation", lazy="dynamic")