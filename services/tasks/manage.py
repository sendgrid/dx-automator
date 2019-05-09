#!/usr/bin/env python3
import unittest
import coverage
from datetime import datetime

from flask_script import Manager
from flask_migrate import MigrateCommand

from project import create_app, db
from project.api.models import Task

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
        'project/__init__.py'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
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
    db.session.add(Task(
        created_at=datetime.utcnow(),
        creator="af4ro",
        url="https://github.com/sendgrid",
        title="First test issue"
    ))
    db.session.add(Task(
        created_at=datetime.utcnow(),
        creator="anshul",
        url="anshulsinghal.me",
        title="Second test issue",
        due_date=datetime(2018, 3, 20)
    ))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
