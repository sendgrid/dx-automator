from flask_sqlalchemy import SQLAlchemy


class Builder(object):
    def __init__(self, db_model):
        self.db_model = db_model

    def build_cache(self):
        cache = []
        for r in self.db_model.query.all():
            cache.append(r.to_json())
        return cache


class DXCache(object):
    def __init__(self, db: SQLAlchemy, db_model):
        self.cache = []
        self.db = db
        self.db_model = db_model
        self.builder = Builder(self.db_model)

    def refresh_cache(self):
        self.cache = self.builder.build_cache()
