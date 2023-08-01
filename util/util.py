import json
import pandas as pd


class Record_Array:
    """Record_Array

    Description: An array that keeps tabs on one array
    """

    def __init__(self, record_array=[]):
        self.record_array = record_array

    def get(self):
        return self.record_array

    def append(self, data):
        self.record_array.append(data)

    def count(self, data):
        return self.record_array.count(data)


def write_to_file(filename, data):
    with open(f"logs/{filename}", "w") as f:
        f.write(data)
        print(f"Wrote log for logs/{filename}")
        f.close()


def read_file(filename):
    data = ""

    with open(f"{filename}") as f:
        data = json.loads(f.read())
        print(f"Content of {filename} is: ", data)
        f.close()

    return data


def list_to_dict(list):
    temp = {}
    for i in range(len(list)):
        temp[list[i][0]] = list[i][1]

    return temp


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
            temp.append((col_names[i], row_values[i][j]))
        group_by_row.append(list_to_dict(temp))

    write_to_file(f"{sheet_name}.json", json.dumps(group_by_row))

    return group_by_row


def create_dict_from_path(
    sample_path, value_element, data_type, record_array: Record_Array
):
    temp = {}
    length_list = len(sample_path)
    current_key_name = sample_path[length_list - 1]

    if ["multiple occ. Block"].count(data_type):
        record_array.append(current_key_name)

    temp[current_key_name] = (
        value_element
        if record_array.count(current_key_name) == False
        else [value_element]
    )

    if length_list > 1:
        sample_path.pop(length_list - 1)
        return create_dict_from_path(sample_path, temp, ..., record_array)

    return temp


def transform_to_schema(filename, root_element_name):
    json_data = read_file(f"logs/{filename}")

    record_array = Record_Array([])

    arranged_json_data = []

    for data in json_data:
        if data["X-Paths"] is not None:
            arranged_json_data.append(
                create_dict_from_path(
                    data["X-Paths"].split("/"),
                    data["Example or Valid Values"],
                    data["Data Type"],
                    record_array,
                )
            )

    df_list = pd.DataFrame(arranged_json_data).to_dict("list")[root_element_name]

    # TODO: make a function to merge dictionaries with the same key name and depth

    results = {}
    for d in df_list:
        results.update(d)

    write_to_file("arranged_json_data.json", json.dumps(arranged_json_data))

    write_to_file(
        "df_list.json",
        json.dumps(df_list),
    )

    write_to_file("results.json", json.dumps(results))
