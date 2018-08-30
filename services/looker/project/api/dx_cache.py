from project.api.models import DXLooker
from flask_sqlalchemy import SQLAlchemy


class Builder(object):

    def __init__(self, db: SQLAlchemy, dx_looker: DXLooker):
        self.db = db
        self.dx_looker = dx_looker

    def build_cache(self):
        d = dict()
        for r in self.db.query.all():
            key = r["email_send_month"]
            new_r = r.copy().pop(key)
            d[key] = new_r
        return d


class DXCache(object):
    def __init__(self, db):
        self.cache = dict()
        self.db = db
        self.builder = Builder(self.db)

    def get_month(self, email_send_month):
        return self.cache.get(email_send_month, None)
