import pytest
from wtforms.validators import ValidationError
from datetime import datetime, timedelta
from pm_app import create_app, db
from pm_app.models.user import User, load_user
from pm_app.models.project import Project, generateTimeline
from pm_app.models.task import Task
from pm_app.models.task_history import TaskHistory
from pm_app.models.user_history import UserHistory

######### User Tests #########
def test_set_password():
    user = User(username='test', email='test@test.com')
    user.set_password('testpassword')
    assert user.password_hash is not None
    assert user.password_hash != 'testpassword'

def test_check_password():
    user = User(username='test', email='test@test.com')
    user.set_password('testpassword')
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')

def test_validate_username():
    user1 = User(username='test', email='test@test.com')
    user2 = User(username='test', email='test2@test.com')
    with pytest.raises(ValidationError):
        user2.validate_username(user2.username)
    with pytest.raises(ValidationError):
        user2.validate_username('a')
    with pytest.raises(ValidationError):
        user2.validate_username('a'*21)

def test_repr():
    user = User(username='test', email='test@test.com')
    assert repr(user) == '<User test>'

@pytest.fixture
def user(db):
    user = User(username='test', email='test@test.com')
    db.session.add(user)
    db.session.commit()
    return user

def test_load_user(user, db):
    loaded_user = load_user(user.id)
    assert loaded_user == user

def test_load_user():
    user = User(username='testuser', email='testuser@example.com')
    db.session.add(user)
    db.session.commit()
    loaded_user = load_user(user.id)
    assert loaded_user == user

def test_load_user_invalid_id():
    loaded_user = load_user(999)
    assert loaded_user is None


########## Project Tests ##########
@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
        yield test_client

    db.session.remove()
    db.drop_all()

def test_repr(test_client):
    project = Project(name="Test Project", description="This is a test project.")
    assert repr(project) == "<Project Test Project>"

def test_update_timeline(test_client):
    project = Project(name="Test Project", description="This is a test project.")
    db.session.add(project)
    db.session.commit()

    task = Task(title="Test Task", description="This is a test task.", project_id=project.id)
    db.session.add(task)
    db.session.commit()

    project.update_timeline(project.id)
    assert project.timeline_html is not None

def test_generateTimeline(test_client):
    tasks = [{'id': 1, 'title': 'Test Task', 'description': 'This is a test task.', 'status': True, 'deadline': '2022-12-31 23:59', 'url': '/task/1'}]
    timeline_html = generateTimeline(tasks)
    assert timeline_html is not None

########### Task Tests ###########
def test_task_creation():
    """
    Test the creation of a Task instance.
    """
    task = Task(title="Test Task", description="This is a test task", deadline="2022-12-31 23:59:59")
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.deadline == "2022-12-31 23:59:59"
    assert task.status == False

def test_task_attributes():
    """
    Test the assignment of attributes to a Task instance.
    """
    task = Task()
    task.title = "New Task"
    task.description = "This is a new task"
    task.deadline = "2022-12-31 23:59:59"
    task.status = True
    assert task.title == "New Task"
    assert task.description == "This is a new task"
    assert task.deadline == "2022-12-31 23:59:59"
    assert task.status == True

def test_task_history_relationship():
    """
    Test the relationship between Task and TaskHistory.
    """
    task = Task(title="Test Task", description="This is a test task", deadline="2022-12-31 23:59:59")
    task_history = TaskHistory(task_id=task.id, status="Created")
    task.history.append(task_history)
    assert task.history[0] == task_history

######## User History Tests ########
def test_user_history_creation():
    # Create a UserHistory instance
    user_history = UserHistory(
        id=1,
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0',
        requested_url='http://localhost:5000',
        referrer_url='http://localhost:5000/login',
        user_id=1
    )

    # Assert that the instance is of type UserHistory
    assert isinstance(user_history, UserHistory)

def test_user_history_attributes():
    # Create a UserHistory instance
    user_history = UserHistory(
        id=1,
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0',
        requested_url='http://localhost:5000',
        referrer_url='http://localhost:5000/login',
        user_id=1
    )

    # Assert that the attributes are assigned correctly
    assert user_history.id == 1
    assert user_history.ip_address == '192.168.1.1'
    assert user_history.user_agent == 'Mozilla/5.0'
    assert user_history.requested_url == 'http://localhost:5000'
    assert user_history.referrer_url == 'http://localhost:5000/login'
    assert user_history.user_id == 1

def test_user_history_timestamp():
    # Create a UserHistory instance
    user_history = UserHistory(
        id=1,
        ip_address='192.168.1.1',
        user_agent='Mozilla/5.0',
        requested_url='http://localhost:5000',
        referrer_url='http://localhost:5000/login',
        user_id=1
    )

    # Assert that the timestamp is assigned a default value
    assert isinstance(user_history.timestamp, datetime)
    assert datetime.utcnow() - user_history.timestamp < timedelta(seconds=1)

########## Task History Tests ##########
def test_task_history_creation():
    """
    Test the creation of a TaskHistory object.
    """
    task_history = TaskHistory(
        task_id=1,
        date=datetime.utcnow(),
        attribute='status',
        old_value='in progress',
        new_value='completed'
    )

    assert task_history.task_id == 1
    assert task_history.attribute == 'status'
    assert task_history.old_value == 'in progress'
    assert task_history.new_value == 'completed'

def test_task_history_repr():
    """
    Test the __repr__ method of the TaskHistory object.
    """
    task_history = TaskHistory(
        task_id=1,
        date=datetime.utcnow(),
        attribute='status',
        old_value='in progress',
        new_value='completed'
    )

    assert repr(task_history) == '<TaskHistory 1 status>'