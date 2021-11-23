import pandas as pd
from utils import constants
import os


def json_file_to_dataframe(path):
    try:
        print('============= Read files =============')
        print(f'Reading file: {path}')
        df = pd.read_json(path, dtype=str)
        df.columns = [
            constants.DATETIME,
            constants.ID_USER,
            constants.CONTEXT_EVENT,
            constants.COMPONENT,
            constants.EVENT,
            constants.DESCRIPTION,
            constants.ORIGIN,
            constants.IP_ADDRESS
        ]
        print('File read successfully!')
        return df
    except Exception as e:
        print(e)
        exit(1)


def save_features(data_out, directory, exclude_json=False, exclude_excel=False,):
    print('\n============= Save features =============')

    if exclude_json and exclude_excel:
        print('Output not saved as requested!')
        return

    if not os.path.exists(directory):
        os.mkdir(directory)

    if not exclude_json:
        full_path_json = os.path.join(directory, 'features.json')
        data_out.to_json(full_path_json, orient='index')
        print(f'Json file saved in location: {full_path_json}')

    if not exclude_excel:
        full_path_xlsx = os.path.join(directory, 'features.xlsx')
        data_out.to_excel(full_path_xlsx)
        print(f'Excel file saved in location: {full_path_xlsx}')

