import unittest, os

from flask.cli import FlaskGroup
from project import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
# from project.api.models import DXLooker
# from project.api.looker_api_handler import LookerApiHandler
# from project.api.util import clean_invoice_json
#
# app = create_app()
# cli = FlaskGroup(create_app=create_app)
#
#
# @cli.command()
# def recreate_db():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()
#
#

#
#
# # @cli.command()
# # def seed_db():
# #     """Seeds the database"""
# #     db.session.add(Looker(username="james", email="james@sendgrid.com"))
# #     db.session.add(Looker(username="purpura", email="purpura@sendgrid.com"))
# #     db.session.commit()


if __name__ == '__main__':
    cli()
    # app = create_app()
    # app.config.from_object("project.config.BaseConfig")
    # email_send_month = app.config["EMAIL_SEND_MONTH"]
    # total_ei_revenue = app.config["TOTAL_EI_REVENUE"]
    # sg_client_id = os.environ.get("LOOKER_CLIENT_ID")
    # sg_client_secret = os.environ.get("LOOKER_CLIENT_SECRET")
    # sg_endpoint = os.environ.get("SENDGRID_LOOKER")
    # print(sg_endpoint)
    #
    # looker_api = LookerApiHandler(sg_client_id, sg_client_secret, sg_endpoint)
    # looker_api.login()
    # json_object = looker_api.run_look("4405").json()
    # print(json_object)
    # for j in json_object:
    #     print(clean_invoice_json(j, email_send_month, total_ei_revenue))
    # looker_api.logout()
