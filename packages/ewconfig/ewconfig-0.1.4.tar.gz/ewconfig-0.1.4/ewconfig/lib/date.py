import datetime as dt

ALL_DATE_FORMATS = ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f',
                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M',
                    '%Y-%m-%d')


def parse_date(value):
    for format in ALL_DATE_FORMATS:
        try:
            return dt.datetime.strptime(value, format).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    raise ValueError('Cannot parse "%s" as a datetime' % value)


def between(start, date, finish):
    date = date if date else dt.datetime.now()
    return (start is None or start <= date) and (finish is None or date <= finish)

