# project/api/models.py


import datetime

from project import db


class Item_Status(db.Model):
    __tablename__ = "item_status"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=1)
    value_type = db.Column(db.String(50), nullable=False, default="multiplier")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now)

    def __init__(self, name, value, value_type):
            self.name = name
            self.value = value
            self.value_type = value_type
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, 
                       db.ForeignKey('item_status.id'),
                       nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.now)
    due_date = db.Column(db.DateTime, nullable=True)
    requestor = db.Column(db.String(), nullable=False)
    maintainer = db.Column(db.String(), nullable=True)

    def __init__(self, subject, url, requestor, due_date=None):
        self.subject = subject
        self.url = url
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        self.requestor = requestor
        self.due_date = due_date
        self.status = 1
    
    # Determine if two Items are equal
    @staticmethod
    def items_equal(item_1, item_2):
        if item_1.subject != item_2.subject:
            return False
        if item_1.status != item_2.status:
            return False
        if item_1.url != item_2.url:
            return False
        if item_1.requestor != item_2.requestor:
            return False
        if item_1.maintainer != item_2.maintainer:
            return False
        if item_1.due_date != item_2.due_date:
            return False
        return True
