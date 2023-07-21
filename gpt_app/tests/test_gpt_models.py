import pytest
from datetime import datetime
from pm_app import create_app, db
from gpt_app.models.study_conversation import StudyConversation
from gpt_app.models.study_question import StudyQuestion

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

######## Study Conversation Tests ########
def test_study_conversation_creation():
    """
    Test the creation of a StudyConversation instance.
    """
    study_conversation = StudyConversation()
    assert isinstance(study_conversation, StudyConversation)

def test_study_conversation_attributes():
    """
    Test the assignment of attributes to a StudyConversation instance.
    """
    study_conversation = StudyConversation()
    study_conversation.id = 1
    study_conversation.name = "Test Study Conversation"
    study_conversation.keywords = "Test, Study, Conversation"
    study_conversation.seed_prompt = "This is a test seed prompt."

    assert study_conversation.id == 1
    assert study_conversation.name == "Test Study Conversation"
    assert study_conversation.keywords == "Test, Study, Conversation"
    assert study_conversation.seed_prompt == "This is a test seed prompt."

def test_study_conversation_study_question_relationship():
    """
    Test the relationship between StudyConversation and StudyQuestion.
    """
    study_conversation = StudyConversation()
    study_question = StudyQuestion()
    study_question.study_conversation = study_conversation

    assert study_question in study_conversation.study_histories


######## Study Question Tests ########
@pytest.fixture
def study_question():
    question = StudyQuestion(
        gpt_question="What is AI?",
        question_reason="To understand the basics of AI",
        gpt_response="AI stands for Artificial Intelligence...",
        is_multiple_choice=True,
        choices={"A": "Artificial Intelligence", "B": "Apple Inc", "C": "An Ice-cream"},
        correct_answer="A",
        conversation_id=1
    )
    return question

def test_study_question_creation(study_question):
    assert isinstance(study_question, StudyQuestion)

def test_study_question_defaults(study_question):
    assert isinstance(study_question.created_at, datetime)
    assert study_question.is_multiple_choice is True

def test_study_question_assignments(study_question):
    assert study_question.gpt_question == "What is AI?"
    assert study_question.question_reason == "To understand the basics of AI"
    assert study_question.gpt_response == "AI stands for Artificial Intelligence..."
    assert study_question.choices == {"A": "Artificial Intelligence", "B": "Apple Inc", "C": "An Ice-cream"}
    assert study_question.correct_answer == "A"
    assert study_question.conversation_id == 1

# Assuming you have a StudyConversation model
def test_study_question_relationship(study_conversation, study_question):
    study_question.conversation_id = study_conversation.id
    db.session.add(study_question)
    db.session.commit()
    assert study_question.conversation_id == study_conversation.id