# gpt_app/models/study_question.py
from pm_app import db

class StudyQuestion(db.Model):
    """
    This class represents a study question in the database.

    Attributes:
        id (int): The unique identifier for the study question.
        created_at (datetime): The timestamp for when the study question was created.
        gpt_question (str): The question generated by the GPT model.
        question_reason (str): The reason for asking the question.
        gpt_response (str): The response generated by the GPT model.
        is_multiple_choice (bool): Whether the question is a multiple choice question.
        choices (list): The choices for a multiple choice question.
        correct_answer (str): The correct answer for a multiple choice question.
        conversation_id (int): The ID of the conversation that the question belongs to.
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    gpt_question = db.Column(db.Text)
    question_reason = db.Column(db.Text)
    gpt_response = db.Column(db.Text)
    is_multiple_choice = db.Column(db.Boolean, default=False)
    choices = db.Column(db.JSON)
    correct_answer = db.Column(db.Text)
    conversation_id = db.Column(db.Integer, db.ForeignKey("study_conversation.id"))