import pandas as pd
from utils import arg_parse as args, file as file, constants
from handle_data import populate_data as hdp

if __name__ == '__main__':
    print('Application started!\n')

    arguments = args.register_and_get_args()
    data_frame_logs = file.json_file_to_dataframe(arguments.input)
    list_users = hdp.get_users_list(data_frame_logs)

    print(f'\nFound {data_frame_logs.shape[0]} logs of {list_users.size} anonymous users!')

    data_frame_output = pd.DataFrame({}, index=list_users)
    data_frame_output.index.name = constants.ID_USER
    hdp.populate_data_frame_output(data_frame_output, data_frame_logs, extra=arguments.extra)
    file.save_features(data_frame_output,
                       arguments.output,
                       exclude_json=arguments.no_json,
                       exclude_excel=arguments.no_excel)
    print('\nApplication completed!\n\nFollowing info about features:')
    print(data_frame_output.info())
