import pytest
from unittest.mock import patch
from pm_app.blueprints.forms import LoginForm, RegistrationForm, ProjectForm, TaskForm, EditTaskForm, EditProjectForm, ProfileForm
from pm_app.models.user import User
from pm_app import db, create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    db.session.remove()
    db.drop_all()

def test_login_form():
    form = LoginForm(username="testuser", password="testpassword")
    assert form.validate() == True

def test_registration_form():
    form = RegistrationForm(username="testuser", email="testuser@example.com", password="testpassword", password_confirm="testpassword")
    with patch.object(User, 'query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = None
        assert form.validate() == True

def test_project_form():
    form = ProjectForm(name="Test Project", description="This is a test project.")
    assert form.validate() == True

def test_task_form():
    form = TaskForm(title="Test Task", description="This is a test task.", deadline="2022-12-31", project_id=1)
    assert form.validate() == True

def test_edit_task_form():
    form = EditTaskForm(title="Test Task", description="This is a test task.", deadline="2022-12-31", status=False, project_id=1)
    assert form.validate() == True

def test_edit_project_form():
    form = EditProjectForm(name="Test Project", description="This is a test project.")
    assert form.validate() == True

def test_profile_form():
    form = ProfileForm(firstname="Test", lastname="User", email="testuser@example.com", phonenumber="1234567890", dark_mode=False)
    assert form.validate() == True

def test_registration_form(setup):
    form = RegistrationForm(username='testuser', email='test@example.com', password='password', password_confirm='password')
    assert form.validate() == True

def test_login_form(setup):
    form = LoginForm(email='test@example.com', password='password', remember_me=True)
    assert form.validate() == True

def test_project_form(setup):
    form = ProjectForm(name='Test Project', description='This is a test project.')
    assert form.validate() == True

def test_task_form(setup):
    form = TaskForm(title='Test Task', description='This is a test task.', deadline='2022-12-31', project_id=1)
    assert form.validate() == True

def test_edit_task_form(setup):
    form = EditTaskForm(title='Test Task', description='This is a test task.', deadline='2022-12-31', status=False, project_id=1)
    assert form.validate() == True

def test_edit_project_form(setup):
    form = EditProjectForm(name='Test Project', description='This is a test project.')
    assert form.validate() == True

def test_profile_form(setup):
    form = ProfileForm(firstname='Test', lastname='User', email='test@example.com', phonenumber='1234567890', dark_mode=False)
    assert form.validate() == True

