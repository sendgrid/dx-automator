from project.api.looker_api_handler import get_look
from project.api.json_cleaner import read_json, JsonCleaner
from project.api.db_cache import DBCache, Look
from flask_sqlalchemy import SQLAlchemy


class DXLookerService(object):
    def __init__(self, db_cache: DBCache, db: SQLAlchemy,
                 look: Look, json_cleaner: JsonCleaner):
        self.db_cache = db_cache
        self.db = db
        self.look = look
        self.json_cleaner = json_cleaner

    def cache_look(self):
        json_object = get_look(self.look.look_id)
        for j in json_object:
            clean_j = self.json_cleaner.clean_json(j)
            i = self.db_cache.db_model(**clean_j)
            self.db.session.add(i)
        self.db.session.commit()
