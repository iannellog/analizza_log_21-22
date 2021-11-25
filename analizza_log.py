# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 23:41:04 2021

@author: carpy, Maria elena Contini

Program to read a list of anonymized logs from a file 
and calculate a feature vector for each user by saving the data in json format
Expected json data: a list of log with the following fields:
- Data/Ora
- Identificativo unico dell’utente
- Contesto dell’evento
- Componente
- Evento
- Descrizione
- Origine 
- Indirizzo IP
"""

import json
from datetime import datetime


def fatal_error(message):
    """
    manage a fatal error: print a message and exit program
    :param message: message to be printed
    :return: None
    """
    print(message)
    exit()


def read_json_file(file_name):
    """
    read a json file and returns data
    manage exceptions
    :param file_name: file to be read
    :return: data structure corresponding to file content
    """
    try:
        fin = open(file_name)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except OSError as message:
        fatal_error(message)
    except json.JSONDecodeError as message:
        fatal_error(f'*** json error *** {message}')


def write_json_file(data, file_name, indnt=3):
    """
    write data to a json file
    manage exceptions
    :param data: python object to be written to file
    :param file_name: file to be written
    :param indent:
    :return: None
    """
    try:
        fout = open(file_name, 'w')
        json.dump(data, fout, indent=indnt)
        fout.close()
    except OSError as message:
        fatal_error(message)
        

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
            tab_tot_occurrences[(log[1])]= {}
            tab_tot_occurrences[(log[1])]['tot_occurrences'] = 1
        else:
            tab_tot_occurrences[log[1]]['tot_occurrences'] += 1
    return dict(sorted(tab_tot_occurrences.items()))


def add_event_occurrences(log_list, tab_tot_occurrences):
    '''
    calculates the occurences per events
    :param log_list: a list of logs
    :param tab_tot_occurrences: dictionary of dictionary with user codes
             and total occurrences per user
    :return: the same dictionary adding the
             occurrences for each event
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


def get_dates_of_occurrences(tab_tot_occurrences):
    '''
    calculates all dates on which the user performs an event
    :param tab_tot_occurrences: dictionary of dictionary with user codes,
             total occurrences per user and occurences for each event
    :return: the same dictionary with all dates on which the user performs an event
    '''
    dates = {}
    for user in tab_tot_occurrences:
        dates[user] = []
        for log in log_list:
            data = log[0].split()
            if log[1] == user:
                dates[user] += [datetime.strptime(log[0], "%d/%m/%Y %H:%M")]
    return dates
# It can be useful for the next calculation of first date, last date etc.


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
                        

filein = input('insert path of the json file to analyze:')
pos = filein.rfind('/')
nomefile = filein[pos:]
log_list = read_json_file(filein)
tab_tot_occurrences = add_tot_occurrences(log_list)
dates = get_dates_of_occurrences(tab_tot_occurrences)
tab_tot_occurrences = add_first_last_dates(tab_tot_occurrences, dates)
tab_tot_occurrences = add_event_occurrences(log_list, tab_tot_occurrences)
write_json_file(tab_tot_occurrences, 'outdata' + nomefile, indnt=3)

print('Fine')
