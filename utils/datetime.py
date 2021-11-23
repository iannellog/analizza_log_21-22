import datetime
import pandas as pd
import utils.handle_exception as he


def get_datetime_from_string(datetime_string):
    """
    transform string date from logs into a datetime instance
    :param datetime_string: string following this format 'dd/MM/YYYY HH:mm'
    :return datetime.datetime
    """
    try:
        date_and_time = datetime_string.split(' ', 1)
        date_parts = [int(x) for x in date_and_time[0].split('/', 2)]
        time_parts = [int(x) for x in date_and_time[1].split(':', 1)]

        return datetime.datetime(
            date_parts[2],
            date_parts[1],
            date_parts[0],
            time_parts[0],
            time_parts[1]
        )
    except Exception as e:
        he.fatal_error(f'***** error in get datetime **** {e}')


def format_date_as_input(date):
    """
    transform date in string format given in input 'dd/MM/YYYY HH:mm'
    :param date: datetime.datetime to convert
    :return str
    """
    return f'{date.day}/{date.month}/{date.year} {str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}'


def get_extremes_datetime(list_dates):
    """
    calculate first and last date in a list
    :param list_dates: pandas.Series containing datetime string of logs
    :return datetime.datetime, datetime.datetime
    """
    timestamps_list = pd.Series([get_datetime_from_string(date_string) for date_string in list_dates])
    return timestamps_list.min(), timestamps_list.max()


def get_days_between_two_dates(date_start, date_end):
    """
    calculate different in days between two dates
    :param date_start: datetime.datetime
    :param date_end: datetime.datetime
    :return num
    """
    return abs(date_end - date_start).days


def get_num_logs_for_week(dates_users):
    """
    calculate a pandas.Series containing the number of logs for each week between first and last date
    :param dates_users: pandas.Series containing datetime string of logs
    :return pandas.Series
    """
    dates_datetime = [get_datetime_from_string(date) for date in dates_users]
    dates_datetime.sort()
    num_logs_for_week = []
    num_current_week = 0
    first_of_week = set_to_monday(dates_datetime[0])
    last_of_week = first_of_week + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)
    for date in dates_datetime:
        if first_of_week <= date <= last_of_week:
            num_current_week += 1
        else:
            num_logs_for_week.append(num_current_week)
            num_current_week = 1
            difference = date - last_of_week
            add_zeros_to_array_if_needed(difference, num_logs_for_week)
            first_of_week = set_to_monday(date)
            last_of_week = first_of_week + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)
    num_logs_for_week.append(num_current_week)

    return pd.Series(num_logs_for_week)


def set_to_monday(date):
    # return monday of the week of date passed
    return date - datetime.timedelta(days=date.weekday()) - datetime.timedelta(hours=date.hour,
                                                                               minutes=date.minute)


def add_zeros_to_array_if_needed(difference, array):
    # insert a 0 for each week in the difference duration
    for i in range(difference.days // 7):
        array.append(0)
