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

from utils import read_json_file, write_json_file
from statistics import compute_statistics
import sys


if __name__ == "__main__":

    # get input file name
    if len(sys.argv) > 1:
        filein = sys.argv[1]
    else:
        # filein = input('insert path of the json file to analyze:')
        filein = 'indata/test_simple.json'

    # build output file name from input file name
    pos = filein.rfind('/')
    filename = filein[pos:]

    # read input file in a list of logs
    log_list = read_json_file(filein)

    # compute statistics and add them to a table which keys are user IDs
    statistics_tab = compute_statistics(log_list)

    # save the table
    write_json_file(statistics_tab, 'outdata' + filename, indnt=3)

    print('Fine')
