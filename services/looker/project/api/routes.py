from flask import Blueprint, jsonify, request

from project.api.looker_api_handler import build_handler
from project import config, db
from project.api.json_cleaner import JsonCleaner, read_json
from project.api.dx_looker_service import build_service
from project.api.models import SendsByLibrary, InvoicingByLibrary

dx_looker_blueprint = Blueprint('dx_looker', __name__)

ESM = 'email_send_month'

handler = build_handler()
conf = config.DevelopmentConfig
json_cleaner = JsonCleaner(read_json(conf.TRANSFORMATIONS))
services = {
    '4404': build_service('4404', db, handler, SendsByLibrary, json_cleaner),
    '4405': build_service('4405', db, handler, InvoicingByLibrary, json_cleaner),
}


@dx_looker_blueprint.route('/looker/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@dx_looker_blueprint.route('/looker/<look_id>', methods=['GET'])
def get_look_id(look_id):
    """Get look_id data"""
    # db_cache = look_ids[look_id]
    # data = db_cache.cache
    # if not db_cache.cache:
    #     db_cache.db.create_all()
    #     db_cache.db.session.commit()
    #     data = db_cache.refresh_cache()
    # data = services[look_id].db.query.all()
    rows = services[look_id].db_cache.db_model.query.all()
    data = [r.to_json() for r in rows]
    response_object = {
        'status': 'success',
        'data': data
    }
    return jsonify(response_object), 200
