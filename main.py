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

        
        
log_list = read_json_file('/Users/mariaelenacontini/Desktop/programmazione/analizza_git/analizza_log_21-22/indata/caso_di_test.json')
tab_tot_occurences = tot_occ(log_list)
tab_tot_occurences = event_occurences(log_list, tab_tot_occurences)

print('fine')