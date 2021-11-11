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
   # exit()


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
    return tab_tot_occurences

def event_occurences(log_list, tab_tot_occurences):
    '''
    calculates the occurences per events
    :param log_list: a list of logs
    :param tab_tot_occurences: dictionary of dictionary with user codes
             and total occurences per user
    :return: the list of log and the same dictionary
             with occurrences for each event
    '''
    
    for log in log_list:
        if not log[4] in tab_tot_occurences[log[1]]:
            tab_tot_occurences[log[1]][log[4]]=1
        else:
            tab_tot_occurences[log[1]][log[4]]+=1
    return tab_tot_occurences

filein = input('insert path of the json file to analyze:')
log_list = read_json_file(filein)
tab_tot_occurences = tot_occurrences(log_list)
tab_tot_occurences = event_occurences(log_list, tab_tot_occurences)
write_json_file(tab_tot_occurences,'newfile.json', indnt=3)
# the results will be saved in a file named newfile.json

print('Fine')
    