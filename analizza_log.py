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

from utils import JSONReader, JSONWriter
from statistics import statistics

import sys
import pandas as pd


def dict2df(tab):
    keys = list(tab.keys())
    events = [eventID for eventID in tab[keys[0]].keys()]
    df = pd.DataFrame(index=keys, columns=events)
    for k in keys:
        for e in events:
            df.at[k, e] = tab[k][e]
    return df


if __name__ == "__main__":

    # get input file name
    if len(sys.argv) > 1:
        filein = sys.argv[1]
    else:
        filein = 'indata/test_simple.json'

    # build output file name from input file name
    pos = filein.rfind('/')
    filename = filein[pos:]

    # read input file in a list of logs
    reader = JSONReader()
    log_list = reader.read_file(filein)

    # compute statistics and add them to a table which keys are user IDs
    my_statistics = statistics()
    statistics_tab = my_statistics.compute_all(log_list)

    # save the table
    writer = JSONWriter()
    writer.write_file(statistics_tab, 'outdata' + filename, indnt=3)

    df = dict2df(statistics_tab)
    df.to_excel('outdata/ptova.xlsx')

    print('Fine')
