from wsgiref.simple_server import make_server
from pyramid.config import Configurator


def accept_data(request):
    print("GOT", request.json)
    return {"status": "OK"}


if __name__ == '__main__':
    config = Configurator()
    config.add_route('accept_data', '/data')
    config.add_view(accept_data, route_name='accept_data', renderer='json')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
