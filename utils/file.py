import pandas as pd
from utils import constants, handle_exception
import os


def json_file_to_dataframe(path):
    """
    transform json given into a DataFrame to analyze data
    :param path: path of json file to read
    :return pandas.DataFrame
    """
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
    except OSError as e:
        handle_exception.fatal_error(e)
    except Exception as e:
        handle_exception.fatal_error(f'*** generic error *** {e}')


def save_features(data_out, directory, exclude_json=False, exclude_excel=False,):
    """
    save features extracted into the directory indicated. It's possible to exclude some outputs.
    :param data_out: DataFrame to
    :param directory: path indicated in which outputs will be stored
    :param exclude_json: boolean to exclude generation of json file
    :param exclude_excel: boolean to exclude generation of json file
    :return None
    """
    print('\n============= Save features =============')

    if exclude_json and exclude_excel:
        print('Output not saved as requested!')
        return

    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    except OSError as e:
        handle_exception.fatal_error(e)

    if not exclude_json:
        try:
            full_path_json = os.path.join(directory, 'features.json')
            data_out.to_json(full_path_json, orient='index')
            print(f'Json file saved in location: {full_path_json}')
        except OSError as e:
            handle_exception.fatal_error(e)
        except Exception as e:
            handle_exception.fatal_error(f'*** generic error during json saving*** {e}')

    if not exclude_excel:
        try:
            full_path_xlsx = os.path.join(directory, 'features.xlsx')
            data_out.to_excel(full_path_xlsx)
            print(f'Excel file saved in location: {full_path_xlsx}')
        except OSError as e:
            handle_exception.fatal_error(e)
        except Exception as e:
            handle_exception.fatal_error(f'*** generic error during xlxs saving *** {e}')

