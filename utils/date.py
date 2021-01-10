from datetime import *


def date_to_string(date, pattern):
    return date.strftime(pattern)


def string_to_date(date, pattern):
    return datetime.strptime(date, pattern)


def get_year_and_quarter(date):
    year = date.year
    month = date.month
    quarter = 1

    if 1 <= month <= 3:
        quarter = 1
    elif 4 <= month <= 6:
        quarter = 2
    elif 7 <= month <= 9:
        quarter = 3
    elif 10 <= month <= 12:
        quarter = 4

    return year, quarter
