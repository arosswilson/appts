import uuid
from .exceptions import ValidationError
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def parse_datetime(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValidationError("invalid datetime format. please submit isoformat without seconds, microseconds, or timezone: '%Y-%m-%dT%H:%M'")