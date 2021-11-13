import Utils
from Utils import convertToDate as s2d
from Utils import convertDateToString as d2s
import time


"""
Json file info:
    [0] Data/Ora
    [1] Identificativo unico dell’utente
    [2] Contesto dell’evento
    [3] Componente
    [4] Evento
    [5] Descrizione
    [6] Origine
    [7] Indirizzo IP


Needed info for each user:
    - numero totale di eventi
    - quante volte si è verificato ciascun evento
    - data primo evento
    - data ultimo evento
    - numero di giorni tra il primo e l'ultimo evento
    - media e varianza del numero eventi in una settimana (da lunedi' a domenica)
    - altre features a piacere

"""

FEATURE_1_NAME = 'Numero totale di eventi'
FEATURE_2_NAME = 'Ripetizioni per evento'
FEATURE_3_NAME = 'Data primo evento'
FEATURE_4_NAME = 'Data ultimo evento'
FEATURE_5_NAME = 'Numero di giorni tra il primo e l\'ultimo evento'

"""
Info order in dictionary
    [0] Data/Ora
    [1] Contesto dell’evento
    [2] Componente
    [3] Evento
    [4] Descrizione
    [5] Origine
    [6] Indirizzo IP
"""


def extractDictionaryFromListOfLists(listOfLogs, keyValueIndex):  # keyValueIndex is the field used as a key of the new dictionary
    mainDict = {}
    for userLog in listOfLogs:
        keyValue = userLog[keyValueIndex]
        del userLog[keyValueIndex]  # Removing userIndex from list
        if keyValue in mainDict:
            mainDict[keyValue].append(userLog)
        else:
            mainDict[keyValue] = [userLog]
    return mainDict


def feature2Check(feature2, eventName):
    if eventName.capitalize() in feature2:
        feature2[eventName.capitalize()] += 1
    else:
        feature2[eventName.capitalize()] = 1


def extractAllFeatures(listOfLogs):
    userDictionary = {}
    feature2 = {}
    feature3 = s2d(listOfLogs[0][0])
    feature4 = s2d(listOfLogs[0][0])
    for log in listOfLogs:
        feature2Check(feature2, log[3])
        feature3 = s2d(log[0]) if s2d(log[0]) < feature3 else feature3
        feature4 = s2d(log[0]) if s2d(log[0]) > feature4 else feature4

    userDictionary[FEATURE_1_NAME] = len(listOfLogs)
    userDictionary[FEATURE_2_NAME] = feature2
    userDictionary[FEATURE_3_NAME] = d2s(feature3)
    userDictionary[FEATURE_4_NAME] = d2s(feature4)
    userDictionary[FEATURE_5_NAME] = (feature4 - feature3).days
    return userDictionary


def extractFeatures(logDictionary):
    features = {}
    for userCode, userLogs in logDictionary.items():
        features[userCode] = extractAllFeatures(userLogs)
    return features


if __name__ == '__main__':
    start = time.time()
    args = Utils.initializeParser()
    basePath, inputFile, extension = Utils.getFilePath_InputFileName_FileExtension(args)
    json = Utils.readJsonFile(basePath + inputFile + extension)
    userLogDictionary = extractDictionaryFromListOfLists(json, 1)  # Using Identificativo unico dell’utente as dictionary key value
    featureDictionary = extractFeatures(userLogDictionary)
    Utils.saveJsonFile(basePath+args.output+extension, featureDictionary)
    print('End after %s' %(time.time() - start))
