from utils import datetime as dt, constants


def populate_data_frame_output(data_frame_output, data_in, extra=False):
    """
    insert in data_frame_output features for each user in data_in.
    Features: num of events, times for each type of event, firs date, last date
        and difference in days between them, mean and variance of num events in weeks
    :param data_frame_output: pandas.DataFrame that will be populated
    :param data_in: pandas.DataFrame read from json
    :param extra: bool that indicates if extra features should be added
    :return None
    """
    print('\n============= Extract features =============')
    print('Extracting values...')

    # extracting number of total events
    data_frame_output[constants.N_EVENTS] = \
        [data_in[data_in[constants.ID_USER] == user].shape[0] for user in data_frame_output.index]

    # extracting number of every type of event
    events = get_distinct_events(data_in)
    data_frame_output[constants.EVENTS] = \
        [get_events_rep(data_in[data_in[constants.ID_USER] == user], events) for user in data_frame_output.index]

    # extracting first date, last date and days between them
    # zip permits to wrap in tuple multiple values for list comprehension
    data_frame_output[constants.FIRST_DATETIME], data_frame_output[constants.LAST_DATETIME], \
        data_frame_output[constants.DAYS_BTW_FIRST_LAST] = \
        zip(*(get_first_last_date_and_diff_user(data_in[data_in[constants.ID_USER] == user][constants.DATETIME])
              for user in data_frame_output.index))

    data_frame_output[constants.MEAN_WEEKS], data_frame_output[constants.VARIANCE_WEEKS] = \
        zip(*(get_mean_var_weeks(data_in[data_in[constants.ID_USER] == user][constants.DATETIME])
              for user in data_frame_output.index))

    if extra:
        origins = get_distinct_origin(data_in)
        data_frame_output[constants.ORIGIN_USAGE] = \
            [get_origin_usage(data_in[data_in[constants.ID_USER] == user], origins) for user in data_frame_output.index]

    print('Extraction completed!')


def get_first_last_date_and_diff_user(dates_user):
    first, last = dt.get_extremes_datetime(dates_user)
    difference = dt.get_days_between_two_dates(first, last)
    return dt.format_date_as_input(first),\
        dt.format_date_as_input(last), \
        difference


def get_mean_var_weeks(dates_user):
    series_num_logs_for_week = dt.get_num_logs_for_week(dates_user)
    return series_num_logs_for_week.mean(), series_num_logs_for_week.var()


def get_users_list(logs_df):
    return logs_df[constants.ID_USER].unique()


def get_distinct_events(data_in):
    return data_in[constants.EVENT].unique()


def get_distinct_origin(data_in):
    return data_in[constants.ORIGIN].unique()


def get_events_rep(users_logs, events_list):
    return {event: users_logs[users_logs[constants.EVENT] == event].size for event in events_list}


def get_origin_usage(users_logs, origin_list):
    return {origin: users_logs[users_logs[constants.ORIGIN] == origin].size for origin in origin_list}
