import json
import uuid
from flask import jsonify, abort, request, Blueprint

from users import user, community, local, snmp

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/request', methods=['GET'])
def get_records():
    """Return all user requests
    @return: 200: an array of all known USER_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    USER_REQUESTS = return_user_dictionary('user')
    return jsonify(USER_REQUESTS)


@REQUEST_API.route('/request_local_user', methods=['GET'])
def get_records_local():
    """Return all user requests
    @return: 200: an array of all known USER_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    USER_REQUESTS = return_user_dictionary('local')
    return jsonify(USER_REQUESTS)


@REQUEST_API.route('/request_snmp_user', methods=['GET'])
def get_records_snmp():
    """Return all user requests
    @return: 200: an array of all known USER_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    USER_REQUESTS = return_user_dictionary('snmp')
    return jsonify(USER_REQUESTS)


@REQUEST_API.route('/request_community_user', methods=['GET'])
def get_records_community():
    """Return all user requests
    @return: 200: an array of all known USER_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    USER_REQUESTS = return_user_dictionary('community')
    return jsonify(USER_REQUESTS)


@REQUEST_API.route('/request/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """Get user request details by it's id
    @param _id: the id
    @return: 200: a USER_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if user request not found
    """
    USER_REQUESTS = return_user_dictionary('user')

    if _id not in USER_REQUESTS:
        abort(404)
    return jsonify(USER_REQUESTS[_id])


@REQUEST_API.route('/request_local_user', methods=['POST'])
def create_local_user():
    """Create a user request record
    @param name: post : the username of the requested user
    @param password: post : the password of the user requested
    @param type:user type
    @:param enabled: True/False
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)

    if not data.get('password'):
        abort(400)


    new_uuid = str(uuid.uuid4())
    returned = local.Local(data['name'],
                           data['password'],
                           "local",
                           data['enabled']).add_user(new_uuid, 'local')

    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@REQUEST_API.route('/request_community_user', methods=['POST'])
def create_community_user():
    """Create a user request record
    @param name: post : the username of the requested user
    @param type:user type
    @:param enabled: True/False
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """

    # if not request.get_json():
    #    abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)

    new_uuid = str(uuid.uuid4())

    community.Community(data['name'],
                        "community",
                        data['enabled']).add_user(new_uuid, 'community')
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@REQUEST_API.route('/request_snmp_user', methods=['POST'])
def create_snmp_user():
    """Create a user request record
    @param name: post : the username of the requested user
    @param password_a: post : first password of the user requested
    @param password_b: post : second password of the user requested
    @param type:user type
    @:param enabled: True/False
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """

    # if not request.get_json():
    #    abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)

    if not data.get('password_a'):
        abort(400)

    if not data.get('password_b'):
        abort(400)

    new_uuid = str(uuid.uuid4())

    snmp.Snmp(data['name'],
              data['password_a'],
              data['password_b'],
              "snmp",
              data['enabled']).add_user(new_uuid, 'snmp')
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@REQUEST_API.route('/request/<string:_id>', methods=['PUT'])
def edit_record(_id):
    """Edit a user request record
    @param name: post : the name of the user
    @param type: post : the type of the user
    @return: 200: a user_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    USER_REQUESTS = return_user_dictionary('user')
    type = USER_REQUESTS[_id]['type']
    USER_REQUESTS_TYPE = return_user_dictionary(type)

    if _id not in USER_REQUESTS:
        abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)

    if not data.get('password'):
        abort(400)

    user.User(data['name'],
              data['password'],
              type,
              data['enabled']).add_user(_id, type)

    USER_REQUESTS = return_user_dictionary('user')
    return jsonify(USER_REQUESTS[_id]), 200


@REQUEST_API.route('/request/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """Delete a user request record
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if user request not found
    """
    USER_REQUESTS = return_user_dictionary('user')
    type = USER_REQUESTS[_id]['type']
    USER_REQUESTS_TYPE = return_user_dictionary(type)

    if _id not in USER_REQUESTS.keys():
        abort(404)

    del USER_REQUESTS[_id]
    del USER_REQUESTS_TYPE[_id]

    return '', 204


@REQUEST_API.route('/request_convert_community_user/<string:id>/<string:type>', methods=['PUT'])
def convert_community_user(id, type):
    """Convert community user request record
    @param name: post : the name of the user
    @param type: post : the type of the user
    @return: 200: a user_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    USER_REQUESTS = return_user_dictionary('community')

    if type == 'local':
        local.Local(USER_REQUESTS[id]['name'], '', type, False).add_user(id, type)

    if type == 'snmp':
        snmp.Snmp(USER_REQUESTS[id]['name'], '', '', type, False).add_user(id, type)

    del USER_REQUESTS[id]
    save_user_request(USER_REQUESTS, 'community')
    return '', 200


@REQUEST_API.route('/request_convert_local_user/<string:id>', methods=['PUT'])
def convert_local_user(id):
    """Convert local user request to snmp
    @param id: post : the id of the user
    @return: 200
    @raise 400: misunderstood request
    """
    USER_REQUESTS = return_user_dictionary('local')
    print("requested convert")
    print(USER_REQUESTS)

    snmp.Snmp(USER_REQUESTS[id]['name'],
              USER_REQUESTS[id]['password'],
              USER_REQUESTS[id]['password'],
              'snmp', False).add_user(id, 'snmp')

    del USER_REQUESTS[id]
    save_user_request(USER_REQUESTS, 'local')
    return '', 200


def return_user_dictionary(type):
    with open('jsons/' + type + '.json', 'r') as f:
        user_request = json.load(f)
        return user_request


def save_user_request(user_request, type):
    with open('jsons/' + type + '.json', 'w') as f:
        json.dump(user_request, f)
