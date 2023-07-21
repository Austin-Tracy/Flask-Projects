# Project Management App (pm_app)
pm_app is a Flask-based web application designed to assist users in efficiently managing their projects and tasks. It provides a convenient and user-friendly platform for project management activities, allowing you to focus on what matters: getting things done.

## Features
pm_app is feature-rich and offers the following capabilities:

- **User authentication**: Sign in to your account and securely log out when finished.
- **Project management**: Create, view, edit, and delete projects easily.
- **Task management**: Manage tasks within projects, with the ability to create, view, edit, and delete tasks.
- **Task history**: View the history of changes made to any task, providing full transparency.
- **User activity tracking**: Monitor user login activities, a crucial feature for team collaboration.
- **User profile management**: Users have the flexibility to update their profile information at any time.

## Forms
pm_app uses a variety of forms for different operations, these include:

- **LoginForm**: Used for user authentication during login.
- **RegistrationForm**: Used for registering new users to the application.
- **ProjectForm**: Used for creating new projects.
- **TaskForm**: Used for creating new tasks within projects.
- **EditTaskForm**: Used for updating the details of existing tasks.
- **EditProjectForm**: Used for updating the details of existing projects.
- **ProfileForm**: Used for updating user's profile information.

## Models
pm_app uses several models to represent various data entities:

- **Project**: Represents a project, with attributes like ID, name, description, timeline, and associated tasks.
- **Task**: Represents a task, with details such as ID, title, description, deadline, status, and associated project.
- **TaskHistory**: Represents the history of a task, capturing every change made to it.
- **User**: Represents a user, with information such as ID, first name, last name, username, email, phone number, hashed password, associated projects, and tasks.
- **UserHistory**: Represents a user's activity history within the app.

## Routes
pm_app is organized into various routes for smooth navigation:

- `'/'`: Displays the user's projects and tasks on the main page.
- `'/login'`: Access the login page for the application.
- `'/create_project'`: Form page for creating a new project.
- `'/create_task'` & `'/create_task/<int:project_id>'`: Form pages for creating a new task, either standalone or within a specific project.
- `'/task/<int:task_id>'`: View the details of a specified task.
- `'/edit_task/<int:task_id>'`: Form page for editing a specified task.
- `'/project/<int:project_id>'`: View the details of a specified project along with its associated tasks.
- `'/project/<int:project_id>/edit`: Form page for editing a specified project.
- `'/profile'`: Form page for editing user's profile information.
- `'/delete_project/<int:project_id>'`: Deletes a specified project (if the user is authorized).
- `'/delete_task/<int:task_id>'`: Deletes a specified task (if the user is authorized).

## Testing
Several tests are included with pm_app, including tests for task creation, attribute assignment, task history relationships, and more.

## License
pm_app is released under the terms of the MIT license.