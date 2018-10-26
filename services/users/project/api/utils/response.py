def response_json_ok(json):
    """Creates a tuple representing the HTTP package to
    respond the requisition with the given JSON on its body
    and status code 200
    :param json: object to be sent on HTTP body
    :return response: tuple representing the HTTP response package
    """

    return _make_json_response(json, 200)

def response_json_created(json):
    """Creates a tuple representing the HTTP package to
    respond the requisition with the given JSON on its body
    and status code 201
    :param json: object to be sent on HTTP body
    :return response: tuple representing the HTTP response package
    """

    return _make_json_response(json, 201)


def response_json_bad_request(json):
    """Creates a tuple representing the HTTP package to
    respond the requisition with the given JSON on its body
    and status code 400
    :param json: object to be sent on HTTP body
    :return response: tuple representing the HTTP response package
    """

    return _make_json_response(json, 400)


def response_json_unauthorized(json):
    """Creates a tuple representing the HTTP package to
    respond the requisition with the given JSON on its body
    and status code 401
    :param json: object to be sent on HTTP body
    :return response: tuple representing the HTTP response package
    """

    return _make_json_response(json, 401)


def _make_json_response(json, status):
    """Creates a tuple representing the HTTP package to
    respond the requisition with the given JSON on its body
    and the given status code.
    :param json: object to be sent on HTTP body
    :param status: status code
    :return response: tuple representing the HTTP response package
    """

  return json, status, {'Content-Type': 'application/json'}
