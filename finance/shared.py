import re
from enum import Enum
from datetime import date, timedelta


def date_to_mysql_str(date: date) -> str:
  return date.strftime("%Y-%m-%d")

  
def date_diff_months(d1: date, d2: date) -> int:
  return abs((d1.year - d2.year) * 12 + d1.month - d2.month)


def date_diff_days(d1: date, d2: date) -> int:
  delta = d1 - d2
  return abs(delta.days)


def date_diff_weeks(d1: date, d2: date) -> int:
  return int(date_diff_days(d1, d2) / 7)


def date_diff_years(d1: date, d2: date) -> int:
  return abs(d1.year - d2.year)


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
    weeks =  int(timespan_list[1])
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
