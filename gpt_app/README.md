# Study Application

This is a GPT application developed to manage and create interactive study conversations. The application can create, retrieve, and manage conversations, and generate study questions for a given conversation. The application also allows the user to input any topic area of interest and create new questions.

## Table of Contents
- [Features](#features)
- [Usage](#usage)
- [Tests](#tests)
- [Utilities](#utilities)

### Conversation Management

- `get_study_conversation(conversation_id: int) -> StudyConversation`: Retrieves a study conversation by its ID.
- `get_study_conversation_name(conversation_id: int) -> str`: Retrieves the name of a study conversation by its ID.
- `get_all_study_conversations_dict() -> dict`: Returns a dictionary of all study conversations.
- `get_all_study_conversations() -> List[StudyConversation]`: Retrieves all study conversations.
- `get_latest_study_conversation_id() -> int`: Retrieves the ID of the most recent study conversation.
- `insert_study_conversation(name: str) -> StudyConversation`: Inserts a new study conversation into the database.

### Question Management

- `is_duplicate_study_question(conversation_id: int, gpt_question: str) -> bool`: Checks if a study question with the same conversation ID and GPT question already exists.
- `get_study_question(question_id: int) -> StudyQuestion`: Retrieves a study question by its ID.
- `get_latest_study_question(conversation_id: int) -> StudyQuestion`: Retrieves the latest study question for a conversation.
- `get_all_study_questions(conversation_id: int) -> List[StudyQuestion]`: Retrieves all study questions for a conversation.
- `get_all_study_gpt_questions(conversation_id: int) -> List[str]`: Retrieves all GPT questions for a conversation.
- `insert_study_question(gpt_question: str, formatted_gpt_response: str, conversation_id: int, is_multiple_choice: bool, choices: List[List[str]], correct_answer: str, question_reason: str) -> StudyQuestion`: Inserts a new study question into the database.
- `insert_study_questions(results) -> StudyQuestion`: Inserts multiple study questions into the database.

### Forms

- `CreateStudyConversationForm`: A FlaskForm class for creating a new study conversation.
- `StudyConversationFormSingleChoice`: A FlaskForm class for a study conversation with single choice questions.
- `StudyConversationFormMultipleChoice`: A FlaskForm class for a study conversation with multiple choice questions.

### Views

- `study(conversation_id: int) -> str`: Loads the study page.
- `initialize_study_data(conversation_id: int) -> tuple`: Initializes the data for the study page.
- `get_or_create_first_question(conversation_id: int, study_conversation: StudyConversation) -> StudyQuestion`: Gets or creates the first question for the study page.
- `handle_post_request(selected_topic: str, conversation_id: int) -> redirect`: Handles a POST request to the study page.
- `handle_get_request(study_conversations, selected_topic: str, form, conversation_id: int) -> The rendered template`: Handles a GET request to the study page.
- `load_study_conversations() -> str`: Loads all study conversations.
- `load_study_conversation(conversation_id: int) -> Response`: Loads the selected study conversation.
- `create_study_conversation() -> Response`: Creates a new study conversation.
- `question(conversation_id: int, question_id: int) -> Response`: Loads the question page.
- `submit_answer() -> dict`: Submits user's answer and gets the correct answer and reasoning.

## Tests

- `test_study_conversation_creation()`: Test the creation of a StudyConversation instance.
- `test_study_conversation_attributes()`: Test the assignment of attributes to a StudyConversation instance.
- `test_study_conversation_study_question_relationship()`: Test the relationship between StudyConversation and StudyQuestion.

## Utilities

- `generate_keywords(question_list: list) -> list`: Generates keywords from a list of questions.
- `get_turbo_gpt_response(user_input: str) -> openai.openai_object.OpenAIObject:` Sends a prompt to OpenAI's GPT-3 API using the Turbo model and returns the response.
- `debug_gpt_response_string(response: str, verbose: bool = False) -> str:` Formats the response and offers verbose debug if 'verbose' flag is set to True.
- `get_gpt_response(prompt: str) -> dict`: Sends a prompt to OpenAI's GPT-3 API and returns the response.
- `generate_study_questions(conversation_id: int, selected_topic: str, verbose: bool = False) -> List[Dict[str, Union[str, Dict[str, str]]]]:`: Generates 5 study questions for a given topic.

## Logging

Logging functionality is included in the application. Logs are recorded in a file named `stderr.log` located in the `gpt_app/logs` directory, with the logging level set to DEBUG.

## Running the Application

To run the application, navigate to the root directory and use the following command:

```bash
flask run
```

**Note**: This application is designed for educational and demonstration purposes. It should not be used for making actual predictions in a production environment.

## License
This project is licensed under the terms of the MIT license.