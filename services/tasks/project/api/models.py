# services/tasks/project/api/models.py

from project import db
from datetime import datetime


class Task(db.Model):


    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    updated_locally_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
    url = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    task_type = db.Column(db.String(128), nullable=True)
    category = db.Column(db.String(128), nullable=True)
    maintainer = db.Column(db.String(128), nullable=True)
    language = db.Column(db.String(128), nullable=True)
    customer_count = db.Column(db.Integer, nullable=True)
    estimated_customer_points = db.Column(db.Integer, nullable=True)
    estimated_points = db.Column(db.Integer, nullable=True)
    impact = db.Column(db.Float, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    reach = db.Column(db.Float, nullable=True)
    effort = db.Column(db.Float, nullable=True)
    rice_total = db.Column(db.Float, nullable=True)
    date_multiplier = db.Column(db.Integer, nullable=True)
    labels = db.Column(db.ARRAY(db.String(255)), nullable=True)
    num_of_comments = db.Column(db.Integer, nullable=True)
    num_of_reactions = db.Column(db.Integer, nullable=True)

    def __init__(self,
                 creator,
                 url,
                 created_at=datetime.utcnow(),
                 updated_at=datetime.utcnow(),
                 updated_locally_at=None,
                 title="",
                 due_date=None, 
                 task_type="",
                 category="",
                 maintainer=None,
                 language=None,
                 customer_count=1,
                 estimated_customer_points=None,
                 estimated_points=None,
                 impact=0, reach=0,
                 effort=0,
                 confidence=0,
                 labels=None,
                 date_multiplier=1,
                 num_of_comments=0,
                 num_of_reactions=0,
                 rice_total=0):
        self.creator = creator
        self.url = url
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
        self.updated_locally_at = updated_locally_at
        self.due_date = due_date
        self.task_type = task_type
        self.category = category
        self.maintainer = maintainer
        self.labels = labels
        self.language = language
        self.customer_count = customer_count
        self.estimated_customer_points = estimated_customer_points
        self.estimated_points = estimated_points
        self.impact = impact
        self.confidence = confidence
        self.reach = reach
        self.effort = effort
        self.days_to_due = self.calculateDaysToDue(due_date)
        self.date_multiplier = date_multiplier
        self.rice_total = rice_total
        self.num_of_comments = num_of_comments
        self.num_of_reactions = num_of_reactions

    # Get the number of days to due date
    def calculateDaysToDue(self, due_date):
        ''' The Due date should be in the format MM/DD/YYYY '''
        if due_date and isinstance(due_date, datetime):
            return (due_date - datetime.today()).days
        return None

    def to_json(self):
        return {
            'id': self.id,
            'category': self.category,
            'confidence': self.confidence,
            'creator': self.creator,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'updated_locally_at': self.updated_locally_at,
            'customer_count': self.customer_count,
            'date_multiplier': self.date_multiplier,
            'days_to_due': self.calculateDaysToDue(self.due_date),
            'due_date': self.due_date,
            'effort': self.effort,
            'estimated_customer_points': self.estimated_customer_points,
            'estimated_points': self.estimated_points,
            'impact': self.impact,
            'labels': self.labels,
            'language': self.language,
            'maintainer': self.maintainer,
            'num_of_comments': self.num_of_comments,
            'num_of_reactions': self.num_of_reactions,
            'reach': self.reach,
            'rice_total': self.rice_total,
            'task_type': self.task_type,
            'title': self.title,
            'url': self.url
        }
