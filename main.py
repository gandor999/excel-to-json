import pandas as pd
import json


def write_to_file(filename, data):
    with open(f"logs/{filename}", "w") as f:
        f.write(data)
        f.close()


def list_to_dict(list):



def excel_to_json_by_sheet(filename, sheet_name):
    # to get rid of null convert to json first then to dict
    sheet = json.loads(pd.read_excel(filename, sheet_name=sheet_name).to_json())

    col_names = []
    row_values = []

    for k, v in sheet.items():
        col_names.append(k)
        row_values.append(list(v.values()))

    col_length = len(col_names)
    row_length = len(row_values[0])

    group_by_row = []

    # iterate over values
    # arrange them with same index

    for j in range(row_length):
        temp = []
        for i in range(col_length):
            print(col_names[i], row_values[i][j])
            temp.append((col_names[i], row_values[i][j]))
        group_by_row.append(list_to_dict(temp))

    write_to_file(f"{sheet_name}.json", json.dumps(group_by_row))

    return group_by_row


