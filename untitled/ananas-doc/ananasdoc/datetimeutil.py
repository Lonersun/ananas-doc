#-*- coding:utf-8 -*-
import calendar
from functools import partial
import time
from datetime import datetime, date, timedelta

import pytz

utc = pytz.utc

PRC_TZ_STR = 'Asia/Shanghai'
prc = pytz.timezone(PRC_TZ_STR)


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None


def is_naive(value):
    """
    Determines if a given datetime.datetime is naive.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is None or value.tzinfo.utcoffset(value) is None


def make_aware(value, timezone):
    """
    Makes a naive datetime.datetime in a given time zone aware.
    """
    if hasattr(timezone, 'localize'):
        # available for pytz time zones
        return timezone.localize(value, is_dst=None)
    else:
        # may be wrong around DST changes
        return value.replace(tzinfo=timezone)


def make_naive(value, timezone):
    """
    Makes an aware datetime.datetime naive in a given time zone.
    """
    value = value.astimezone(timezone)
    if hasattr(timezone, 'normalize'):
        # available for pytz time zones
        value = timezone.normalize(value)
    return value.replace(tzinfo=None)


def make_prc_datetime(*args, **kwargs):
    d = datetime(*args, **kwargs)
    return make_aware(d, prc)


def now(timezone=utc):
    """
    Returns an aware datetime.datetime
    """
    return make_aware(datetime.utcnow(), timezone)


utcnow = datetime.utcnow


def utc2prc(value):
    """
    Convert utc to PRC local datetime
    """
    if is_naive(value):
        value = make_aware(value, utc)
    return value.astimezone(prc)


def format_prc(value, fmt=None):
    if isinstance(value, datetime):
        if fmt is None:
            fmt = '%Y-%m-%d %H:%M:%S'
        return utc2prc(value).astimezone(prc).strftime(fmt)
    return value


def format_utc(value, fmt=None):
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S UTC'
    return value.strftime(fmt)


def prc_now(fmt='%Y-%m-%d %H:%M:%S'):
    return utc2prc(datetime.utcnow()).strftime(fmt)


def parse_utc_from_str(time_str, zone_name, fmt='%Y-%m-%d %H:%M:%S'):
    """
    Parse a datetime with given zone and convert to utc datetime
    :param time_str:
    :type time_str:
    :param zone_name:
    :type zone_name:
    :param fmt:
    :type fmt:
    :return:
    :rtype:
    """
    zone = pytz.timezone(zone_name)
    # assume naive
    t = datetime.strptime(time_str, fmt)
    # convert to aware
    t2 = make_aware(t, zone)
    return make_naive(t2, utc)


def parse_prc_from_day_str(day_str, fmt='%Y%m%d'):
    """
    解析日期形式的字符串（PRC本地时间）并转换到UTC navie datetime
    :param day_str:
    :param fmt: default is '%Y%m%d'
    :return: datetime UTC naive
    """
    return parse_utc_from_str(day_str, PRC_TZ_STR, fmt)


def datetime2timestamp(datetime_=None):
    """
    Convert local datetime to unix timestamp
    """
    if datetime_ is None:
        datetime_ = datetime.now()
    if not isinstance(datetime_, datetime):
        return 0
    return datetime_ and int(time.mktime(datetime_.timetuple()))


def utc2timestamp(utc_datetime=None):
    """
    Convert utc datetime to seconds since epoch (UTC)
    """
    if utc_datetime is None:
        return int(time.time())
    return calendar.timegm(utc_datetime.utctimetuple())


MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


def expired_ttl(days=0, hours=0, minutes=0, seconds=0, current=None):
    """
    Compute a expired timestamp
    """
    if not current:
        current = int(time.time())
    return current + days * DAY + hours*HOUR + minutes * MINUTE + seconds


def next_time(from_now=None, **kwargs):
    if from_now is None:
        from_now = datetime.utcnow()
    _next_time = from_now + timedelta(**kwargs)
    return _next_time


def after_days(days=1):
    return next_time(days=days).date()


def date2int(date_v):
    """
    >>> date2int(datetime.date(2013,11,1))
    20131101
    :param date_v:
    :type date_v:
    :return:
    :rtype:
    """
    return int(date_v.strftime('%Y%m%d'))


def make_date_timestamp(year, month, day):
    d = datetime(year, month, day, 23, 59, 59)
    return calendar.timegm(d.utctimetuple())


def make_date(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return

_all_chunks = (
    (60 * 60 * 24 * 365, u'年'),
    (60 * 60 * 24 * 30, u'月'),
    (60 * 60 * 24 * 7, u'周'),
    (60 * 60 * 24, u'天'),
    (60 * 60, u'小时'),
    (60, u'分钟')
)

_day_chunks = (
    (60 * 60 * 24, u'天'),
    (60 * 60, u'小时'),
    (60, u'分钟')
)


def compute_relative_time(timestamp=1340875790, ago=True, chunks=None):
    #git/data.c void show_date_relative
    delta = int(time.time()) - int(timestamp)
    # In unitests we have 0 or 1 seconds, not stable,
    # better say 'few' when below 10 s.
    if delta < 10:
        return u"刚刚"
    if delta < 90:
        return unicode(delta) + u" 秒前" if ago else unicode(delta)

    if chunks is None:
        chunks = _all_chunks

    for i, (seconds, name) in enumerate(chunks):
        count = delta // seconds
        if count != 0:
            break

    s = u'{0} {1}'.format(count, name)

    if i + 1 < len(chunks):
        seconds2, name2 = chunks[i + 1]
        count2 = (delta - (seconds * count)) // seconds2
        if count2 != 0:
            s += u' {0} {1}'.format(count2, name2)
    return s + u' 以前' if ago else s


compute_relative_days = partial(compute_relative_time, chunks=_day_chunks)


# def current_month_range_datetime():
#     """
#     返回当前月的start/end datetime(next month first time)
#     :return: list
#     """
#     _now = utcnow()
#     first_time = datetime(_now.year, _now.month, 1, 0, 0, 0, 0)
#     last_time = first_time + relativedelta.relativedelta(months=1)
#     return first_time, last_time
#
#
# def today_range_datetime():
#     _now = utcnow()
#     first_time = datetime(_now.year, _now.month, _now.day, 0, 0, 0, 0)
#     last_time = first_time + relativedelta.relativedelta(days=1)
#     return first_time, last_time


# def before_month_range_datetime(months=1):
#     """
#     返回前一个月的start/end datetime(current month first time)
#     :return: list
#     """
#     _now = utcnow()
#     last_time = datetime(_now.year, _now.month, 1, 0, 0, 0, 0)
#     first_time = last_time - relativedelta.relativedelta(months=months)
#     return first_time, last_time


# def this_month_range_datetime(month, year=None):
#     _now = utcnow()
#     if year is None:
#         year = _now.year
#     first_time = datetime(year, month, 1, 0, 0, 0, 0)
#     last_time = first_time + relativedelta.relativedelta(months=1)
#     return first_time, last_time


def remain_days(target_datetime, from_datetime=None):
    if from_datetime is None:
        from_datetime = utcnow()
    delta = target_datetime - from_datetime
    return delta.days


# def next_month(from_datetime, months=1):
#     return from_datetime + relativedelta.relativedelta(months=months)


def parse_date(date_str, fmt='%Y-%m-%d'):
    return datetime.strptime(date_str, fmt).date()

today = date.today


