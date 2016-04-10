
from datetime import datetime
from marshmallow import fields, Schema, pre_load


class SensorSchema(Schema):
    name = fields.String()
    type_name = fields.String()
    description = fields.String()
    types = fields.List(fields.String)


class MeasurementSchema(Schema):
    created_at = fields.DateTime(default=datetime.utcnow)
    name = fields.String(required=True)
    value = fields.Float(required=True)


class MeasurementRequestSchema(Schema):
    name = fields.String(required=True)
    sensor = fields.String(required=True)
    value = fields.Float(required=True)


class SensorRequestSchema(Schema):
    location = fields.String()
    hive = fields.String()
    measurements = fields.Nested(MeasurementRequestSchema, many=True)

    @pre_load
    def format_measurements_request(self, data):
        """
        Format data['measurements'] for MeasurementRequestSchema.
        """
        measurements = []
        for sensor_name, sensor_data in data['measurements'].items():
            for name, value in sensor_data.items():
                measurement = {
                    'sensor': sensor_name,
                    'name': name,
                    'value': value,
                }
                measurements.append(measurement)

        data['measurements'] = measurements
