from project.api.looker_api_handler import get_look
from project.api.json_cleaner import JsonCleaner
from project.api.db_cache import DBCache, Look
from flask_sqlalchemy import SQLAlchemy


def build_service(look_id, db, handler, db_model, json_cleaner):
    look = Look(look_id, handler)
    db_cache = DBCache(db_model)
    return DXLookerService(db_cache, db, look, json_cleaner)


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

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __hash__(self):
        return hash(self.look.look_id)

    def __repr__(self):
        str_list = []
        for attr, value in self.to_json().items():
            str_list.append("{}={}".format(attr, value))
        return "{}({})".format(self.__class__.__name__, ",".join(str_list))

