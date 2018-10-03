# services/tasks/project/api/models.py

from project import db
from datetime import datetime

class Task(db.Model):
    
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.now)
    link = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    task_type = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    maintainer = db.Column(db.String(128), nullable=True)
    language = db.Column(db.String(128), nullable=True)
    customers_count = db.Column(db.Integer, nullable=False)
    estimated_custmomer_points = db.Column(db.Integer, nullable=True)
    estimated_points = db.Column(db.Integer, nullable=True)
    impact = db.Column(db.Integer, nullable=True)
    confidence = db.Column(db.String(128), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    effort = db.Column(db.String(128), nullable=True)
    date_multiplier = db.Column(db.Integer, nullable=False)

    def __init__(self, creator, link, title="", due_date=None, task_type="", category="",
    maintainer=None, language=None, customers_count=1, estimated_custmomer_points=None,
    estimated_points=None, impact=None, reach=1, effort=None, confidence="",
    date_multiplier=1):
        self.creator = creator
        self.link = link
        self.title = title
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.due_date = due_date
        self.task_type = task_type
        self.category = category
        self.maintainer = maintainer
        self.language = language
        self.customers_count = customers_count
        self.estimated_custmomer_points = estimated_custmomer_points
        self.estimated_points = estimated_points
        self.impact = impact
        self.confidence = confidence
        self.reach = reach
        self.effort = effort
        self.days_to_due = self.calculateDaysToDue(due_date)
        self.date_multiplier = date_multiplier
        self.rice_total = 0

    # Get the number of days to due date
    def calculateDaysToDue(self, due_date):
        ''' The Due date should be in the format MM/DD/YYYY '''
        if due_date and isinstance(due_date, datetime):
            return due_date - datetime.today()
        return None

    def to_json(self):
        return {
            'id': self.id,
            'link': self.link,
            'creator': self.creator,
            'due_date': self.due_date
        }
