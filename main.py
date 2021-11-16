"""
Programma python Contini Maria Elena
15/11/2021


Ciascun elemento della lista di log è costituito dalle seguenti otto informazioni:

Data/Ora
Identificativo unico dell’utente
Contesto dell’evento
Componente
Evento
Descrizione
Origine
Indirizzo IP 

"""

import json
import sys
from datetime import datetime
# questo sottoprogramma legge il file json e salva i dati in una lista di liste

def read_json_file(file):
    try:
        fin = open(file)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except:
        print('*** errore *** Non è stato caricato alcun file!')
        sys.exit()
        
# questo sottoprogramma salva i dati in un nuovo file json

def save_json_file(file, data):
    try:
        fout = open(file, 'w')
        json.dump(data,fout, indent=3)
        fout.close()
    except:
        print('*** errore *** Qualcosa è andato storto durante la creazione del nuovo file')
        sys.exit()

# sottoprogramma che calcola le occorrenze dei log dei diversi user
def tot_occ(log_list):
    tab_log_user = {} # creo un dizionario vuoto in cui metto le occorrenze dei log degli utenti
    for log in log_list:
        if not log[1] in tab_log_user:
            tab_log_user[(log[1])]= {}
            tab_log_user[(log[1])]['tot_occ']=1
        else:
            tab_log_user[log[1]]['tot_occ']+=1
    return tab_log_user

def event_occurences(log_list, tab_log_user):
    
    for log in log_list:
        if log[4] not in tab_log_user[log[1]]:
            tab_log_user[log[1]][log[4]]=1
        else:
            tab_log_user[log[1]][log[4]]+=1
    eventi = set()
    for user in tab_log_user:
        eventi = eventi.union(set(tab_log_user[user].keys()))
    eventi.remove('tot_occ')
    for user in tab_log_user:
        for e in eventi:
            if e not in tab_log_user[user]:
                tab_log_user[user][e] = 0
    return tab_log_user  

def access(log_list):
    tab_time = {}
    for log in log_list:
        if not log[1] in tab_time:
            tab_time[(log[1])] = {}
            d1 = datetime.strptime(log[0], "%d/%m/%Y %H:%M")
            tab_time[(log[1])]['first access'] = d1
            tab_time[(log[1])]['last access'] = d1
        else:
            d1 = datetime.strptime(log[0], "%d/%m/%Y %H:%M")
            if tab_time[(log[1])]['first access'] > d1:
                tab_time[(log[1])]['first access'] = d1
            if tab_time[(log[1])]['last access'] < d1:
                tab_time[(log[1])]['last access'] = d1
    return tab_time
        
            
                
            
        
filein = 'indata/logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json'
log_list = read_json_file(filein)
pos = filein.rfind('/')
nomefile = filein[pos:]
tab_tot_occurences = tot_occ(log_list)
tab_tot_occurences = event_occurences(log_list, tab_tot_occurences)
tab_access= access(log_list)

save_json_file('output/occorrenze.json' , tab_tot_occurences)
# TODO (non funziona): save_json_file('output/accessi.json', tab_access)

print('fine')