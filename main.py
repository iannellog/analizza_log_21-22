"""
Created on Wed Nov 10 12:52:57 2021

@author: Massimo Capurro Lladò

Scrivere un programma Python che legge una lista di log anonimizzati da un file. 

Ciascun elemento della lista di log è costituito dalle seguenti otto informazioni:

- Data/Ora
- Identificativo unico dell’utente
- Contesto dell’evento
- Componente
- Evento
- Descrizione
- Origine 
- Indirizzo IP

L'obiettivo è quello di calcolare per ogni utente un vettore di feature e salvare i dati sia in un foglio excel, sia in formato json

Possibili feature per ogni utente

- numero totale di eventi
- quante volte si è verificato ciascun evento 
- data primo evento
- data ultimo evento
- numero di giorni tra il primo e l'ultimo evento
- media e varianza del numero eventi in una settimana (da lunedi' a domenica)
- altre features a piacere
"""
#TODO: EVERITHING

import sys
import pandas as pd

DATE= 0
USER_CODE= 1
EVENT= 4



#This function reads the json file and saves its data into a list of lists

def ReadJsonFile(file):
    try:
        log_list = pd.read_json(file)
        return log_list
    except:
        print('Could not load the file! \nThe specified file path-name does not exist!')
        sys.exit()
    

#This function saves data onto a new json file

def SaveJsonFile(file, data):
    try: 
        data.to_json(file)
    except:
        print('Something went wrong during the creation of the new file!')
        sys.exit()
  
        




jsonfile = 'indata\logs_analizza1.json' 
log_list=ReadJsonFile(jsonfile)
#
SaveJsonFile(r'indata/newfile', log_list)       
print("Task ended")