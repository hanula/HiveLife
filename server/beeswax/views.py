
import transaction
from datetime import datetime, timedelta
from pyramid.view import view_config
from .schemas import SensorSchema, SensorRequestSchema, MeasurementSchema
from .models import DBSession, Location, Hive, Sensor, Measurement


@view_config(route_name='api.sensors', renderer='json')
def get_sensors(request):
    schema = SensorSchema(many=True)
    query = Sensor.query.order_by(Sensor.name).all()
    return schema.dump(query).data


@view_config(route_name='api.measurements', request_method='GET',
             renderer='json')
def get_measurements(request):
    sensor = Sensor.get_by(name=request.matchdict['sensor_name'],
                           type_name=request.matchdict['type_name'])

    start_time = datetime.utcnow() - timedelta(days=1)
    query = (Measurement.query
             .filter_by(sensor=sensor)
             .filter(Measurement.created_at > start_time)
             .order_by(Measurement.created_at.desc())
             .all())

    return MeasurementSchema(many=True).dump(query[::-1]).data


@view_config(route_name='api.datasink', request_method='POST', renderer='json')
def accept_data(request):
    schema = SensorRequestSchema()
    result = schema.load(request.json)

    if result.errors:
        print(result.errors)
        request.response.status_code = 400
        return {"status": "error"}

    sensor_request = result.data
    location = Location.get_or_create(name=sensor_request['location'])
    hive = Hive.get_or_create(location=location,
                              name=sensor_request['hive'])

    for measurement_request in sensor_request['measurements']:
        sensor = Sensor.get_or_create(hive=hive,
                                      type_name=measurement_request['name'],
                                      name=measurement_request['sensor'])
        Measurement(sensor=sensor, value=measurement_request['value']).save()

    transaction.commit()
    return {"status": "ok"}


@view_config(route_name='dashboard.home', renderer='dashboard.jinja2')
def dashboard_home(request):
    return {}
