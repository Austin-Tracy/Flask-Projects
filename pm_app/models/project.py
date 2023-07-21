# pm_app/models/project.py
from pm_app import db
from pm_app.models.task import Task
from flask import url_for
import pandas as pd
import plotly.express as px


class Project(db.Model):
    """A class representing a project.

    Attributes:
        id (int): The unique identifier of the project.
        name (str): The name of the project.
        description (str): The description of the project.
        timeline_html (str): The HTML representation of the project timeline.
        user_id (int): The user ID of the owner of the project.
        tasks (relationship): A relationship to the tasks associated with the project.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    timeline_html = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tasks = db.relationship("Task", backref="project", lazy="dynamic")

    def __repr__(self):
        """Return a string representation of the project."""
        return f"<Project {self.name}>"
    
    def update_timeline(project_id):
        """Update the timeline HTML for the given project.

        Args:
            project_id (int): The ID of the project to update.

        Returns:
            None
        """
        project = Project.query.get_or_404(project_id)
        tasks = Task.query.filter_by(project_id=project_id).all()

        tasks_data = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'deadline': task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else "",
                'url': url_for('main.task', task_id=task.id)
            }
            tasks_data.append(task_data)
        timeline_html = generateTimeline(tasks_data)
        project.timeline_html = timeline_html
        db.session.commit()

def generateTimeline(tasks):
    """
    Generates an HTML timeline of tasks using Plotly.

    Args:
        tasks (list): A list of dictionaries, each containing information about a task.

    Returns:
        str: The HTML code for the Plotly graph.
    """
    df = pd.DataFrame(tasks)
    df['deadline'] = pd.to_datetime(df['deadline'])
    df = df.sort_values('deadline')
    df['size'] = df['deadline'].apply(lambda x: 20 if x < pd.Timestamp.now() else 20 - (x - pd.Timestamp.now()).days if (20 - (x - pd.Timestamp.now()).days) > 0 else 3)
    color_map = {True: 'green', False: 'red'}

    # Group tasks by deadline and calculate y positions
    df['y'] = df.groupby('deadline').cumcount() + 1

    # Create a scatter plot
    fig = px.scatter(df, x='deadline', y='y', color='status', color_discrete_map=color_map, hover_data=['title', 'description'], title='Task Timeline', size='size')

    # Add task title as hovertext and set the custom hovertemplate
    fig.update_traces(hovertext=df['title'].values, hovertemplate="<b>%{hovertext}</b><br>Deadline: %{x}<br>Description: %{customdata[1]}<extra></extra>")

    # Set the axis labels and hide y-axis labels and ticks
    fig.update_layout(xaxis_title='Deadline', yaxis_title='', showlegend=False, yaxis=dict(showticklabels=False, zeroline=False, showgrid=False))

    # Set the range of the x-axis
    min_date = min(df['deadline'].min() - pd.Timedelta(days=1), pd.Timestamp.now() - pd.Timedelta(days=1))
    max_date = max(df['deadline'].max() + pd.Timedelta(days=1), pd.Timestamp.now() + pd.Timedelta(days=1))
    fig.update_xaxes(range=[min_date, max_date], tickformat='%b %d')

    # Add a vertical line to indicate the current date, as well as a label just above the line
    fig.add_vline(x=pd.Timestamp.now().date(), line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(x=pd.Timestamp.now().date(), y=1.00, text=pd.Timestamp.now().date().strftime('%b %d'), showarrow=True, xref="x", yref="paper", font=dict(color="black"))

    # Add a horizontal line at y = 1 with a layer below the points
    max_size = df['size'].max()
    fig.add_hline(y = 1 - max_size / 2, line_width=1, line_dash="solid", line_color="black", layer='below')

    # Return the HTML code for the Plotly graph
    return fig.to_html(full_html=False)