#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 14:34:17 2021
per utente 
- numero totale di eventi
- quante volte si è verificato ciascun evento 
- data primo evento
- data ultimo evento
- numero di giorni tra il primo e l'ultimo evento
- media e varianza del numero eventi in una settimana (da lunedi' a domenica)
- altre features a piacere
-prova
@author: francyvadi
"""

# import json
# import sys
# from os.path import splitext
#importo la libreria pandas"

#!pip install pandas



import sys
import pandas as pd

def SaveJsonFile(file, data):
    try: 
        data.to_json(file, indent= 3, orient='table')
    except:
        print('Something went wrong during the creation of the new Json file!')
        sys.exit()

#creo un DataFrame con il file json"
df = pd.read_json('/Users/francyvadi/Desktop/analizza_log_21-22/indata/logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json')


#indicizzo i dati "
df.columns = ['DATA', 'MATRICOLA', 'CORSO', 'COMPONENTE','EVENTO','DESCRIZIONE','ORIGINE','INDIRIZZO']



#creo un nuvo dataframe prendendo le series MATRICOLA e EVENTO e separo gli eventi
df3=df.groupby('MATRICOLA').agg({ 'EVENTO': lambda x:  "|".join(x)})

#indicizzo la colonna
df3.columns = ['EVENTI COMPIUTI'] 

#divido gli eventi in più colonne usando il separatore |
df3=df3['EVENTI COMPIUTI'].str.split('|', expand=True)


#creo un nuovo dataframe 'eventi_utente' partendo da df3 per analizzarele features sugli eventi
#quante volte si è verificato ciascun evento  per ogni matricola 
eventi_utente=df3.apply(pd.Series.value_counts, axis=1).fillna(0)

#su questo nuovo database calcolo la somma di ogni evento per ogni matricola cioè sulle righe
eventi_utente.sum(axis=1)

#inserisco una nuova colonna nel quale è presente la somma del numero totale di eventi 
eventi_utente.insert(0, "somma_tot", eventi_utente.sum(axis=1), allow_duplicates=False)



# #nel database originario specifico la divisione della dta
# df['DATA']=pd.to_datetime(df['DATA'],format="%d/%m/%Y %H:%M")

# # creo un dict nel quale è presente massimo e minimo evento 
# massimo=max(df['DATA'])
# minimo=min(df['DATA'])

# data= {
#     'minima_data,': [massimo], 
#     'massima_data': [minimo]
    

# }
# date_max_min = pd.DataFrame(data, index=['1','50'])

# date_max_min

# #numero di giorni tra il primo e l'ultimo evanto 
# delta=massimo - minimo
# print(delta.days)

 

     
# #intoduco un dict con i giorni della settimana 
# dweek = {0:'Lunedi', 1:'Martedi', 2: 'Mercoledi', 3:'Giovedi', 4:'Venerdi', 5:'Sabato', 6:'Domenica'}


# #uso weekday() per associare ad ogni data il giorno della settimana corrispondente
# df['DATA'][0].weekday()
# dweek[df['DATA'][0].weekday()]

# #aggiungo una colonna che mi dice il giorno  di ogni data 
# df['Giorno'] = pd.Series(dweek[pd.datetime.weekday(df['DATA'][i])] for i in range(len(df)))



SaveJsonFile(r'indata/prova_eventi', eventi_utente)