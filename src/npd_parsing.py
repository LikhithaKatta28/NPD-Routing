from datetime import datetime
import logging
import os

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def read_test_csv(path, filename):
    filepath = os.path.join(path, filename)
    try:
        input_df = pd.read_csv(filepath, low_memory=False)
    except Exception as e:
        logging.error(e)

    input_df = input_df[
        ["Material", "Plnt", "GrC", "Seq.", "MTyp", "Group", "Valid From MA",
         "Valid From OP", "OpAc", "StdVal1", "UM 1", "Usage", "Stat",
         "Ctrl", "Work ctr"]]

    # Adding spaces to header column name based on max length of column value

    for col in input_df.columns:
        column_length = input_df[col].apply(lambda x: len(str(x)))
        get_diff = max(column_length) - len(col)
        insert_space = col + get_diff * ' '
        input_df.rename(columns={col: insert_space}, inplace=True)

    # Adding Spaces to column values based on Header column length in a df

    def adding_space_tovalues(column_len, value):
        length_difference = int(column_len - int(len(str(value))))
        if length_difference < column_len:
            return str(value) + length_difference * ' ' + '|'
        else:
            return str(value) + '|'

    for column_name in input_df.columns:
        input_df[column_name] = input_df[column_name].apply(
            lambda x: adding_space_tovalues(len(column_name), x))

    input_df[input_df.columns[0]] = input_df[input_df.columns[0]].apply(
        lambda x: '|' + str(x))

    #  To get +---------+ Top Row and botton row
    get_top_rows = []
    for column_name in input_df.columns:
        index_number = input_df.columns.get_loc(column_name)

        if index_number == 0:
            add_string = '+'
            get_column_length = len(column_name)
            for _ in range(0, get_column_length):
                add_string += '-'
            add_string += '+'
            get_top_rows.append(add_string)
        else:
            add_string = ''
            get_column_length = len(column_name)
            for _ in range(0, get_column_length):
                add_string += '-'
            add_string += '+'
            get_top_rows.append(add_string)

    # To get Header columns

    header_names = []
    for get_column in input_df.columns:
        index_number = input_df.columns.get_loc(get_column)
        if index_number == 0:
            header_names.append('|' + str(get_column) + '|')
        else:
            header_names.append(str(get_column) + '|')

    # input_df.loc[-2] = header_names
    input_df.loc[-1] = get_top_rows
    input_df.loc[-2] = header_names
    input_df.loc[-3] = get_top_rows

    input_df.index = input_df.index + 1
    input_df.sort_index(inplace=True)
    input_df.loc[len(input_df.index)] = get_top_rows

    print_output(filename, input_df, path)


def print_output(filename, input_df, path):
    sap_filename = get_output_name(filename)
    output_folder_path = os.path.join(path, sap_filename)
    logging.info(f'output path is: {path}')
    logging.info(f'output file name: {sap_filename}')
    np.savetxt(output_folder_path, input_df, fmt='%s')


def get_output_name(filename):
    sap_file_parts = str(filename).split('.')
    sap_file_parts[0] = 'UFO_NPD_ROUTING'
    sap_file_parts[1] = datetime.now().strftime('%Y%m%d%H%M%S')
    sap_file_parts[5] = 'txt'
    return '.'.join(sap_file_parts)
