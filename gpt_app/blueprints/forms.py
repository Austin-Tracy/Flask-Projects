# gpt_app/blueprints/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class CreateStudyConversationForm(FlaskForm):
    """
    A FlaskForm class for creating a new study conversation.

    Attributes:
    - name (StringField): a field for the user to input the conversation name
    - submit (SubmitField): a submit button for the form
    """
    name = StringField('New Topic', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class StudyConversationFormSingleChoice(FlaskForm):
    """
    A FlaskForm class for a study conversation with single choice questions.

    Attributes:
    - conversation_id (HiddenField): a hidden field for the conversation ID
    - question_id (HiddenField): a hidden field for the question ID
    - name (StringField): a field for the user to input the conversation name
    - question (RadioField): a field for the user to select a single choice question
    - submit (SubmitField): a submit button for the form
    """
    conversation_id = HiddenField("Conversation ID", validators=[DataRequired()])
    question_id = HiddenField("Question ID", validators=[DataRequired()])
    name = StringField("Conversation Name:", validators=[DataRequired(), Length(max=100)])
    question = RadioField('Question', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')

    @property
    def choices(self: FlaskForm) -> list:
        """
        Returns the choices for the question field.

        Returns:
        - list: the choices for the question field
        """
        return self.question.choices

    @choices.setter
    def choices(self, choices_list: list) -> None:
        """
        Sets the choices for the question field.

        Args:
        - choices_list (list): the list of choices to set for the question field
        """
        self.question.choices = choices_list

class StudyConversationFormMultipleChoice(FlaskForm):
    """
    A FlaskForm class for a study conversation with multiple choice questions.

    Attributes:
    - conversation_id (HiddenField): a hidden field for the conversation ID
    - question_id (HiddenField): a hidden field for the question ID
    - name (StringField): a field for the user to input the conversation name
    - question (SelectMultipleField): a field for the user to select multiple choice questions
    - submit (SubmitField): a submit button for the form
    """
    conversation_id = HiddenField("Conversation ID", validators=[DataRequired()])
    question_id = HiddenField("Question ID", validators=[DataRequired()])
    name = StringField("Conversation Name:", validators=[DataRequired(), Length(max=100)])
    question = SelectMultipleField('Question', validators=[DataRequired(), Length(min=2)])
    # add validators to choices to make sure at least one choice is selected
    
    submit = SubmitField('Submit', )

    @property
    def choices(self: FlaskForm) -> list:
        """
        Returns the choices for the question field.

        Returns:
        - list: the choices for the question field
        """
        # make sure a choice is selected before submitting form
        return self.question.choices

    @choices.setter
    def choices(self, choices_list: list) -> None:
        """
        Sets the choices for the question field.

        Args:
        - choices_list (list): the list of choices to set for the question field
        """
        self.question.choices = choices_list

