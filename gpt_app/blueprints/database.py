#/gpt_app/blueprints/database.py
from typing import List
from pm_app import db
from gpt_app.models.study_conversation import StudyConversation
from gpt_app.models.study_question import StudyQuestion
from sqlalchemy import desc, asc
from datetime import datetime as dt

def get_study_conversation(conversation_id: int) -> StudyConversation:
    """Retrieve a study conversation by its ID.

    Args:
        conversation_id (int): The ID of the study conversation.

    Returns:
        StudyConversation: The study conversation object.

    Raises:
        NotFound: If the study conversation with the given ID is not found.
    """
    return StudyConversation.query.get_or_404(conversation_id)

def get_study_conversation_name(conversation_id: int) -> str:
    """Retrieve the name of a study conversation by its ID.

    Args:
        conversation_id (int): The ID of the study conversation.

    Returns:
        str: The name of the study conversation.
    """
    return StudyConversation.query.filter_by(id=conversation_id).first().name

# Return a dictionary where the key is the conversation name and the value is the conversation id
def get_all_study_conversations_dict() -> dict:
    """Return a dictionary of all study conversations.

    Returns:
        dict: A dictionary where the key is the conversation name and the value is the conversation ID.
    """
    study_conversations = get_all_study_conversations()
    study_conversations_dict = {}
    for study_conversation in study_conversations:
        study_conversations_dict[study_conversation.name] = study_conversation.id
    return study_conversations_dict

def get_all_study_conversations() -> List[StudyConversation]:
    """Retrieve all study conversations.

    Returns:
        List[StudyConversation]: A list of study conversation objects.
    """
    return StudyConversation.query.all()

# function that returns the most recent study conversation id
def get_latest_study_conversation_id() -> int:
    """Retrieve the ID of the most recent study conversation.

    Returns:
        int: The ID of the most recent study conversation.
    """
    first_conversation = StudyConversation.query.order_by(desc(StudyConversation.id)).first()
    if first_conversation:
        return first_conversation.id
    else:
        return 0


def insert_study_conversation(name: str) -> StudyConversation:
    """Insert a new study conversation into the database.

    Args:
        name (str): The name of the study conversation.

    Returns:
        StudyConversation: The inserted study conversation object.
    """
    new_study_conversation = StudyConversation(name=name)
    db.session.add(new_study_conversation)
    db.session.commit()
    if new_study_conversation:
        print("Study Conversation Inserted Successfully")
    return new_study_conversation

# Return a boolean indicating whether the same question is already found in the study_question table
def is_duplicate_study_question(conversation_id: int, gpt_question: str) -> bool:
    """Check if a study question with the same conversation ID and GPT question already exists.

    Args:
        conversation_id (int): The ID of the conversation.
        gpt_question (str): The GPT question.

    Returns:
        bool: True if a duplicate study question is found, False otherwise.
    """
    possible_match = StudyQuestion.query.filter_by(conversation_id=conversation_id, gpt_question=gpt_question).first()
    if possible_match:
        if possible_match.gpt_question.lower() == gpt_question.lower():
            return True
    return False

# Function that returns a specific study question
def get_study_question(question_id: int) -> StudyQuestion:
    """Retrieve a study question by its ID.

    Args:
        question_id (int): The ID of the study question.

    Returns:
        StudyQuestion: The study question object.

    Raises:
        NotFound: If the study question with the given ID is not found.
    """
    return StudyQuestion.query.get_or_404(question_id)

def get_latest_study_question(conversation_id: int) -> StudyQuestion:
    """Retrieve the latest study question for a conversation.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        StudyQuestion: The latest study question object.

    Raises:
        NotFound: If no study question is found for the conversation.
    """
    return StudyQuestion.query.filter_by(conversation_id=conversation_id).order_by(desc(StudyQuestion.created_at)).first()

def get_all_study_questions(conversation_id: int) -> List[StudyQuestion]:
    """Retrieve all study questions for a conversation.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        List[StudyQuestion]: A list of study question objects, ordered by creation date.
    """
    return StudyQuestion.query.filter_by(conversation_id=conversation_id).order_by(asc(StudyQuestion.created_at)).all()

# Given an input of conversation_id return a List of all gpt_question that are part of that conversation
def get_all_study_gpt_questions(conversation_id: int) -> List[str]:
    """Retrieve all GPT questions for a conversation.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        List[str]: A list of GPT questions.
    """
    study_questions = StudyQuestion.query.filter_by(conversation_id=conversation_id).all()
    study_questions_list = []
    for study_question in study_questions:
        study_questions_list.append(study_question.gpt_question)
    return study_questions_list

def insert_study_question(gpt_question: str, formatted_gpt_response: str, conversation_id: int, is_multiple_choice: bool, choices: List[List[str]], correct_answer: str, question_reason: str) -> StudyQuestion:
    """Insert a new study question into the database.

    Args:
        gpt_question (str): The GPT question.
        formatted_gpt_response (str): The formatted GPT response.
        conversation_id (int): The ID of the conversation.
        is_multiple_choice (bool): Indicates whether the question is multiple choice.
        choices (List[List[str]]): The choices for the multiple choice question.
        correct_answer (str): The correct answer for the question.
        question_reason (str): The reason for the question.

    Returns:
        StudyQuestion: The inserted study question object.
    """
    study_question = StudyQuestion(
        gpt_question = gpt_question,
        gpt_response = str(formatted_gpt_response),
        conversation_id = conversation_id,
        is_multiple_choice = is_multiple_choice,
        choices = choices,
        correct_answer = correct_answer,
        question_reason = question_reason,
        created_at = dt.now(),
    )
    db.session.add(study_question)
    db.session.commit()
    if study_question:
        print("Study Question Inserted Successfully")
    else:
        print("Study Question Insert Failed")
    return study_question

def insert_study_questions(results) -> StudyQuestion:
    """Insert multiple study questions into the database.

    Args:
        results: The study questions to insert.

    Returns:
        StudyQuestion: The inserted study question object.
    """
    for result in results:
        study_question = StudyQuestion(
            gpt_question = result[0],
            gpt_response = str(result[1]),
            is_multiple_choice = results[2],
            choices = results[3],
            correct_answer = results[4],
            question_reason = results[5],
            conversation_id = results[6],
            created_at = dt.now(),
        )
        db.session.add(study_question)
    db.session.commit()
    question_count = len(results)
    if study_question:
        print(f"Study Questions Inserted Successfully: {question_count}")
    else:
        print("Study Question Insert Failed")
    return study_question