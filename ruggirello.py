import argparse
import json
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


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="The input/output file path",
                        type=str,
                        default='indata/')
    parser.add_argument("-i", "--input",
                        help="The input file name, no extension",
                        type=str,
                        default="logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized"
                        )
    parser.add_argument("-e", "--extension",
                        help="Input/output file extension, including dot (Es -> .json)",
                        type=str,
                        default='.json')
    parser.add_argument("-o", "--output",
                        help="The output file name, no extension, Default = \'output\'",
                        type=str,
                        default='output')
    return parser.parse_args()


def readJsonFile(completeFilePath):
    try:
        jsonFile = open(completeFilePath)
        data = json.load(jsonFile)  # This is a list of lists
        jsonFile.close()
        return data
    except OSError as e:
        print(e)
        exit()
    except json.JSONDecodeError:
        print('Error! The specified input file doesn\'t contains info in json format.')
        exit()


def saveJsonFile(fileName, dumpData, indent=3):
    try:
        file = open(fileName, 'w')
        json.dump(dumpData, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def getFilePath_InputFileName_FileExtension(args):
    # Check if last words contains a dot
    filePath = args.path
    inputFileName = args.input if '.' not in args.input else args.input.split('.')[0]
    fileExtension = args.extension if '.' not in args.input else '.' + args.input.split('.')[1]
    pathSlices = filePath.split('/')
    lastIndex = len(pathSlices) - 1
    if '.' in pathSlices[lastIndex]:  # Means that the last element is a file name including extension
        fileNameAndExtension = pathSlices[lastIndex].split('.')
        inputFileName = fileNameAndExtension[0]
        fileExtension = '.' + fileNameAndExtension[1]
        del pathSlices[lastIndex]
        filePath = ''.join([(element + '/') for element in pathSlices])
    return filePath, inputFileName, fileExtension


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


if __name__ == '__main__':
    args = initializeParser()
    basePath, inputFile, extension = getFilePath_InputFileName_FileExtension(args)
    json = readJsonFile(basePath + inputFile + extension)
    userLogDictionary = extractDictionaryFromListOfLists(json, 1)  # Using Identificativo unico dell’utente as dictionary key value

