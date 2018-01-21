"""Application Manager

This module administers this application.

Example:
    The following commands will create the DB, seed it with sample
    data and then run tests:

        $ python3 manage.py recreate_db
        $ python3 manage.py seed_db
        $ python3 manage.py test

Attributes:
    app (Flask Appliction Object):
        http://flask.pocoo.org/docs/0.12/api/

    manager (FlaskScript Manager Object): Module level variables may be documented in
        https://flask-script.readthedocs.io/en/latest/

Todo:
    * TBD

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import unittest

from flask_script import Manager
from project import create_app, db
from project.api.models import Item, ItemStatus

app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""

    db.session.add(
        ItemStatus(
            name="Intake",
            value="1000000000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Needs PR Deploy",
            value="60000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Needs PR Merge",
            value="55000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Waiting for CLA",
            value="50000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Waiting for feedback",
            value="50000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Waiting for changes",
            value="50000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Waiting for build to run",
            value="50000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Needs PR Review",
            value="49000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="In Progress",
            value="20000",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Completed",
            value="-1",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Deferred",
            value="-1",
            value_type="multiplier"
            ))

    db.session.add(
        ItemStatus(
            name="Solved",
            value="-1",
            value_type="multiplier"
            ))
    """Need to make sure the item status values are available"""
    db.session.commit()
    
    db.session.add(
        Item(
             subject="The firstest item",
             url='https://github.com/sendgriddx/issues/1',
             requestor='mbernier'))

    db.session.add(
        Item(subject="The secondest item",
             url='https://github.com/sendgriddx/issues/2',
             requestor='thinkingserious'))

    db.session.commit()

if __name__ == '__main__':
    manager.run()
