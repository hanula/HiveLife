from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def setup_routes(config):
    config.add_route('api.sensors', '/api/sensors')

    config.add_route('api.datasink', '/api/datasink')
    config.add_route('api.measurements', '/api/sensors/:sensor_name/:type_name/measurements')
    config.add_route('dashboard.home', '/')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    setup_routes(config)
    config.scan()
    return config.make_wsgi_app()
