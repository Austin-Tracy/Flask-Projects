# pm_app/blueprints/routes.py
from flask import render_template, url_for, flash, redirect, request, abort, make_response, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from typing import Optional
from pm_app import db
from pm_app.blueprints import bp
from pm_app.blueprints.forms import LoginForm, RegistrationForm, ProjectForm, TaskForm, EditTaskForm, EditProjectForm, ProfileForm
from pm_app.models.user import User
from pm_app.models.project import Project, generateTimeline
from pm_app.models.task import Task
from pm_app.models.task_history import TaskHistory
from pm_app.models.user_history import UserHistory
from dateutil.parser import parse
from datetime import timedelta, datetime

@bp.route('/')
@login_required
def index() -> str:
    """
    The main page of the web application.

    Displays the user's projects and tasks.

    Returns:
        The rendered HTML template for the index page.
    """
    if not current_user.is_authenticated:
        current_app.logger.error('User not authenticated. Redirecting to login page.')
        return redirect(url_for('main.login'))
    else:
        current_app.logger.info(f'User {current_user.username} authenticated.')
    projects = current_user.projects.all()
    tasks = current_user.tasks.order_by(Task.deadline.asc()).all()
    return render_template("index.html", projects=projects, tasks=tasks)


@bp.route('/welcome')
def welcome() -> str:
    """
    The welcome page for the web application.

    Returns:
        The rendered HTML template for the welcome page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('welcome.html')


@bp.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """
    The login page for the web application.

    Users can log in with their username and password.

    Returns:
        The rendered HTML template for the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data,
                   duration=timedelta(days=7))

        # Collect the data and store it in the UserHistory model
        timestamp = datetime.utcnow()
        activity_data = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'timestamp': timestamp,
            'requested_url': request.url,
            'referrer_url': request.headers.get('Referer')
        }
        print(activity_data)

        user_history = UserHistory(ip_address=activity_data['ip_address'],
                                   user_agent=activity_data['user_agent'],
                                   timestamp=activity_data['timestamp'],
                                   requested_url=activity_data['requested_url'],
                                   referrer_url=activity_data['referrer_url'],
                                   user_id=current_user.id
                                   )
        user.user_activity.append(user_history)

        db.session.add(user)
        db.session.commit()

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@bp.route("/logout")
def logout() -> str:
    """
    The logout page for the web application.

    Users can log out from their account.

    Returns:
        A redirect to the welcome page.
    """
    logout_user()
    return redirect(url_for('main.welcome'))


@bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    The registration page for the web application.

    Users can create a new account with their email, username, and password.

    Returns:
        The rendered HTML template for the registration page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print(f"User registered: {user}")  # Add this line
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    """
    Renders a page with a form to create a new project, and creates the project when the form is submitted.

    Returns:
        A redirect to the user's index page after creating the project.
    """
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!')
        return redirect(url_for('main.index'))
    return render_template('create_project.html', title='Create Project', form=form)


@bp.route('/create_task', methods=['GET', 'POST'])
@bp.route('/create_task/<int:project_id>', methods=['GET', 'POST'])
@login_required
def create_task(project_id: Optional[int] = None) -> str:
    """
    Renders a page with a form to create a new task, and creates the task when the form is submitted.

    Args:
        project_id (int, optional): ID of the project to which the task belongs. Defaults to None.

    Returns:
        A redirect to the user's index page after creating the task.
    """
    form = TaskForm()
    form.project_id.choices = [(project.id, project.name)
                               for project in current_user.projects.all()]

    if project_id:
        form.project_id.default = project_id
        form.process()

    if form.validate_on_submit():
        try:
            deadline = parse(form.deadline.data)  # Parse the date string
        except ValueError:
            current_app.logger.error('Invalid date format. Please try again.')
            flash('Invalid date format. Please try again.')
            return render_template('create_task.html', title='Create Task', form=form)

        task = Task(title=form.title.data, description=form.description.data,
                    deadline=deadline, user_id=current_user.id, project_id=form.project_id.data)
        db.session.add(task)
        db.session.commit()
        Project.update_timeline(form.project_id.data)
        flash('Task created successfully!')
        return redirect(url_for('main.index'))

    return render_template('create_task.html', title='Create Task', form=form)


@bp.route('/task/<int:task_id>')
@login_required
def task(task_id: int) -> str:
    """
    Renders a page with details of the specified task.

    Args:
        task_id (int): ID of the task to display.

    Returns:
        A page with details of the specified task.
    """
    task = Task.query.get_or_404(task_id)
    task_history = TaskHistory.query.filter_by(task_id=task_id).order_by(TaskHistory.date.desc()).all()
    if not task.history:
        task.history = []
    return render_template('task.html', title='Task Details', task=task, project=task.project, task_history=task_history)


@bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id: int) -> str:
    """
    Renders a page with a form to edit the specified task, and updates the task when the form is submitted.

    Args:
        task_id (int): ID of the task to edit.

    Returns:
        A redirect to the task's details page after editing the task.
    """
    task = Task.query.get_or_404(task_id)
    form = EditTaskForm()

    form.project_id.choices = [(project.id, project.name)
                               for project in current_user.projects.all()]

    if form.validate_on_submit():
        try:
            deadline = parse(
                form.deadline.data) if form.deadline.data else None
        except ValueError:
            current_app.logger.error('Invalid date format. Please try again.')
            flash('Invalid date format. Please try again.')
            return render_template('edit_task.html', title='Edit Task', form=form, task=task)

        # Store the changes in the TaskHistory model
        changes = []

        if task.title != form.title.data:
            changes.append(TaskHistory(task_id=task.id, attribute='Title',
                           old_value=task.title, new_value=form.title.data))
            task.title = form.title.data

        if task.description != form.description.data:
            changes.append(TaskHistory(task_id=task.id, attribute='Description',
                           old_value=task.description, new_value=form.description.data))
            task.description = form.description.data

        if task.deadline != deadline:
            old_deadline = task.deadline.strftime(
                '%Y-%m-%d %H:%M') if task.deadline else ""
            new_deadline = deadline.strftime(
                '%Y-%m-%d %H:%M') if deadline else ""
            changes.append(TaskHistory(task_id=task.id, attribute='Deadline',
                           old_value=old_deadline, new_value=new_deadline))
            task.deadline = deadline

        if task.project_id != form.project_id.data:
            old_project = Project.query.get(task.project_id).name
            new_project = Project.query.get(form.project_id.data).name
            changes.append(TaskHistory(task_id=task.id, attribute='Project',
                           old_value=old_project, new_value=new_project))
            task.project_id = form.project_id.data

        if task.status != form.status.data:
            changes.append(TaskHistory(task_id=task.id, attribute='Status',
                           old_value=str(task.status), new_value=str(form.status.data)))
            task.status = form.status.data

        for change in changes:
            db.session.add(change)

        db.session.commit()

        if changes:
            Project.update_timeline(form.project_id.data)
            flash('Task updated successfully!')
        else:
            flash('No changes detected.')
        return redirect(url_for('main.task', task_id=task.id))

    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.deadline.data = task.deadline.strftime(
            '%Y-%m-%d %H:%M') if task.deadline else ""
        form.project_id.data = task.project_id
        form.status.data = task.status

    return render_template('edit_task.html', title='Edit Task', form=form, task=task)


@bp.route('/project/<int:project_id>')
@login_required
def project(project_id: int) -> str:
    """
    Renders the details of a project, along with the tasks associated with it.

    Args:
        project_id (int): The ID of the project whose details are to be rendered.

    Returns:
        str: The rendered HTML template.
    """
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).order_by(Task.deadline.asc()).all()
    if not tasks:
        flash('No tasks found for this project.')
        return render_template('project.html', title='Project Details', project=project, tasks=[], timeline=None)
    else:
        tasks_data = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else "",
                'url': url_for('main.task', task_id=task.id)
            }
            tasks_data.append(task_data)

        if project.timeline_html == None:
            project.timeline_html = generateTimeline(tasks_data)
            db.session.commit()
        timeline = project.timeline_html
        return render_template('project.html', title='Project Details', project=project, tasks=tasks_data, timeline=timeline)


@bp.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id: int)-> str:
    """
    Allows the user to edit the details of a project.

    Args:
        project_id (int): The ID of the project to be edited.

    Returns:
        str: The rendered HTML template.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    form = EditProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash("Project has been updated!", "success")
        return redirect(url_for("main.project", project_id=project.id))
    elif request.method == "GET":
        form.name.data = project.name
        form.description.data = project.description
    return render_template("edit_project.html", form=form, project_id=project.id)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile() -> str:
    """
    Allows the user to edit their profile information.

    Returns:
        str: The rendered HTML template.
    """
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phonenumber = form.phonenumber.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
    
        resp = make_response(redirect(url_for('main.index')))

        return resp
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phonenumber.data = current_user.phonenumber
    return render_template('profile.html', title='Profile', form=form)


@bp.route('/delete_project/<int:project_id>')
@login_required
def delete_project(project_id: int) -> redirect:
    """Deletes the project with the given ID from the database, if the user is authorized.

    Args:
        project_id (int): The ID of the project to be deleted.

    Returns:
        redirect: Redirects to the home page after deleting the project.

    Raises:
        403: If the user is not authorized to delete the project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    tasks = Task.query.filter_by(project_id=project_id).all()
    if tasks:
        for task in tasks:
            db.session.delete(task)
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted.')
    return redirect(url_for('main.index'))

@bp.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id: int) -> redirect:
    """Deletes the task with the given ID from the database, if the user is authorized.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        redirect: Redirects to the home page after deleting the task.

    Raises:
        403: If the user is not authorized to delete the task.
    """
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    
    project = Project.query.get_or_404(task.project_id)
    project.timeline_html = None
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.')
    return redirect(url_for('main.index'))


