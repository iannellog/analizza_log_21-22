#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:09:57 2021

@author: giuliano
"""

import datetime
import sys
import pandas as pd 

 


# apro file iniziale lo rinomino e lo ordino per utente
 
imported_df = pd.read_json('/Users/giuliano/Desktop/Spezzone_prova.json', 'values')
imported_df.columns = ['DATA', 'UTENTE', 'CORSO', 'MAIN_EVENT','CORE_EVENT','DESCRIZIONE','ORIGINE','INDIRIZZO']
imported_df= imported_df.sort_values(by=['UTENTE'])




# definisco intervallo tra il primo e ultimo utente
users=range(1,imported_df['UTENTE'].max() +1)
# Prima implementazione del dataframe contenente le features volute, partendo dal conteggio dei singoli eventi per ciascun utente 
features_df = pd.DataFrame([],columns= list(imported_df['MAIN_EVENT'].unique()), index=users)
events_list= list(imported_df['MAIN_EVENT'].unique()) #lista di tutti gli eventi
users_events_df= imported_df[['UTENTE', 'MAIN_EVENT']]
for event in range(len(events_list)):
    for i in users:
           df_temp= users_events_df[users_events_df['MAIN_EVENT']== events_list[event]]
           df_temp= df_temp[df_temp['UTENTE']==i]
           event_frequency= df_temp['MAIN_EVENT'].count()
           features_df[events_list[event]][i]= event_frequency  

#una volta popolato il Dataframe con il conteggio voluto, aggiungo le rispettive feature
# calcolo della somma degli eventi totali per ciascun utente e aggiunta nel DF
sum_events= imported_df[['UTENTE', 'MAIN_EVENT']].groupby('UTENTE')['MAIN_EVENT'].count().tolist()          
features_df['Total_Event']= sum_events
# rilevazione della prima e ultima data per ciascun utente e aggiunta nel DF
prima_data=imported_df[['UTENTE', 'DATA']].groupby('UTENTE')['DATA'].min().tolist() #dataprimoevento x ogni utente
ultima_data= imported_df[['UTENTE', 'DATA']].groupby('UTENTE')['DATA'].max().tolist() #dataultimo x ogni utente  
features_df['First_Data']= prima_data
features_df['Last_Data']= ultima_data

