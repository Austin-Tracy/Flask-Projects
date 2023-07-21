# pm_app/models/task_history.py
from pm_app import db
from datetime import datetime

class TaskHistory(db.Model):
    """
    Model class for task history.
    
    Attributes:
        id (int): Unique identifier for the task history.
        task_id (int): Foreign key reference to the task.
        date (datetime): Date when the task history was recorded.
        attribute (str): Attribute that was changed.
        old_value (str): Old value of the attribute.
        new_value (str): New value of the attribute.
    """
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    attribute = db.Column(db.String(64))
    old_value = db.Column(db.String(256))
    new_value = db.Column(db.String(256))

    def __repr__(self) -> str:
        """
        String representation of the task history object.
        """
        return f'<TaskHistory {self.task_id} {self.attribute}>'