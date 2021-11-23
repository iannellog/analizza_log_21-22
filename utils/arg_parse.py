import argparse


def register_and_get_args():
    parser = argparse.ArgumentParser(description='Optional input')

    parser.add_argument('-i', '--input',
                        help='Complete path of file that contains the input data to handle',
                        type=str,
                        default='./indata/logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json')

    parser.add_argument('-o', '--output',
                        help='Path of the directory in which you want to store the outputs',
                        type=str,
                        default='./outdata')

    parser.add_argument('-nj', '--no_json',
                        help='Flag to exclude generation of json file',
                        action='store_true')

    parser.add_argument('-ne', '--no_excel',
                        help='Flag to exclude generation of excel file',
                        action='store_true')

    parser.add_argument('-e', '--extra',
                        help='Flag to extract more features than requested',
                        action='store_true')

    return parser.parse_args()

