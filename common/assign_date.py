from dateutil import parser as date_parser

DATE_FORMAT="%Y-%m-%d"

def str_format(date):
    return date.strftime(DATE_FORMAT)

def assign_date(date):
    try:
        return date_parser.parse(date)
    except TypeError:
        return date