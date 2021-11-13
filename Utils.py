import json
import argparse
from datetime import datetime

DATE_FORMAT = '%d/%m/%Y %H:%M'


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
                        help="Input file extension, including dot (Es -> .json)",
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


def saveJsonFile(filePath, dumpData, indent=3):
    try:
        file = open(filePath, 'w')
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


def convertToDate(dateAsString):
    return datetime.strptime(dateAsString, DATE_FORMAT)


def convertDateToString(StringAsDate):
    return StringAsDate.strftime(DATE_FORMAT)