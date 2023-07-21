from gpt_app.blueprints.forms import CreateStudyConversationForm, StudyConversationFormSingleChoice, StudyConversationFormMultipleChoice

def test_create_study_conversation_form():
    form = CreateStudyConversationForm()
    assert form.name.label.text == "New Topic"
    assert form.submit.label.text == "Submit"

def test_study_conversation_form_single_choice():
    form = StudyConversationFormSingleChoice()
    assert form.conversation_id.label.text == "Conversation ID"
    assert form.question_id.label.text == "Question ID"
    assert form.name.label.text == "Conversation Name:"
    assert form.question.label.text == "Question"
    assert form.submit.label.text == "Submit"

def test_study_conversation_form_multiple_choice():
    form = StudyConversationFormMultipleChoice()
    assert form.conversation_id.label.text == "Conversation ID"
    assert form.question_id.label.text == "Question ID"
    assert form.name.label.text == "Conversation Name:"
    assert form.question.label.text == "Question"
    assert form.submit.label.text == "Submit"

def test_choices_property_single_choice():
    form = StudyConversationFormSingleChoice()
    choices = [('1', 'Choice 1'), ('2', 'Choice 2')]
    form.choices = choices
    assert form.choices == choices

def test_choices_property_multiple_choice():
    form = StudyConversationFormMultipleChoice()
    choices = [('1', 'Choice 1'), ('2', 'Choice 2')]
    form.choices = choices
    assert form.choices == choices