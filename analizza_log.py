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

from utils import FeatureWriter, JSONReader
from statistics import abstract_statistics

import sys


if __name__ == "__main__":

    # get input file name
    if len(sys.argv) > 1:
        filein = sys.argv[1]
    else:
        filein = 'indata/test_simple.json'

    if len(sys.argv) > 2:
        suffix = sys.argv[2]
    else:
        suffix = 'xlsx'

    # build output file name from input file name
    pos = filein.rfind('/')
    filename = filein[pos:]
    pos = filename.rfind('.')
    filename = filename[:pos]

    # read input file in a list of logs
    reader = JSONReader()
    log_list = reader.read_file(filein)

    # compute statistics and add them to a table which keys are user IDs
    my_statistics = abstract_statistics.create_instance("normalized")
    statistics_tab = my_statistics.compute_all(log_list)

    # save the table
    writer = FeatureWriter.create_instance(suffix)
    writer.write_file(statistics_tab, 'outdata' + filename + '.' + suffix)

    print('Fine')
