import datetime
import pandas as pd


def get_datetime_from_string(datetime_string):
    # format dd/MM/YYYY HH:mm
    try:
        # separating date from time
        date_and_time = datetime_string.split(' ', 1)

        # split date following format dd/MM/YYYY
        date_parts = [int(x) for x in date_and_time[0].split('/', 2)]
        # split time following format HH:mm
        time_parts = [int(x) for x in date_and_time[1].split(':', 1)]

        return datetime.datetime(
            date_parts[2],
            date_parts[1],
            date_parts[0],
            time_parts[0],
            time_parts[1]
        )

        # TODO - not in the correct
    except Exception as e:
        print('Not correct datetime')


def format_date_as_input(date):
    return f'{date.day}/{date.month}/{date.year} {str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}'


def get_extremes_datetime(list_dates):
    # transform string into datetime and using Series min and max
    timestamps_list = pd.Series([get_datetime_from_string(date_string) for date_string in list_dates])
    return timestamps_list.min(), timestamps_list.max()


def get_days_between_two_dates(date_start, date_end):
    return abs(date_end - date_start).days


def get_num_logs_for_week(dates_users):
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
    return date - datetime.timedelta(days=date.weekday()) - datetime.timedelta(hours=date.hour,
                                                                               minutes=date.minute)


def add_zeros_to_array_if_needed(difference, array):
    for i in range(difference.days // 7):
        array.append(0)
