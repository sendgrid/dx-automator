import unittest
import click
from datetime import datetime

from flask.cli import FlaskGroup
from project import create_app, ibl_cache
from project.api.looker_api_handler import get_look
from project.api.clean_looker_json import CleanLookerJson, read_json

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    ibl_cache.db.drop_all()
    ibl_cache.db.create_all()
    ibl_cache.db.session.commit()


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
    json_object = get_look(l)
    trans = read_json("project/db_creation/column_transformations.json")
    cleaner = CleanLookerJson(trans)
    for j in json_object:
        print(j)
        print(cleaner.clean_json(j))
    # for j in json_object:
    #     i = ibl_cache.db_model(**j)
    #     ibl_cache.db.session.add(i)
    # ibl_cache.db.session.commit()


if __name__ == "__main__":
    cli()
