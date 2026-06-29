import json
import base64


def create(response, username):
    session = base64.b64encode(json.dumps({'username': username}).encode()).decode('utf-8')
    response.set_cookie('vulpy_session', session)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get('vulpy_session')

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(decoded)
    except Exception:
        pass

    return session


def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response

