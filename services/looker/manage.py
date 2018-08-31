import unittest
import click
from datetime import datetime

from flask.cli import FlaskGroup
from project import create_app, dx_cache, db
from project.api.models import DXLooker
from project.api.looker_api_handler import get_look

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    dx_cache.db.drop_all()
    dx_cache.db.create_all()
    dx_cache.db.session.commit()


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
    dx = dx_cache.db_model(**d)
    dx_cache.db.session.add(dx)
    dx_cache.db.session.commit()


@cli.command()
@click.option("-l")
def pull_look(l):
    json_object = get_look(l)
    for j in json_object:
        i = dx_cache.db_model(**j)
        dx_cache.db.session.add(i)
    dx_cache.db.session.commit()


if __name__ == "__main__":
    cli()
