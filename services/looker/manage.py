import unittest
import click
from datetime import datetime

from flask.cli import FlaskGroup
from project import create_app, ibl_cache, db, config
from project.api.dx_looker_service import DXLookerService
from project.api.json_cleaner import JsonCleaner, read_json
from project.api.looker_api_handler import LookerApiHandler, get_looker_credentials
from project.api.db_cache import Look


app = create_app()
cli = FlaskGroup(create_app=create_app)

conf = config.DevelopmentConfig
c_id, c_secret, endpoint = get_looker_credentials()
handler = LookerApiHandler(endpoint)
look = Look(conf.LOOKS["INVOICING"], handler)
json_cleaner = JsonCleaner(read_json(conf.TRANSFORMATIONS))
ibl_service = DXLookerService(ibl_cache, db, look, json_cleaner)


@cli.command()
def recreate_db():
    ibl_service.db.drop_all()
    ibl_service.db.create_all()
    ibl_service.db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_db():
    """Seeds the database"""
    d = dict()
    d["email_send_month"] = datetime(2018, 8, 1).isoformat()
    dx = ibl_cache.db_model(**d)
    ibl_cache.db.session.add(dx)
    ibl_cache.db.session.commit()


@cli.command()
@click.option("-l")
def pull_look(l):
    if l not in conf.LOOKS.values():
        print("Invalid Look ID")
    else:
        ibl_service.cache_look()


if __name__ == "__main__":
    handler.login(c_id, c_secret)
    cli()
    handler.logout()
