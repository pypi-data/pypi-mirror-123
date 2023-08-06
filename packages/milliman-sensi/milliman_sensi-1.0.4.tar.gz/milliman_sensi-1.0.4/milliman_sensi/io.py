import json
import os
import re
import shutil
import argparse

import pandas as pd
import numpy as np
import milliman_sensi.syntax as syn

from pathlib import Path

pd.options.mode.chained_assignment = None  # Used to supress panda warning
SENSI_CONFIG_HEADER = ['Scenario', 'Stress name', 'Apply stress']

# IR -> Nominal_rates
# RIR -> Real_rates
# EQ -> Equity
# RE -> Real_estate
# CRED -> Credit
# FX -> FX_rate

def read_json_file(file_path):
    data = None
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
    except Exception as e:
        # print(e)
        pass

    return data


def find_file_in_directory(filename, dir):
    for root, dirs, files in os.walk(dir):
        if filename in files:
            return os.path.join(root, filename).replace("\\", "/")
    return None


def validate_sensi_config(filepath):
    if os.path.exists(filepath) is False:
        return "{} doesn't exist".format(filepath)

    sensi_config = pd.read_csv(filepath, sep=r'~', squeeze=True, header=None)
    sensi_config = sensi_config.map(lambda x: re.sub(r'"([^"]*)"', lambda m: re.sub(r';', '_SEMI_COL', m.group()), x))

    sensi_config = pd.concat([
        sensi_config.str.split(';', expand=True),
        sensi_config.str.count(';').rename('_count_sep')
        ], axis=1)

    if sensi_config['_count_sep'].nunique(dropna=True) != 1:
        sensi_config_rows_with_more_columns = sensi_config[
            sensi_config['_count_sep'] > sensi_config.iloc[0]['_count_sep']]['_count_sep']
        sensi_config_rows_with_less_columns = sensi_config[
            sensi_config['_count_sep'] < sensi_config.iloc[0]['_count_sep']]['_count_sep']

        message1 = "" if sensi_config_rows_with_more_columns.empty else "Rows with additional columns are {}".format(list(sensi_config_rows_with_more_columns.index.values))
        message2 = "" if sensi_config_rows_with_less_columns.empty else "Rows with fewer columns are {}".format(list(sensi_config_rows_with_less_columns.index.values))

        return '\n'.join([message1, message2])

    else:
        sensi_config = sensi_config.drop(columns=['_count_sep'])
        sensi_config.columns = sensi_config.iloc[0]
        sensi_config = sensi_config[1:]
        sensi_config.reset_index(drop=True)

    sensi_config_copy = sensi_config

    sensi_config_columns = list(sensi_config_copy.columns)
    message = []

    if len(sensi_config_columns) > len(SENSI_CONFIG_HEADER):
        difference = list(set(sensi_config_columns) - set(SENSI_CONFIG_HEADER))
        for ele in sorted(difference):
            message.append("'Sensi_config.csv': '{}' is extra".format(ele))

    elif len(sensi_config_columns) < len(SENSI_CONFIG_HEADER):
        difference = list(set(SENSI_CONFIG_HEADER) - set(sensi_config_columns))
        for ele in sorted(difference):
            message.append("'Sensi_config.csv': '{}' is missing".format(ele))

    else:
        for index in range(len(sensi_config_columns)):
            if sensi_config_columns[index] != SENSI_CONFIG_HEADER[index]:
                message.append("'Sensi_config.csv': '{}' is incorrect, should be '{}'"
                               .format(sensi_config_columns[index], SENSI_CONFIG_HEADER[index]))

    if message:
        return '\n'.join(message)
    else:
        if sensi_config_copy['Apply stress'].dtype != bool:
            d = {'true': True, 'false': False}
            sensi_config_copy['Apply stress'] = sensi_config_copy['Apply stress'].apply(
                lambda x: x if isinstance(x, bool) or x.lower() not in ['true', 'false'] else d[x.lower()])
            incorrect_values = sensi_config_copy[(sensi_config_copy[['Apply stress']].applymap(type) != bool).any(axis=1)]
            if not incorrect_values.empty:
                return "'Sensi_config.csv': 'Apply stress' has incorrect entry at row(s) {}".format(
                    list(incorrect_values.index.values))

    return sensi_config


def validate_sensi_param(filepath):
    if os.path.exists(filepath) is False:
        return "{} doesn't exist".format(filepath)

    sensi_param = pd.read_csv(filepath, sep=r'~', squeeze=True, header=None)
    sensi_param = sensi_param.map(lambda x: re.sub(r'"([^"]*)"', lambda m: re.sub(r';', '_SEMI_COL', m.group()), x))

    sensi_param = pd.concat([
        sensi_param.str.split(';', expand=True),
        sensi_param.str.count(';').rename('_count_sep')
        ], axis=1)

    if sensi_param['_count_sep'].nunique(dropna=True) != 1:
        sensi_param_rows_with_more_columns = sensi_param[
            sensi_param['_count_sep'] > sensi_param.iloc[0]['_count_sep']]['_count_sep']
        sensi_param_rows_with_less_columns = sensi_param[
            sensi_param['_count_sep'] < sensi_param.iloc[0]['_count_sep']]['_count_sep']

        message1 = "" if sensi_param_rows_with_more_columns.empty else "Rows with additional columns are {}".format(list(sensi_param_rows_with_more_columns.index.values))
        message2 = "" if sensi_param_rows_with_less_columns.empty else "Rows with fewer columns are {}".format(list(sensi_param_rows_with_less_columns.index.values))

        return '\n'.join([message1, message2])
    else:
        sensi_param = sensi_param.drop(columns=['_count_sep'])
        sensi_param.columns = sensi_param.iloc[0]
        sensi_param = sensi_param[1:]
        sensi_param.reset_index(drop=True)

    sensi_param_copy = sensi_param

    sensi_param_columns = list(sensi_param_copy.columns)
    message = ""

    if sensi_param_columns[0] != 'Name':
        message = "'Sensi_param.csv': 'Name' doesn't exist"

    if message:
        return message

    return sensi_param


def read_sensitivities(env_dir):
    sensi_list = {}
    param_map = {}

    # TODO:
    #  1. Read Sensi_config.csv & Sensi_param.csv in the /sensitivities directory (throw error if column not match)
    #  2. Sanitary check for columns in both csv files
    # RETURN: sensi_list, param_map
    #  sensi_list: Name_in_Sensi_config -> [List_of_Stress_name_in_Sensi_config_in_order]
    #    eg: "Sensi_1" -> ["Stress_vol_1", "Stress_eq_vol_1"]
    #  param_map: Stress_name_in_Sensi_param -> [List_of_Parameters_syntax_in_Sensi_param]
    #    eg: "Stress_vol_1" -> ["param.H=(+100)","file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]=(+100)"]

    result = validate_sensi_config(find_file_in_directory('Sensi_config.csv', env_dir))
    if isinstance(result, str):
        # print(result)
        return sensi_list, param_map
    sensi_config = result

    result = validate_sensi_param(find_file_in_directory('Sensi_param.csv', env_dir))
    if isinstance(result, str):
        # print(result)
        return sensi_list, param_map
    sensi_param = result

    sensi_list = dict(sensi_config[sensi_config['Apply stress'] == True].groupby(['Scenario'])['Stress name'].apply(list))

    # TODO: To cross check the Stress names in the Sensi_param -> To add a unit test
    # Check if colmuns of sensi_config['Stress name'] values all are columns in sensi_param
    if not set(sensi_config['Stress name']).issubset(set(sensi_param.columns)):
        # print("Columns {} in sensi_param don't match the values in sensi_config".format(sensi_config['Stress name'] - set(sensi_param.columns)))
        pass

    param_map_unsorted = {}

    for stress_name in list(sensi_param.columns)[1:]:
        # Drop all rows with empty values for that stress_name
        sensi_param_cleaned = sensi_param[['Name', stress_name]]
        sensi_param_cleaned.replace('', np.nan, inplace=True)
        sensi_param_cleaned.dropna(inplace=True)
        # Concatenate values
        sensi_param_cleaned[stress_name] = sensi_param_cleaned['Name'] + '=' + sensi_param_cleaned[stress_name].astype(str)
        param_map_unsorted[stress_name] = sensi_param_cleaned.to_dict('list')[stress_name]

    # Ordering Stress names in param_map following the values in sensi_config.csv
    param_map = {key: param_map_unsorted[key] for key in sensi_config[sensi_config['Apply stress'] == True]['Stress name']}

    return sensi_list, param_map


def create_one_sensi_from_base(sensi_name, base_dir):
    # Create new directory and copy the content from base_dir to
    #  C:/Users/quincy.hsieh/Desktop/Workspace/CHESS-Sensitivity-Manager/sensitivity/tests/Central_RN_Simulation_20201218_152857
    path_to_sensi = None

    # Checks if base_dir exists
    if os.path.exists(base_dir):
        path = Path(base_dir)
        parent_dir = path.parent

        # Checks if sensi_dir already exists
        path_to_sensi = os.path.join(parent_dir, sensi_name).replace("\\", '/')
        if os.path.exists(path_to_sensi):
            # print("{} directory already exists, deleting it".format(path_to_sensi))
            shutil.rmtree(path_to_sensi)

        # Copies the files
        try:
            # print("Copying files to {}".format(path_to_sensi))
            shutil.copytree(base_dir, path_to_sensi)
        except shutil.Error as exc:
            errors = exc.args[0]
            for error in errors:
                src, dst, msg = error
                # print("can't copy {} to {}: {}".format(src, dst, error))
            path_to_sensi = None

    else:
        # print("Can't create a sensi_dir because {} doesn't exist".format(base_dir))
        pass

    return path_to_sensi


class SensiConfig:
    def __init__(self, env_dir):
        self.base_dir = env_dir
        self.settings_json = read_json_file(f'{env_dir}/resources/settings.json')
        self.sensi_list, self.param_map = read_sensitivities(self.base_dir)

    def create_tables(self):
        # For Seni_config.csv
        # To new create directory from the name of the Scenario
        # Copy env_dir to each directory of the name of the Scenario
        # Replace gen_param.name = name of the Scenario in the settings.json of the newly copied directory
        # Replace gen_param.path = newly created path

        if self.sensi_list:
            for sensi in self.sensi_list.keys():
                path_to_sensi = create_one_sensi_from_base(sensi, self.base_dir)
                if path_to_sensi:
                    settings_json_sensi = read_json_file(f'{path_to_sensi}/resources/settings.json')
                    settings_json_sensi['gen_param']['name'] = sensi
                    settings_json_sensi['gen_param']['path'] = path_to_sensi.replace("\\", "/")
                    with open(os.path.join(path_to_sensi, 'resources/settings.json').replace("\\", "/"), 'w') as f:
                        # print("Modifying {}".format(os.path.join(path_to_sensi, 'resources/settings.json').replace("\\", "/")))
                        f.write(json.dumps(settings_json_sensi, indent=4))
        else:
            # print("sensi_list is empty")
            pass

        # for sensi in sensi_list:
        #     # C:/Users/quincy.hsieh/Desktop/Workspace/CHESS-Sensitivity-Manager/sensitivity/tests/sensi_name
        #     create_one_sensi_from_base(sensi_name, self.base_dir)

    def apply(self):
        # For Sensi_param.csv
        # Iterate over sensi_list and apply the stress in the param_map
        # When interate param_map:
        # Build the good correct path from the json query
        # Call syntax.apply_sentax_to_file(path, syntax) in the syntax.py

        if self.param_map:
            if os.path.exists(self.base_dir):
                path = Path(self.base_dir)
                parent_dir = path.parent

                for sensi_name in self.sensi_list.keys():
                    sensi_dirpath = f'{parent_dir}/{sensi_name}'
                    settings_json_sensi = read_json_file(os.path.join(sensi_dirpath, 'resources/settings.json').replace("\\", "/"))
                    if sensi_dirpath:
                        for stress_name in self.sensi_list[sensi_name]:
                            for command in self.param_map[stress_name]:
                                syntax = syn.parse_param(command)
                                path_to_file = syn.get_input_file_path(settings_json_sensi, syntax.expression, sensi_dirpath)
                                if path_to_file:
                                    # print("\nModifying the input file at {} using the following :".format(path_to_file))
                                    # print(stress_name, ":", end=" ")
                                    syn.apply_syntax_to_file(path_to_file, syntax, settings_json_sensi)


def main(env_dir):
    sensi_list, param_map = read_sensitivities(env_dir)
    sensi_config = SensiConfig(env_dir)
    sensi_config.create_tables()
    sensi_config.apply()


if __name__ == "__main__":
    # execute only if run as a script
    parser = argparse.ArgumentParser(description='Sensitivity modifier for settings.json in CHESS.')
    parser.add_argument("-d", "--env_dir", type=str, required=True, help='The environment directory for CHESS')
    args = parser.parse_args()
    # print("Given args: {}".format(args))
    main(args.env_dir)
