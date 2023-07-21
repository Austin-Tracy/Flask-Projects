# pm_app/models/task.py
from pm_app import db

class Task(db.Model):
    """
    Model class for tasks.
    
    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Description of the task.
        deadline (datetime): Deadline for the task.
        status (bool): Status of the task.
        project_id (int): Foreign key reference to the project the task belongs to.
        user_id (int): Foreign key reference to the user who created the task.
        history (relationship): Relationship to the task history.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    
    # Add a foreign key to the User model
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Add history field
    history = db.relationship('TaskHistory', backref='task', lazy='dynamic')