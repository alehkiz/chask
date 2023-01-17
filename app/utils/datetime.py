from dateutil.tz import tzutc
from babel.dates import format_timedelta, format_datetime, get_timezone, format_date
from datetime import date as d_date, datetime, tzinfo
from dateutil import tz


def format_elapsed_time(timestamp:datetime, locale='pt_BR'):
    """Return elapsed time between `timezone` and actually timestap

    Args:
        timestamp (datetime): timestap as datetime used for calculate

    Returns:
        str: A string formated as locale
    """
    if isinstance(timestamp, datetime):
        # if timestamp.tzinfo is None:
        timestamp = convert_datetime_to_local(timestamp).replace(microsecond=0)
        return format_timedelta(timestamp-convert_datetime_to_local(datetime.utcnow()).replace(microsecond=0), add_direction=True, locale=locale)

def format_datetime_local(timestamp, format='short', locale='pt_BR'):
    if not format in ['full', 'long', 'medium', 'short']:
        format = 'short'
    if isinstance(timestamp, datetime):
        return format_datetime(timestamp, locale=locale, format=format, tzinfo=get_timezone('America/Sao_Paulo'))

def format_date_local(date, format='short', locale='pt_BR'):
    if not format in ['full', 'long', 'medium', 'short']:
        format = 'short'
    if isinstance(date, d_date):
        return format_date(date, locale=locale, format=format)

def days_elapsed(timestamp : datetime):
    '''
    Retornar os dias decorridos entre o ´timestamp´ e o tempo atual
    '''
    if isinstance(timestamp, datetime):
        timestamp = timestamp.replace(microsecond=0, tzinfo=None)
        return (convert_datetime_to_local(datetime.utcnow()) - timestamp).days

def convert_datetime_to_local(timestamp):
    to_zone = tz.gettz('America/Sao_Paulo')
    from_zone = tz.gettz('UTC')
    # if timestamp.tzinfo is None:
    #     utctime = utc.localize(timestamp)
    #     return localtz.normalize(utctime.astimezone(localtz))
    # utctime = utc.localize(timestamp.replace(tzinfo=None))
    # timestamp_utc = timestamp.replace(tzinfo=from_zone)
    return timestamp.replace(tzinfo=from_zone).astimezone(to_zone)

def convert_datetime_utc(timestamp):
    to_zone = tz.gettz('UTC')
    # utc = pytz.timezone('UTC')
    # utctime = utc.localize(timestamp)
    return timestamp.astimezone(to_zone) 