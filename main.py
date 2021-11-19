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
- data primo evento(done)
- data ultimo evento(done)
- numero di giorni tra il primo e l'ultimo evento(done)
- altre features a piacere
"""
#TODO: Add more features
import sys
import pandas as pd
from datetime import datetime



#This function reads the json file and saves its data into a list of lists (using pandas)

def ReadJsonFile(file):
    try:
        log_list = pd.read_json(file)
        return log_list
    except:
        print('Could not load the file! \nThe specified file path-name does not exist!')
        sys.exit()
    

#This function saves data onto a new json file (using pandas)

def SaveJsonFile(file, data):
    try: 
        data.to_json(file)
    except:
        print('Something went wrong during the creation of the new Json file!')
        sys.exit()
  

# =============================================================================
# 
#Fuction that saves data onto a new Excel file 
#
# def SaveExelFile(file, data):
#     try: 
#         data.to_exel(file)
#     except:
#         print('Something went wrong during the creation of the new Excel file!')
#         sys.exit()
# 
# =============================================================================
        
#This function receives 2 strings that represent 2 dates and calculates the distance
def CalculateDateDistance (str1, str2):
     date0= pd.to_datetime(str1,format="%d/%m/%Y %H:%M")
     date1= pd.to_datetime(str2,format="%d/%m/%Y %H:%M")
     dist= date1 - date0
     return dist

#TODO: Try to fix formatting for the date_distance. The result is in sec but it would be nice to keep the TimeDelta format
def UserFeatures (log_list):
    
    #Rename the columns for readability
    log_list.rename(columns={ 0:'DATE', 1: 'USER_ID', 3: 'EVENT_TYPE'}, inplace=True)
    
    #Splitting the DataFrame of logs into groups based on user_id 
    df_per_user = log_list.groupby(log_list.USER_ID)
    
    #Creating a range for the loop. The max value is the biggest ID 
    users= range(1, log_list.USER_ID.max()+1) 
    
    features=[]   
    for i in users:
        #Taking as current the DataFrame that contains only the logs of the i-th user
        current= df_per_user.get_group(i)
        
        event_participations= current['USER_ID'].value_counts().tolist()
        event_counts= current['EVENT_TYPE'].value_counts().to_frame()
        print(event_counts, '\n\n')
    
        first_event_date= current['DATE'].min()
        last_event_date= current['DATE'].max()
        dates_distance= CalculateDateDistance(first_event_date, last_event_date)
        print(dates_distance, '\n\n')
        
        feature_obj=[i, event_participations[0], event_counts, first_event_date, last_event_date, dates_distance]
        features.append(feature_obj)

    #TODO: Divide in some way lines and columns of the result file (the dataframe shape should be ok)
    #Converting the list of features into a DataFrame
    user_features= pd.DataFrame(features)
    user_features.rename(columns={ 0:'USER_ID', 1: 'Event participation', 2: 'Event type count', 
                              3: 'First event date', 4:'Last event date', 
                              5:'Date distance first and last event'}, inplace=True)
    return user_features

#TODO: The real file
jsonfile = 'indata\logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json'  

# =============================================================================
# 
# #TODO: Fake file with only the first few logs for simplicity
#jsonfile = 'indata\logs_analizza1.json'  
# 
# =============================================================================

log_list=ReadJsonFile(jsonfile)
user_features= UserFeatures(log_list)
print(user_features.loc[:, 'USER_ID':'Event type count'])
SaveJsonFile(r'indata/User_features.json', user_features)   
#SaveExelFile(r'indata/User_features.xlsx', user_features)   
print("Task ended")