import re
import json
from typing import Union
from datetime import date, timedelta
from flask import Response


class Validation():
    EMAIL_REG = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


    @staticmethod
    def validate_email(email: str):
        reg = re.compile(Validation.EMAIL_REG)
        if reg.fullmatch(email):
            return True
        return False


class Timespan():
    def __init__(self, days=0, weeks=0, months=0, years=0):
        if days < 0 or days > 31:
            raise ValueError('days must be > 0 and <= 31')
        if weeks < 0 or weeks > 52:
            raise ValueError('weeks must be > 0 and <= 52')
        if months < 0 or months > 12:
            raise ValueError('months must be > 0 and <= 12')
        if years < 0 or years > 1:
            raise ValueError('years must be > 0 and <= 1')

        self.__days = days
        self.__weeks = weeks
        self.__months = months
        self.__years = years

    TIMESPAN_REG = r"^(0[0-9]|[0-9]|[1-2][0-9]|3[0-1]):([0-9]|0[0-9]|[1-4][0-9]|5[0-2]):([0-9]|1[0-2]|0[0-9]):([0-1])$"

    @staticmethod
    def get_timespan_str(days: int, weeks: int, months: int, years: int) -> str:
        return "%d:%d:%d:%d" % (days, weeks, months, years)

    @staticmethod
    def get_timespan(timespan: str) -> 'Timespan':
        reg = re.compile(Timespan.TIMESPAN_REG)
        if reg.fullmatch(timespan) is None:
            return None

        timespan_list = timespan.split(':')

        days = int(timespan_list[0])
        weeks = int(timespan_list[1])
        months = int(timespan_list[2])
        years = int(timespan_list[3])
        return Timespan(days, weeks, months, years)

    def to_timespan_str(self) -> str:
        return Timespan.get_timespan_str(
            self.__days,
            self.__weeks,
            self.__months,
            self.__years)

    @property
    def days(self):
        return self.__days

    @days.setter
    def days(self, days):
        self.__days = days

    @property
    def weeks(self):
        return self.__weeks

    @weeks.setter
    def weeks(self, weeks):
        self.__weeks = weeks

    @property
    def months(self):
        return self.__months

    @months.setter
    def months(self, months):
        self.__months = months

    @property
    def years(self):
        return self.__years

    @years.setter
    def years(self, years):
        self.__years = years


class HTTPErrorResponse():
    __json_mime_type = 'application/json'

    @staticmethod
    def post_missing_parameters(parameter: str):
        ret = {
          'error': 'Request body missing parameter',
          'message': '%s parameter missing from request body' % parameter
        }
        return HTTPResponse.return_json_response(ret, 400)


    @staticmethod
    def post_invalid_credentials():
        ret = {
          'error': 'Invalid Credentials',
          'message': 'Invalid email or password'
        }
        return HTTPResponse.return_json_response(ret, 400)

    
    @staticmethod
    def post_expects_json():
        ret = {
          'error': 'POST request body invalid format',
          'message': "POST request body expected to be 'application/json'"
        }
        return HTTPResponse.return_json_response(ret, 400)

    
    @staticmethod
    def user_already_exists():
        ret = {
          'error': 'User already exists',
          'message': "A user with the given email already exists"
        }
        return HTTPResponse.return_json_response(ret, 400)

    
    @staticmethod
    def invalid_email(email: str):
        ret = {
          'error': 'Email parameter is invalid',
          'message': "Email parameter '%s' is not a valid email address" % email
        }
        return HTTPResponse.return_json_response(ret, 400)

    
    @staticmethod
    def unauthorized_user():
        ret = {
          'error': '401 Unauthorized',
          'message': "The server could not verify that you are authorized to access the URL requested. " +
              "You either supplied the wrong credentials (e.g. a bad password), or your browser " + 
              "doesn't understand how to supply the credentials required."
        }
        return HTTPResponse.return_json_response(ret, 401)
    

    @staticmethod
    def internal_server_error(message: str = 'An unknown internal server error ocurred'):
        ret = {
          'error': 'Internal Server Error',
          'message': '%s' % message
        }
        return HTTPResponse.return_json_response(ret, 500)



class HTTPResponse():
    __json_mime_type = 'application/json'

    @staticmethod
    def return_json_response(json_obj: Union[dict, list], status: int):
        return Response(json.dumps(json_obj), status=status, mimetype=HTTPResponse.__json_mime_type)
