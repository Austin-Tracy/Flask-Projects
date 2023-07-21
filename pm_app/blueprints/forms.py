# /pm_app/blueprints/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from pm_app.models.user import User

class LoginForm(FlaskForm):
    """
    A class representing the login form.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        remember_me (bool): Whether to remember the user or not.
        submit (str): The text on the login button.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    """
    A class representing the registration form.

    Attributes:
        username (str): The desired username.
        email (str): The email address of the user.
        password (str): The desired password.
        password_confirm (str): The repeated password for confirmation.
        submit (str): The text on the registration button.
    """
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username: str) -> None:
        """
        Validates that the username is not already taken.

        Args:
            username (str): The desired username.

        Raises:
            ValidationError: If the username is already taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken. Please choose a different one.")

    def validate_email(self, email: str) -> None:
        """
        Validates that the email address is not already in use.

        Args:
            email (str): The email address entered by the user.

        Raises:
            ValidationError: If the email address is already in use.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please use a different one.")

class ProjectForm(FlaskForm):
    """
    A class representing the form for creating a new project.

    Attributes:
        name (str): The name of the project.
        description (str): A description of the project.
        submit (str): The text on the submit button.
    """
    name = StringField("Project Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Create Project")

class TaskForm(FlaskForm):
    """
    A class representing the form for creating a new task.

    Attributes:
        title (str): The title of the task.
        description (str): A description of the task.
        deadline (str): The deadline for the task.
        project_id (int): The ID of the project that the task belongs to.
        submit (str): The text on the submit button.
    """
    title = StringField("Task Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    deadline = StringField("Deadline")  # Use StringField instead of DateTimeField
    project_id = SelectField("Project", coerce=int)  # Add this field
    submit = SubmitField("Create Task")

class EditTaskForm(FlaskForm):
    """
    A class representing the form for editing a task.

    Attributes:
        title (str): The title of the task.
        description (str): A description of the task.
        deadline (str): The deadline for the task.
        status (bool): Whether the task is completed or not.
        project_id (int): The ID of the project that the task belongs to.
        submit (str): The text on the submit button.
    """
    title = StringField("Task Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    deadline = StringField("Deadline")
    status = BooleanField('Status (Completed)', default=False)
    project_id = SelectField("Project", coerce=int)
    submit = SubmitField("Update Task")

class EditProjectForm(FlaskForm):
    """
    A class representing the form for editing a project.

    Attributes:
        name (str): The name of the project.
        description (str): A description of the project.
        submit (str): The text on the submit button.
    """
    name = StringField("Project Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Update Project")

class ProfileForm(FlaskForm):
    """
    A class representing the form for updating a user's profile.

    Attributes:
        firstname (str): The user's first name.
        lastname (str): The user's last name.
        email (str): The user's email address.
        phonenumber (str): The user's phone number.
        submit (str): The text on the submit button.
    """
    firstname = StringField("First Name")
    lastname = StringField("Last Name")
    email = StringField("Email", validators=[DataRequired(), Email()])
    phonenumber = StringField("Phone Number")
    dark_mode = BooleanField("Dark Mode")
    submit = SubmitField("Update Profile")

    def validate_email(self, email: str) -> None:
        """
        Validates that the email address is not already in use.

        Args:
            email (str): The email address entered by the user.

        Raises:
            ValidationError: If the email address is already in use.
        """
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != email.data:
            raise ValidationError("Email is already in use. Please use a different one.")
    
