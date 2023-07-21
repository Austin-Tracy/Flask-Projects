# gpt_app/blueprints/routes.py
import re
from typing import List
from sqlalchemy.orm import Query
from sqlalchemy import desc
from datetime import datetime as dt
from flask import render_template, request, jsonify, redirect, url_for, Response, flash, current_app
from flask_login import login_required
from pm_app import db
from gpt_app import gpt_blueprint as gpt_app
from gpt_app.models.study_conversation import StudyConversation
from gpt_app.models.study_question import StudyQuestion
from gpt_app.utils.helper_functions import generate_study_questions
from gpt_app.blueprints.forms import (
    CreateStudyConversationForm,
    StudyConversationFormSingleChoice,
    StudyConversationFormMultipleChoice,
)
from gpt_app.blueprints.database import (
    get_study_conversation,
    insert_study_conversation,
    get_latest_study_question,
    get_all_study_questions,
    insert_study_question,
    get_all_study_conversations,
    get_latest_study_conversation_id,
    get_study_question,
    get_study_conversation_name,
    get_all_study_conversations_dict,
)


@gpt_app.route("/study", methods=["GET", "POST"])
@login_required
def study(conversation_id=None) -> str:
    """Loads the study page.

    If a conversation ID is not provided, retrieves the latest study conversation ID.
    Initializes the study data, including study conversations, selected topic, and form.
    If a POST request is made with valid form data, handles the post request.
    Otherwise, handles the get request and renders the study page template.

    Args:
        conversation_id (int, optional): The ID of the conversation. Defaults to None.

    Returns:
        str: The rendered template or a redirect response.
    """
    if not conversation_id:
        conversation_id = get_latest_study_conversation_id()
    study_conversations, selected_topic, form = initialize_study_data(conversation_id)
    if request.method == "POST" and form.validate_on_submit():
        return handle_post_request(selected_topic, conversation_id)
    else:
        return handle_get_request(study_conversations, selected_topic, form, conversation_id)
        
def initialize_study_data(conversation_id: int) -> tuple:
    """Initializes the data for the study page.

    Retrieves all study conversations, the selected topic based on the conversation ID,
    and creates an instance of the CreateStudyConversationForm.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        tuple: A tuple containing study conversations, selected topic, and the form instance.
    """
    current_app.logger.info("initialize_study_data")
    study_conversations = get_all_study_conversations()
    selected_topic = get_study_conversation_name(conversation_id)
    form = CreateStudyConversationForm()
    return study_conversations, selected_topic, form


def get_or_create_first_question(conversation_id: int, study_conversation: StudyConversation) -> StudyQuestion:
    """Gets or creates the first question for the study page.

    Retrieves the latest study question for the given study conversation.
    If no question exists, generates study questions and inserts them into the database.
    Otherwise, loads the existing question and choices.

    Args:
        conversation_id (int): The ID of the conversation.
        study_conversation (StudyConversation): The study conversation object.

    Returns:
        StudyQuestion: The first question object.
    """
    current_app.logger.info("get_or_create_first_question")
    first_question = get_latest_study_question(study_conversation.id)
    selected_topic = str(study_conversation.name)
    if first_question is None:
        results = generate_study_questions(study_conversation.id, selected_topic)
        # Insert the new question into the study_conversation
        if results is None:
            return None
        else:
            # loop through the results and set the variables to create all the questions
            for result in results:
                study_question = insert_study_question(
                    gpt_question=result[0],
                    formatted_gpt_response=result[1],
                    is_multiple_choice=result[2],
                    choices=result[3],
                    correct_answer=result[4],
                    question_reason=result[5],
                    conversation_id=conversation_id,
                )
        # study_conversation, gpt_question, choices, is_multiple_choice)
    else:
        # Load the existing question and choices
        gpt_question = first_question.gpt_question
        choices = first_question.choices
        is_multiple_choice = first_question.is_multiple_choice

    return choices, is_multiple_choice, gpt_question, first_question


def handle_post_request(selected_topic: str, conversation_id: int) -> redirect:
    """Handles a POST request to the study page.

    Retrieves the first question for the selected topic and conversation.
    Redirects to the study page with the new conversation ID and current question information.

    Args:
        selected_topic (str): The selected topic for the study.
        conversation_id (int): The ID of the conversation.

    Returns:
        redirect: Redirect to the study page.
    """
    print("handle_post_request")
    if selected_topic and conversation_id:
        current_question = get_or_create_first_question(conversation_id, selected_topic)
        # Return a redirect to the study page with the new conversation_id
        return redirect(
            url_for(
                "gpt.study",
                conversation_id=conversation_id,
                current_question_id=current_question.id,
                current_question=current_question,
            )
        )
    else:
        return redirect(url_for("study"))


def handle_get_request(study_conversations, selected_topic: str, form, conversation_id: int):
    """Handles a GET request to the study page.

    Renders the study page template with the necessary data.

    Args:
        study_conversations: The study conversations.
        selected_topic (str): The selected topic for the study.
        form: The form instance.
        conversation_id (int): The ID of the conversation.

    Returns:
        The rendered template.
    """
    print("handle_get_request")
    return render_template(
        "study.html",
        form=form,
        conversation_id=conversation_id,
        study_conversations=study_conversations,
    )


@gpt_app.route("/topics", methods=["GET"])
@login_required
def load_study_conversations():
    """Loads all study conversations.

    Retrieves the necessary data for the study page, including study conversations,
    form instances, and the latest study question. Renders the study page template.

    Returns:
        str: The rendered template.
    """
    form: CreateStudyConversationForm = CreateStudyConversationForm()
    single_choice_form = StudyConversationFormSingleChoice()
    multiple_choice_form = StudyConversationFormMultipleChoice()
    study_conversations: List[StudyConversation] = get_all_study_conversations()
    conversation_id = get_latest_study_conversation_id()
    current_question = None
    study_question = None
    if conversation_id:
        study_question = get_latest_study_question(conversation_id)

    return render_template(
        "study.html",
        form=form,
        study_conversations=study_conversations,
        single_choice_form=single_choice_form,
        multiple_choice_form=multiple_choice_form,
        current_question=study_question,
    )


@gpt_app.route("/topic/<int:conversation_id>", methods=["GET"])
@login_required
def load_study_conversation(conversation_id: int) -> Response:
    """Loads the selected study conversation.

    Retrieves the necessary data for the selected study conversation, including form instances,
    study conversations, the latest study question, and the conversation name. Renders the
    study page template.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        Response: The rendered template.
    """
    form: CreateStudyConversationForm = CreateStudyConversationForm()
    single_choice_form = StudyConversationFormSingleChoice()
    multiple_choice_form = StudyConversationFormMultipleChoice()
    study_conversations: List[StudyConversation] = get_all_study_conversations()
    study_question: Query = get_latest_study_question(conversation_id)
    if study_question is not None:
        study_question_id = study_question.id
    else:
        study_question_id = None  # Or some default value
    study_conversation_name: Query = get_study_conversation(conversation_id).name

    # Get the question from the latest study history
    create_study_conversation_form = CreateStudyConversationForm()
    return render_template(
        "study.html",
        form=form,
        study_conversations=study_conversations,
        study_question=study_question,
        single_choice_form=single_choice_form,
        multiple_choice_form=multiple_choice_form,
        conversation_id=conversation_id,
        create_study_conversation_form=create_study_conversation_form,
        conversation_name=study_conversation_name,
        study_question_id=study_question_id,
    )


@gpt_app.route("/create_study_conversation", methods=["POST"])
@login_required
def create_study_conversation() -> Response:
    """Creates a new study conversation.

    Creates a new study conversation with the provided name if it does not exist.
    Generates study questions for the new conversation and redirects to the study page
    with the new conversation ID and current question information.

    Returns:
        Response: Redirect to the study page.
    """
    form = CreateStudyConversationForm()
    if form.validate_on_submit():
        conversation_id = get_latest_study_conversation_id()
        existing_conversation_dict = get_all_study_conversations_dict()

        # print("Existing Conversation Dict:", existing_conversation_dict) # DEBUG

        conversation_name = str(form.name.data)

        if not conversation_name in existing_conversation_dict.keys():
            new_study_conversation = insert_study_conversation(conversation_name)
            existing_conversation_dict = get_all_study_conversations_dict()
            conversation_id = new_study_conversation.id
            selected_topic = conversation_name
        else:
            conversation_id = existing_conversation_dict[conversation_name]
            selected_topic = conversation_name
            
        results = generate_study_questions(conversation_id, selected_topic)

        if results is None:
            flash("No question was generated. Please try again.")
            return redirect(url_for("gpt.load_study_conversation", conversation_id=conversation_id))
        
        elif results:
            # loop through the results and set the variables to create all the questions
            for result in results:
                study_question = insert_study_question(
                    gpt_question=result[0],
                    formatted_gpt_response=result[1],
                    is_multiple_choice=result[2],
                    choices=result[3],
                    correct_answer=result[4],
                    question_reason=result[5],
                    conversation_id=result[6],
                )
            # Return a redirect to the study page with the new conversation_id
            return redirect(
                url_for(
                    "gpt.load_study_conversation",
                    conversation_id=conversation_id,
                    study_question_id=study_question.id,
                )
            )
    else:
        return redirect(url_for("gpt.study", conversation_id=conversation_id))

@gpt_app.route("/add_questions/<int:conversation_id>", methods=["GET"])
@login_required
def add_questions(conversation_id: int, verbose: bool = False) -> Response:
    study_conversation = get_study_conversation(conversation_id)
    if study_conversation:
        results = generate_study_questions(study_conversation.id, study_conversation.name)
        if results:
            # loop through the results and set the variables to create all the questions
            for result in results:
                study_question = insert_study_question(
                    gpt_question=result[0],
                    formatted_gpt_response=result[1],
                    is_multiple_choice=result[2],
                    choices=result[3],
                    correct_answer=result[4],
                    question_reason=result[5],
                    conversation_id=result[6],
                )
        newest_question = get_latest_study_question(study_conversation.id)
        if verbose:
            current_app.logger.info("Question: ", newest_question)
        if newest_question:
            return redirect(url_for('gpt.question', 
                                    conversation_id=conversation_id, 
                                    question_id=newest_question.id))
    flash('No questions added.')
    return redirect(url_for('gpt.study'))

@gpt_app.route("topic/<int:conversation_id>/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def question(conversation_id: int, question_id: int) -> Response:
    """Loads the question page.
    
    Retrieves the necessary data for the question page, including study questions,
    the selected topic, and the current question. Renders the question page template.

    Args:
        conversation_id (int): The ID of the conversation.
        question_id (int): The ID of the question.

    Returns:
        Response: The rendered template or a redirect response.
    """
    study_questions = get_all_study_questions(conversation_id)
    selected_topic = get_study_conversation_name(conversation_id)
    current_question = get_study_question(question_id)

    if current_question.is_multiple_choice:
        form = StudyConversationFormMultipleChoice()
    else:
        form = StudyConversationFormSingleChoice()

    # Deserialize the choices field into a list of tuples
    choices = current_question.choices
    form.choices = [[choice[0], choice[1]] for choice in choices]

    if request.method == "POST" and form.validate_on_submit():
        # get the user's answers from the form
        user_answers = form.data["choices"]

        # get the correct answer(s) from the database
        correct_answers = current_question.correct_answer

        # compare the user's answers with the correct ones
        user_correct = user_answers == correct_answers

        # find the reasoning for the question
        question_reasoning = current_question.question_reason

        # render a new template displaying the results
        return render_template('result.html', 
                                user_correct=user_correct, 
                                correct_answers=correct_answers,
                                user_answers=user_answers,
                                question_reasoning=question_reasoning)

    return render_template('question.html', 
                           study_questions=study_questions, 
                           current_question=current_question,
                           conversation_id=conversation_id, 
                           selected_topic=selected_topic,
                           multiple_choice_form=form if current_question.is_multiple_choice else None,
                           single_choice_form=form if not current_question.is_multiple_choice else None)

    
@gpt_app.context_processor
@login_required
def utility_processor() -> dict:
    """Creates a context processor for utility functions.

    Defines utility functions to be used within templates, such as getting the previous
    and next question IDs.

    Returns:
        dict: A dictionary containing the utility functions.
    """
    def get_previous_question_id(question_id: int) -> int:
        current_question = get_study_question(question_id)
        previous_question = StudyQuestion.query.filter(StudyQuestion.conversation_id == current_question.conversation_id, StudyQuestion.created_at < current_question.created_at).order_by(desc(StudyQuestion.created_at)).first()
        if previous_question:
            return previous_question.id
        else:
            return question_id  # return the current question id if there is no previous question

    def get_next_question_id(question_id: int) -> int:
        current_question = get_study_question(question_id)
        next_question = StudyQuestion.query.filter(StudyQuestion.conversation_id == current_question.conversation_id, StudyQuestion.created_at > current_question.created_at).order_by(StudyQuestion.created_at).first()
        if next_question:
            return next_question.id
        else:
            return question_id  # return the current question id if there is no next question

    return dict(get_previous_question_id=get_previous_question_id, get_next_question_id=get_next_question_id)

def parse_reasoning(reasoning: str, verbose: bool = False):
    reasoning_dict = {}
    # Split the string on commas that are outside of parentheses
    reasoning = reasoning.replace('\"','')
    choices = re.findall(r'\(([A-E]),\\(.*?)\\', reasoning)

    for choice in choices:
        choice_letter = choice[0]
        choice_explanation = choice[1]
        reasoning_dict[choice_letter] = choice_explanation
    if verbose:
        current_app.logger.info("Parsed Reasoning: ", reasoning_dict)
    return reasoning_dict

@gpt_app.route("/submit_answer", methods=["POST"])
@login_required
def submit_answer(verbose: bool = False) -> dict:
    """Submit user's answer and get the correct answer and reasoning.

    Receives the user's selected answers, retrieves the correct answer and reasoning for the question,
    and determines whether each user selection is correct.

    Returns:
        dict: A dictionary containing the correct answer, reasoning, and a mapping of the user's selections to their correctness.
    """
    # request.json should be a dictionary like {"question_id": 1, "user_choices": ["choice1", "choice2"]}
    question_id = request.json["question_id"]
    user_choices = request.json["user_choices"]

    # Get the question from the database
    current_question = get_study_question(question_id)

    # Get the correct answer(s) and reasoning for the question
    correct_answers = current_question.correct_answer
    if verbose:
        current_app.logger.info("Correct Answers: ", correct_answers)
    correct_count = len(correct_answers)
    # Determine if each user selection is correct
    user_choices_correctness = {choice: choice in correct_answers for choice in user_choices}
    if verbose:
        current_app.logger.info("Question Reasoning from DB: ", current_question.question_reason)
    reasoning = parse_reasoning(current_question.question_reason)
    if verbose:
        current_app.logger.info("User Choices Correctness: ", user_choices_correctness)
    return jsonify({
        'user_choices_correctness': user_choices_correctness,
        'reasoning': reasoning,
        'total_correct': correct_count
    }), 200