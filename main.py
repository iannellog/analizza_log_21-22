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
- numero totale di eventi per utente (done)
- quante volte si è verificato ciascun evento (done)
- data primo evento (done)
- data ultimo evento (done)
- numero di giorni tra il primo e l'ultimo evento (done)
- altre features a piacere
"""

#TODO: Add more features
import pandas as pd
import Utils


        
#Function that calculates the distance between 2 dates

def CalculateDateDistance (str1, str2):
     date0= pd.to_datetime(str1,format="%d/%m/%Y %H:%M")
     date1= pd.to_datetime(str2,format="%d/%m/%Y %H:%M")
     dist= date1 - date0
     return abs(dist)


#Function that produces a list of features for every user
#FIXME: Try to fix formatting for the date_distance. Keep the TimeDelta format
def UserFeatures (log_list):
    df_per_user = log_list.groupby(log_list.USER_ID)
    users= range(1, log_list.USER_ID.max()+1) 
    features=[] 
    
    for i in users:
        current= df_per_user.get_group(i)
        #Feature 1: Count how many events has the user created 
        event_participations= current['USER_ID'].value_counts().tolist()
        #Feature 2: Get the first event date of the user
        first_event_date= current['DATE'].min()
        #Feature 3: Get the last event date of the user
        last_event_date= current['DATE'].max()
        #Feature 4: Get the distance between first and last event date of the user
        dates_distance= CalculateDateDistance(first_event_date, last_event_date)
        print(dates_distance, '\n\n')
        feature_obj=[i, event_participations[0], first_event_date, last_event_date, str(dates_distance)]
        features.append(feature_obj)
    #Converting the list of features into a DataFrame
    user_features= pd.DataFrame(features)
    user_features.rename(columns={ 0:'USER_ID', 1: 'Event participation', 2: 'First event date', 
                                  3:'Last event date', 4:'Date distance first and last event'}, inplace=True)
    return user_features


# Function for the feature Event type count 
#FIXME: Fix the format of the result
def EventTypeCount (log_list):
    event_type_count= []
    #Split the base Dataframe in smaller dataframes by USER_ID
    df_per_user = log_list.groupby(log_list.USER_ID) 
    #Count for every user DataFrame the events
    users= range(1, log_list.USER_ID.max()+1) 
    for i in users:
        current= df_per_user.get_group(i)
        event_counts= current.groupby('EVENT_TYPE').count()
        event_type_count.append(event_counts)
    return event_type_count

#TODO: The real file
#jsonfile = 'indata\logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json'  
#TODO: Fake file with only the first few logs for simplicity
#jsonfile = 'indata\logs_analizza1.json' 

 
args = Utils.initializeParser()
basePath, inputFile, extension = Utils.getFilePath_InputFileName_FileExtension(args)
log_list = Utils.ReadJsonFile(basePath + inputFile + extension)

log_list.rename(columns={ 0:'DATE', 1: 'USER_ID', 3: 'EVENT_TYPE'}, inplace=True)
user_features= UserFeatures(log_list)
event_type_count= EventTypeCount(log_list)

Utils.SaveJsonFile(basePath+args.output+extension, user_features)
Utils.SaveExcelFile(r'indata/User_features.xlsx', user_features, event_type_count)


print("Task ended")