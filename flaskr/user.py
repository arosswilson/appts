from dataclasses import dataclass
from dataclasses import asdict
from .utils import generate_uuid
from .utils import parse_datetime
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from markupsafe import escape

from dataclasses import dataclass
from datetime import datetime
from .exceptions import ValidationError
from collections import defaultdict
DATABASE = {"users": {}, "appointments": defaultdict(list)}

@dataclass
class Appointment:
    user_id: str
    appt_datetime: datetime
    length: int

    def __init__(self, user_id: str, appt_datetime: str):
        self._user_validation(user_id)
        appt_datetime = parse_datetime(appt_datetime)
        self._appt_datetime_validation(appt_datetime)
        self._validate(user_id, appt_datetime)
        self.user_id = user_id
        self.appt_datetime = appt_datetime
        self.length = 30
        self.save()

    def save(self):
        DATABASE["appointments"][self.user_id].append(self)
        
    def _user_validation(self, user_id: str):
        user = DATABASE["users"].get(user_id)
        if not user:
            raise ValidationError("user does not exist")
    
    def _appt_datetime_validation(self, appt_datetime: datetime):
        minutes = appt_datetime.minute
        if minutes % 30 != 0:
            raise ValidationError("appt times must start on the hour or half hour")
    
    def _validate(self, user_id: str, appt_datetime: datetime):
        user_appts = DATABASE["appointments"].get(user_id, [])
        same_day_appts = [appt for appt in user_appts if appt.appt_datetime.date() == appt_datetime.date()]
        if len(same_day_appts) > 0:
            raise ValidationError("User can't have multiple appts on same day")
    

@dataclass
class User:
    id: str

    def __init__(self):
        self.id = generate_uuid()
        self.save()

    def appointments(self):
        return DATABASE["appointments"].get(self.id, [])

    def save(self):
        DATABASE["users"][self.id] = self
    


bp = Blueprint("user", __name__)



@bp.route('/users/', methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        user = User()
        return make_response(asdict(user), 201)
    elif request.method == "GET":
        return make_response(jsonify([asdict(user) for _, user in DATABASE["users"].items()]), 200)
    else:
        return make_response("endpoint only allows GET and POST requests", 405)


@bp.route('/users/<uuid:user_id>/appointments', methods=('GET', 'POST'))
def appointments(user_id):
    user_id = str(escape(user_id))
    if request.method == "POST":
        data = request.get_json()
        try:
            appt_date_str = data.get("appt_datetime", "")
            appt = Appointment(user_id, appt_date_str)
        except ValidationError as v:
            return make_response(str(v), 400)
        return make_response(asdict(appt), 201)

    elif request.method == "GET":
        user = DATABASE["users"].get(user_id)
        return make_response(jsonify([asdict(appt) for appt in user.appointments()]), 200)
    else:
        return make_response("endpoint only allows GET and POST requests", 405)



