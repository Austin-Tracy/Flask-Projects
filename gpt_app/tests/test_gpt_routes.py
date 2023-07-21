import pytest
from flask import url_for, json
from pm_app import create_app, db
from gpt_app.models.study_question import StudyQuestion
from gpt_app.models.study_conversation import StudyConversation
from gpt_app.blueprints.routes import initialize_study_data, get_or_create_first_question, handle_post_request, handle_get_request, parse_reasoning, utility_processor
from gpt_app.blueprints.forms import CreateStudyConversationForm
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    db.session.remove()
    db.drop_all()

@patch('gpt_app.blueprints.routes.get_latest_study_conversation_id')
@patch('gpt_app.blueprints.routes.initialize_study_data')
@patch('gpt_app.blueprints.routes.handle_post_request')
@patch('gpt_app.blueprints.routes.handle_get_request')
def test_study(mock_get_request, mock_post_request, mock_initialize_data, mock_get_conversation_id, client):
    mock_get_conversation_id.return_value = 1
    mock_initialize_data.return_value = ([], 'topic', None)
    mock_get_request.return_value = 'GET response'
    mock_post_request.return_value = 'POST response'

    response = client.get('/study')
    assert response.data.decode() == 'GET response'

    response = client.post('/study')
    assert response.data.decode() == 'POST response'

@patch('gpt_app.blueprints.routes.get_all_study_conversations')
@patch('gpt_app.blueprints.routes.get_study_conversation_name')
@patch('gpt_app.blueprints.routes.CreateStudyConversationForm')
def test_initialize_study_data(mock_form, mock_get_name, mock_get_conversations):
    mock_get_conversations.return_value = []
    mock_get_name.return_value = 'topic'
    mock_form.return_value = None

    result = initialize_study_data(1)
    assert result == ([], 'topic', None)

@pytest.fixture
def study_conversation():
    return StudyConversation(id=1, name='Test Conversation')

@pytest.fixture
def study_question():
    return StudyQuestion(id=1, gpt_question='Test Question', choices=['Choice 1', 'Choice 2'], is_multiple_choice=True)

def test_get_or_create_first_question(study_conversation, study_question):
    result = get_or_create_first_question(1, study_conversation)
    assert result == (study_question.choices, study_question.is_multiple_choice, study_question.gpt_question, study_question)

def test_handle_post_request(client, study_conversation, study_question):
    with client.session_transaction() as session:
        session['selected_topic'] = study_conversation.name
        session['conversation_id'] = 1
    response = client.post(url_for('gpt.study'), follow_redirects=True)
    assert response.status_code == 200
    assert study_question.gpt_question in response.data.decode()

def test_initialize_study_data(study_conversation):
    result = initialize_study_data(1)
    assert result == ([study_conversation], study_conversation.name, CreateStudyConversationForm())

@patch('gpt_app.blueprints.routes.get_or_create_first_question')
@patch('gpt_app.blueprints.routes.redirect')
@patch('gpt_app.blueprints.routes.url_for')
def test_handle_post_request(mock_url_for, mock_redirect, mock_get_or_create_first_question, setup_data):
    # Arrange
    mock_get_or_create_first_question.return_value = MagicMock(id=1)
    mock_url_for.return_value = '/study'
    selected_topic = 'topic'
    conversation_id = 1

    # Act
    result = handle_post_request(selected_topic, conversation_id)

    # Assert
    mock_get_or_create_first_question.assert_called_once_with(conversation_id, selected_topic)
    mock_url_for.assert_called_once_with('gpt.study', conversation_id=conversation_id, current_question_id=1, current_question=mock_get_or_create_first_question.return_value)
    mock_redirect.assert_called_once_with(mock_url_for.return_value)
    assert result == mock_redirect.return_value

@patch('gpt_app.blueprints.routes.render_template')
def test_handle_get_request(mock_render_template, setup_data):
    # Arrange
    study_conversations = 'study_conversations'
    selected_topic = 'topic'
    form = 'form'
    conversation_id = 1
    mock_render_template.return_value = 'rendered_template'

    # Act
    result = handle_get_request(study_conversations, selected_topic, form, conversation_id)

    # Assert
    mock_render_template.assert_called_once_with('study.html', form=form, conversation_id=conversation_id, study_conversations=study_conversations)
    assert result == 'rendered_template'

def test_load_study_conversations(client):
    rv = client.get('/topics')
    assert rv.status_code == 200

def test_load_study_conversation(client):
    rv = client.get('/topic/1')
    assert rv.status_code == 200

def test_create_study_conversation(client):
    rv = client.post('/create_study_conversation')
    assert rv.status_code == 200

def test_add_questions(client):
    rv = client.get('/add_questions/1')
    assert rv.status_code == 200

def test_question(client):
    rv = client.get('/topic/1/question/1')
    assert rv.status_code == 200

def test_utility_processor():
    result = utility_processor()
    assert isinstance(result, dict)
    assert 'get_previous_question_id' in result

def test_submit_answer(client):
    # Mock data
    data = {
        "question_id": 1,
        "user_choices": ["choice1", "choice2"]
    }
    response = client.post('/submit_answer', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200

def test_get_previous_question_id(client):
    # Mock data
    question_id = 1
    response = client.get(f'/get_previous_question_id/{question_id}')
    assert response.status_code == 200

def test_get_next_question_id(client):
    # Mock data
    question_id = 1
    response = client.get(f'/get_next_question_id/{question_id}')
    assert response.status_code == 200

def test_parse_reasoning():
    # Mock data
    reasoning = "(A,\\Explanation for choice A\\),(B,\\Explanation for choice B\\)"
    expected_output = {
        "A": "Explanation for choice A",
        "B": "Explanation for choice B"
    }
    assert parse_reasoning(reasoning) == expected_output

def test_submit_answer_route_accessible(client):
    response = client.post('/submit_answer', data=json.dumps({"question_id": 1, "user_choices": ["choice1", "choice2"]}), content_type='application/json')
    assert response.status_code == 200

def test_submit_answer_correct_response(client):
    # Assuming there is a question with id 1 in the database
    question = StudyQuestion.query.get(1)
    response = client.post('/submit_answer', data=json.dumps({"question_id": 1, "user_choices": question.correct_answer}), content_type='application/json')
    data = json.loads(response.data)
    assert data['total_correct'] == len(question.correct_answer)
    assert all(value for value in data['user_choices_correctness'].values())

def test_submit_answer_invalid_input(client):
    response = client.post('/submit_answer', data=json.dumps({"question_id": 1, "user_choices": ["invalid_choice"]}), content_type='application/json')
    data = json.loads(response.data)
    assert not any(value for value in data['user_choices_correctness'].values())