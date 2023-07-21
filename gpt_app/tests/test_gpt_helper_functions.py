import pytest
from gpt_app.blueprints.database import is_duplicate_study_question
from utils.helper_functions import generate_study_questions, debug_gpt_response_string
from gpt_app.utils.helper_functions import generate_keywords

@pytest.fixture
def generate_study_questions_fixture():
    return [
        {
            "1": {
                "Question": "What is the capital of France?",
                "Options": {
                    "A": {"Text": "Paris", "Reason": "Paris is the capital of France.", "Correct": "True"},
                    "B": {"Text": "London", "Reason": "London is the capital of England, not France.", "Correct": "False"},
                    "C": {"Text": "Berlin", "Reason": "Berlin is the capital of Germany, not France.", "Correct": "False"},
                    "D": {"Text": "Madrid", "Reason": "Madrid is the capital of Spain, not France.", "Correct": "False"},
                    "E": {"Text": "Rome", "Reason": "Rome is the capital of Italy, not France.", "Correct": "False"},
                }
            }
        }
    ]

def test_generate_study_questions(generate_study_questions_fixture):
    result = generate_study_questions(1, "Geography", False)
    assert result == generate_study_questions_fixture

def test_debug_gpt_response_string():
    response = "[{\"1\": {\"Question\": \"What is the capital of France?\", \"Options\": {\"A\": {\"Text\": \"Paris\", \"Reason\": \"Paris is the capital of France.\", \"Correct\": \"True\"}, \"B\": {\"Text\": \"London\", \"Reason\": \"London is the capital of England, not France.\", \"Correct\": \"False\"}, \"C\": {\"Text\": \"Berlin\", \"Reason\": \"Berlin is the capital of Germany, not France.\", \"Correct\": \"False\"}, \"D\": {\"Text\": \"Madrid\", \"Reason\": \"Madrid is the capital of Spain, not France.\", \"Correct\": \"False\"}, \"E\": {\"Text\": \"Rome\", \"Reason\": \"Rome is the capital of Italy, not France.\", \"Correct\": \"False\"}}}}]"
    result = debug_gpt_response_string(response, False)
    assert result == response

def test_is_duplicate_study_question():
    assert is_duplicate_study_question(1, "What is the capital of France?") == False

def test_generate_keywords_returns_list():
    result = generate_keywords(["This is a test question"])
    assert isinstance(result, list), "The result should be a list."

def test_generate_keywords_returns_list_of_strings():
    result = generate_keywords(["This is a test question"])
    assert all(isinstance(item, str) for item in result), "All items in the result should be strings."

def test_generate_keywords_removes_stop_words():
    result = generate_keywords(["This is a test question"])
    assert "is" not in ' '.join(result), "The stop word 'is' should be removed."

def test_generate_keywords_generates_bigrams():
    result = generate_keywords(["This is a test question"])
    assert "test question" in result, "The bigram 'test question' should be in the result."

def test_generate_keywords_handles_empty_list():
    result = generate_keywords([])
    assert result == [], "The result should be an empty list when the input is an empty list."