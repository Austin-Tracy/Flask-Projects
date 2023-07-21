import pytest
from gpt_app.blueprints.database import (insert_study_conversation, is_duplicate_study_question, get_study_question, get_latest_study_question, get_all_study_questions, get_all_study_gpt_questions, insert_study_question, insert_study_questions)
from gpt_app.models.study_conversation import StudyConversation
from gpt_app.models.study_question import StudyQuestion
from datetime import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gpt_app.models import Base
import pytest

@pytest.fixture(scope='function')
def db_session():
    # Create an engine and a session
    engine = create_engine('sqlite:///:memory:')  # Use in-memory SQLite for testing
    Base.metadata.create_all(engine)  # Create all tables in the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Provide the transaction
        yield session
    finally:
        # Rollback and close the session
        session.rollback()
        session.close()

def test_insert_study_conversation(db_session):
    name = "Test Conversation"
    result = insert_study_conversation(name)
    assert isinstance(result, StudyConversation)
    assert result.name == name

def test_is_duplicate_study_question(db_session):
    # Add a mock StudyQuestion to the database
    question = StudyQuestion(question="Test question", created_at=dt.now())
    db_session.add(question)
    db_session.commit()
    # Test if the function correctly identifies it as a duplicate
    assert is_duplicate_study_question("Test question") == True

def test_get_study_question(db_session):
    # Add a mock StudyQuestion to the database
    question = StudyQuestion(question="Test question", created_at=dt.now())
    db_session.add(question)
    db_session.commit()
    # Test if the function correctly retrieves it
    assert get_study_question(question.id) == question

def test_get_latest_study_question(db_session):
    # Add multiple mock StudyQuestion objects to the database
    question1 = StudyQuestion(question="Test question 1", created_at=dt.now())
    question2 = StudyQuestion(question="Test question 2", created_at=dt.now())
    db_session.add(question1)
    db_session.add(question2)
    db_session.commit()
    # Test if the function correctly retrieves the latest one
    assert get_latest_study_question() == question2

def test_get_all_study_questions(db_session):
    # Add multiple mock StudyQuestion objects to the database
    question1 = StudyQuestion(question="Test question 1", created_at=dt.now())
    question2 = StudyQuestion(question="Test question 2", created_at=dt.now())
    db_session.add(question1)
    db_session.add(question2)
    db_session.commit()
    # Test if the function correctly retrieves all of them
    assert get_all_study_questions() == [question1, question2]

def test_get_all_study_gpt_questions(db_session):
    # Add multiple mock StudyQuestion objects to the database
    question1 = StudyQuestion(question="Test question 1", created_at=dt.now(), is_gpt=True)
    question2 = StudyQuestion(question="Test question 2", created_at=dt.now(), is_gpt=False)
    db_session.add(question1)
    db_session.add(question2)
    db_session.commit()
    # Test if the function correctly retrieves all GPT questions
    assert get_all_study_gpt_questions() == [question1]

def test_insert_study_question(db_session):
    # Create a mock question
    question = "Test question"
    # Test if the function correctly inserts it into the database
    result = insert_study_question(question)
    assert isinstance(result, StudyQuestion)
    assert result.question == question

def test_insert_study_questions(db_session):
    # Create multiple mock questions
    questions = ["Test question 1", "Test question 2"]
    # Test if the function correctly inserts all of them into the database
    results = insert_study_questions(questions)
    assert all(isinstance(result, StudyQuestion) for result in results)
    assert [result.question for result in results] == questions
