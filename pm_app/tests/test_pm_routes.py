import pytest
import datetime
from flask import url_for, render_template
from pm_app import create_app, db
from pm_app.models.user import User
from pm_app.models.project import Project
from pm_app.models.task import Task
from pm_app.blueprints.routes import task
from pm_app.models.task_history import TaskHistory

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    db.session.remove()
    db.drop_all()

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert "/login" in response.location

    User.query.delete()
    user = User(username='test', email='test@test.com')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    login(client, 'test', 'test')

    response = client.get('/')
    assert response.status_code == 200


def test_welcome(client):
    response = client.get('/welcome')
    assert response.status_code == 200

    User.query.delete()
    user = User(username='test', email='test@test.com')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    login(client, 'test', 'test')

    response = client.get('/welcome')
    assert response.status_code == 302
    assert "/index" in response.location

def test_login_logout(client):
    User.query.delete()
    user = User(username='test', email='test@test.com')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    response = login(client, 'test', 'wrongpassword')
    assert b'Invalid username or password' in response.data

    response = login(client, 'test', 'test')
    assert b'User test authenticated.' in response.data

    response = logout(client)
    assert response.status_code == 302
    assert "/welcome" in response.location


def test_register(client):
    User.query.delete()

    response = client.post('/register', data=dict(
        username='test',
        email='test@test.com',
        password='test',
        password2='test'
    ), follow_redirects=True)
    assert b'Congratulations, you are now a registered user!' in response.data

    response = client.post('/register', data=dict(
        username='test',
        email='test2@test.com',
        password='test',
        password2='test'
    ), follow_redirects=True)
    assert b'Please use a different username.' in response.data

def test_create_project_get(client, auth):
    auth.login()
    response = client.get(url_for('main.create_project'))
    assert response.status_code == 200
    assert b"Create Project" in response.data

def test_create_project_post_valid(client, auth):
    auth.login()
    response = client.post(url_for('main.create_project'), data={'name': 'Test Project', 'description': 'This is a test project'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Project created successfully!" in response.data
    assert b"Test Project" in response.data

def test_create_project_post_invalid(client, auth):
    auth.login()
    response = client.post(url_for('main.create_project'), data={'name': '', 'description': 'This is a test project'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Project created successfully!" not in response.data
    assert b"This field is required." in response.data


def test_task():
    # Create a mock task
    mock_task = Task(id=1, title="Test Task", description="This is a test task", deadline=datetime.now(), user_id=1, project_id=1)
    mock_task_history = [TaskHistory(id=1, date=datetime.now(), event="Created", task_id=1)]

    # Mock the query.get_or_404 method to return the mock task
    Task.query.get_or_404 = lambda id: mock_task if id == 1 else None
    TaskHistory.query.filter_by = lambda task_id: mock_task_history if task_id == 1 else None

    # Call the task function
    result = task(1)

    # Check if the result is as expected
    expected_result = render_template('task.html', title='Task Details', task=mock_task, project=mock_task.project, task_history=mock_task_history)
    assert result == expected_result

def test_edit_task(client, auth):
    # Login as a user
    auth.login()

    # Create a mock task
    mock_task = Task(id=1, title="Test Task", description="This is a test task", deadline=datetime.now(), user_id=1, project_id=1)

    # Mock the query.get_or_404 method to return the mock task
    Task.query.get_or_404 = lambda id: mock_task if id == 1 else None

    # Call the edit_task function
    response = client.get(url_for('main.edit_task', id=1))

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Edit Task" in response.data
    assert b"Test Task" in response.data

def test_edit_task_get_valid(client, auth):
    # Login as a user
    auth.login()

    # Create a mock task
    mock_task = Task(id=1, title="Test Task", description="This is a test task", deadline=datetime.now(), user_id=1, project_id=1)

    # Mock the query.get_or_404 method to return the mock task
    Task.query.get_or_404 = lambda id: mock_task if id == 1 else None

    # Call the edit_task function
    response = client.post(url_for('main.edit_task', id=1), data={'title': 'Test Task 2', 'description': 'This is a test task', 'deadline': datetime.now(), 'status': False}, follow_redirects=True)

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Task updated successfully!" in response.data
    assert b"Test Task 2" in response.data

def test_edit_task_get_invalid(client, auth):
    # Login as a user
    auth.login()

    # Create a mock task
    mock_task = Task(id=1, title="Test Task", description="This is a test task", deadline=datetime.now(), user_id=1, project_id=1)

    # Mock the query.get_or_404 method to return the mock task
    Task.query.get_or_404 = lambda id: mock_task if id == 1 else None

    # Call the edit_task function
    response = client.post(url_for('main.edit_task', id=1), data={'title': '', 'description': 'This is a test task', 'deadline': datetime.now(), 'status': False}, follow_redirects=True)

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Task updated successfully!" not in response.data
    assert b"This field is required." in response.data

def test_delete_task(client, auth):
    # Login as a user
    auth.login()

    # Create a mock task
    mock_task = Task(id=1, title="Test Task", description="This is a test task", deadline=datetime.now(), user_id=1, project_id=1)

    # Mock the query.get_or_404 method to return the mock task
    Task.query.get_or_404 = lambda id: mock_task if id == 1 else None

    # Call the delete_task function
    response = client.get(url_for('main.delete_task', id=1), follow_redirects=True)

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Task deleted successfully!" in response.data
    assert b"Test Task" not in response.data


def test_profile(client):
    login(client, 'test@example.com')
    rv = client.get('/profile')
    assert rv.status_code == 200
    rv = client.post('/profile', data=dict(firstname='New', lastname='Name', email='new@example.com', phonenumber='0987654321'), follow_redirects=True)
    assert 'Your profile has been updated!' in rv.data
    rv = client.post('/profile', data=dict(firstname='', lastname='', email='', phonenumber=''), follow_redirects=True)
    assert 'Error in the form' in rv.data

def test_delete_project(client):
    login(client, 'test@example.com')
    project = Project(user_id=1)
    db.session.add(project)
    db.session.commit()
    rv = client.get(f'/delete_project/{project.id}', follow_redirects=True)
    assert 'Project has been deleted.' in rv.data
    rv = client.get(f'/delete_project/{project.id}', follow_redirects=True)
    assert rv.status_code == 403

def test_delete_task(client):
    login(client, 'test@example.com')
    project = Project(user_id=1)
    db.session.add(project)
    db.session.commit()
    task = Task(user_id=1, project_id=project.id)
    db.session.add(task)
    db.session.commit()
    rv = client.get(f'/delete_task/{task.id}', follow_redirects=True)
    assert 'Task has been deleted.' in rv.data
    rv = client.get(f'/delete_task/{task.id}', follow_redirects=True)
    assert rv.status_code == 403

def test_project(client):
    project = Project(name='Test Project', description='Test Description')
    db.session.add(project)
    db.session.commit()
    response = client.get(f'/project/{project.id}')
    assert response.status_code == 302  # Redirect to login page

def test_edit_project(client):
    project = Project(name='Test Project', description='Test Description')
    db.session.add(project)
    db.session.commit()
    response = client.get(f'/project/{project.id}/edit')
    assert response.status_code == 302  # Redirect to login page