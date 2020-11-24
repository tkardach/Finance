import re
import json
from typing import Union
from datetime import date, timedelta
from flask import Response
from werkzeug.exceptions import (HTTPException, NotFound, InternalServerError, Forbidden,
    Unauthorized, BadRequest)


class Validation():
    EMAIL_REG = r'[^@]+@[^@]+\.[^@]+'


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
    def raise_missing_parameter(parameter: str):
        raise BadRequest(description="'%s' missing from the body of the request." % parameter)


    @staticmethod
    def raise_invalid_credentials():
        raise Unauthorized(description="Invalid email or password.")

    
    @staticmethod
    def raise_user_already_exists():
        raise BadRequest(description="A user with the given email already exists.")

    
    @staticmethod
    def raise_invalid_email(email: str):
        raise BadRequest(description="Email parameter '%s' is in an invalid email address format." % email)

    
    @staticmethod
    def raise_invalid_parameter(parameter: str, message: str="Parameter is invalid"):
        raise BadRequest(description="%s : %s" % (parameter, message))

    @staticmethod
    def raise_unauthorized_user():
        raise Unauthorized()
    
    @staticmethod
    def raise_internal_server_error(description=None):
        if description is None:
            raise InternalServerError()
        else:
            raise InternalServerError(description=description)
    

    @staticmethod
    def raise_not_found(item: str):
        raise NotFound("'%s' could not be found." % item)


class HTTPResponse():
    __json_mime_type = 'application/json'

    @staticmethod
    def return_json_response(json_obj: Union[dict, list], status: int):
        return Response(json.dumps(json_obj), status=status, mimetype=HTTPResponse.__json_mime_type)
