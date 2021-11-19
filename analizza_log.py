# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 23:41:04 2021

@author: carpy
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
        

def tot_occurrences(log_list):
    '''
     calculates the total occurences per user from the list of logs
    :param log_list: a list of logs
    :return: a dictionary of dictionary with user codes
             and total occurences per user 
    '''
    tab_tot_occurences = {}
    for log in log_list:
        if not log[1] in tab_tot_occurences:
            tab_tot_occurences[(log[1])]= {}
            tab_tot_occurences[(log[1])]['tot_occurences']=1
        else:
            tab_tot_occurences[log[1]]['tot_occurences']+=1
    return dict(sorted(tab_tot_occurences.items()))


def event_occurences(log_list, tab_tot_occurences):
    '''
    calculates the occurences per events
    :param log_list: a list of logs
    :param tab_tot_occurences: dictionary of dictionary with user codes
             and total occurences per user
    :return: the same dictionary adding the
             occurrences for each event
    '''
    
    for log in log_list:
        if log[4] not in tab_tot_occurences[log[1]]:
            tab_tot_occurences[log[1]][log[4]]=1
        else:
            tab_tot_occurences[log[1]][log[4]]+=1
    eventi = set()
    for user in tab_tot_occurences:
        eventi = eventi.union(set(tab_tot_occurences[user].keys()))
    eventi.remove('tot_occurences')
    for user in tab_tot_occurences:
        for e in eventi:
            if e not in tab_tot_occurences[user]:
                tab_tot_occurences[user][e] = 0
    return tab_tot_occurences

def dates_of_occurences(tab_tot_occurences):
    '''
    calculates all dates on which the user performs an event
    :param tab_tot_occurences: dictionary of dictionary with user codes,
             total occurences per user and occurences for each event
    :return: the same dictionary with all dates on which the user performs an event
    '''
    dates = {}
    for user in tab_tot_occurences:
        dates[user] = []
        for log in log_list:
            data = log[0].split()
            if log[1] == user:
                dates[user] += [data[0]]
    return dates
#It can be useful for the next calculation of first date, last date etc.


def x(tab_tot_occurences, dates):
    for user in tab_tot_occurences:
        date_eventi = dates[user]
        tab_tot_occurences[user]['last_date'] = date_eventi[0]
        tab_tot_occurences[user]['first_date'] = date_eventi[-1]
    return tab_tot_occurences
                        

filein = input('insert path of the json file to analyze:')
pos = filein.rfind('/')
nomefile = filein[pos:]
log_list = read_json_file(filein)
tab_tot_occurences = tot_occurrences(log_list)
tab_tot_occurences = event_occurences(log_list, tab_tot_occurences)
dates = dates_of_occurences(tab_tot_occurences)
tab_tot_occurences = x(tab_tot_occurences, dates)
write_json_file(tab_tot_occurences, 'outdata' + nomefile, indnt=3)

print('Fine')
