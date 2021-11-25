"""
Created on Thu Nov 25 17:18:25 2021

by Giulio Iannello
"""

from datetime import datetime


def add_tot_occurrences(log_list):
    '''
     calculates the total occurrences per user from the list of logs
    :param log_list: a list of logs
    :return: a dictionary of dictionary with user codes
             and total occurrences per user
    '''
    tab_tot_occurrences = {}
    for log in log_list:
        if not log[1] in tab_tot_occurrences:
            tab_tot_occurrences[(log[1])] = {}
            tab_tot_occurrences[(log[1])]['tot_occurrences'] = 1
        else:
            tab_tot_occurrences[log[1]]['tot_occurrences'] += 1
    return dict(sorted(tab_tot_occurrences.items()))


def add_event_occurrences(log_list, tab_tot_occurrences):
    '''
    calculates the occurences per event
    :param log_list: a list of logs
    :param tab_tot_occurrences: dictionary of dictionary with user codes
             and total occurrences per user
    :return: the same dictionary with the occurrences for each event added
    '''
    for log in log_list:
        if log[4] not in tab_tot_occurrences[log[1]]:
            tab_tot_occurrences[log[1]][log[4]] = 1
        else:
            tab_tot_occurrences[log[1]][log[4]] += 1
    eventi = set()
    for user in tab_tot_occurrences:
        eventi = eventi.union(set(tab_tot_occurrences[user].keys()))
    eventi.remove('tot_occurrences')
    for user in tab_tot_occurrences:
        for e in eventi:
            if e not in tab_tot_occurrences[user]:
                tab_tot_occurrences[user][e] = 0
    return tab_tot_occurrences


def get_dates_of_occurrences(log_list, users):
    '''
    calculates all dates on which the user performs an event
    :param tab_tot_occurrences: dictionary of dictionary with user codes,
             total occurrences per user and occurences for each event
    :param log_list: list of all logs
    :return: the same dictionary with all dates on which the user performs an event
    It can be useful for the next calculation of first date, last date etc.
    '''
    dates = {}
    for user in users:
        dates[user] = []
        for log in log_list:
            data = log[0].split()
            if log[1] == user:
                dates[user] += [datetime.strptime(log[0], "%d/%m/%Y %H:%M")]
    return dates


def add_first_last_dates(tab_tot_occurrences, dates):
    """
    For each user in tab_tot_occurrences add the first and last dates
    of events, and
    :param tab_tot_occurrences: dictionary to be updated
    :param dates: for each user gives the list of dates of events
    :return: tab_tot_occurrences updated
    """
    for user in tab_tot_occurrences:
        first_date = dates[user][0]
        last_date = dates[user][0]
        for d in dates[user]:
            if d < first_date:
                first_date = d
            elif last_date < d:
                last_date = d
        tab_tot_occurrences[user]['first_date'] = first_date.strftime("%d/%m/%Y %H:%M")
        tab_tot_occurrences[user]['last_date'] = last_date.strftime("%d/%m/%Y %H:%M")
        tab_tot_occurrences[user]['days between first-last access'] = (last_date - first_date).days
    return tab_tot_occurrences


def compute_statistics(log_list):
    """
    compute statistics and returns a table with users as rows and features as columns
    :param log_list:
    :return:
    """
    feature_tab = add_tot_occurrences(log_list)
    dates = get_dates_of_occurrences(log_list, feature_tab.keys())
    feature_tab = add_first_last_dates(feature_tab, dates)
    feature_tab = add_event_occurrences(log_list, feature_tab)
    return feature_tab