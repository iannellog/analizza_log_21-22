import json
import sys
import argparse
import pandas as pd


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="The input/output file path",
                        type=str,
                        default='indata/')
    
    parser.add_argument("-i", "--input",
                        help="The input file name, no extension",
                        type=str,
                        default="logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized")
    
    parser.add_argument("-e", "--extension",
                        help="Input file extension, including dot (Es -> .json)",
                        type=str,
                        default='.json')
    
    parser.add_argument("-o", "--output",
                        help="The Json output file name, no extension, Default = \'output\'",
                        type=str,
                        default='Json_Output')
    
    return parser.parse_args()


#This function reads the json file and saves its data into a DataFrame 

def ReadJsonFile(path):
    try:
        file= open(path)
        log_list = pd.read_json(file)
        file.close()
        return log_list
    except OSError as e:
        print(e)
        sys.exit()
    except json.JSONDecodeError:
        print('Error! The data in the file is not in json format!!')
        sys.exit()


#This function saves data onto a new json file 
#FIXME: Some values get badly converted
def SaveJsonFile(file, data):
    try: 
        data.to_json(file, indent= 3, orient='table')
    except OSError as e:
        print(e)
        sys.exit()
        
#Fuction that saves data onto a new Excel file (Using multi-sheet for the Event type counter) 

def SaveExcelFile(file, data, data2):
    try: 
        writer = pd.ExcelWriter(file)
        data.to_excel(writer, 'USER FEATURES')
        
        for n, df in enumerate(data2):
            df.columns= ['COUNT', 1,2,3,4,5,6]
            df.drop(df.columns[[1,2,3,4,5,6]], axis=1, inplace=True)
            df.to_excel(writer,'Events for User %s' %(n+1))
        writer.save()
    except OSError as e:
        print(e)
        sys.exit()

  
    
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

