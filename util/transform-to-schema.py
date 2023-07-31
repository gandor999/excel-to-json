import json
import pandas as pd

json_data = ""

with open("logs/WS Response.json") as f:
    json_data = json.loads(f.read())
    f.close()


keys_that_are_arrays = []


def create_dict_from_path(sample_path, value_element, data_type):
    temp = {}
    length_list = len(sample_path)
    current_key_name = sample_path[length_list - 1]

    if ["multiple occ. Block"].count(data_type):
        keys_that_are_arrays.append(current_key_name)

    temp[current_key_name] = (
        value_element
        if keys_that_are_arrays.count(current_key_name) == False
        else [value_element]
    )

    if length_list > 1:
        sample_path.pop(length_list - 1)
        return create_dict_from_path(sample_path, temp, ...)

    return temp


arranged_json_data = []

for data in json_data:
    if data["X-Paths"] is not None:
        arranged_json_data.append(
            create_dict_from_path(
                data["X-Paths"].split("/"),
                data["Example or Valid Values"],
                data["Data Type"],
            )
        )

# print(arranged_json_data)

with open("logs/sample.json", "w") as f:
    f.write(json.dumps(arranged_json_data))
    f.close()

with open("logs/sample-2.json", "w") as f:
    f.write(json.dumps(pd.DataFrame(arranged_json_data).to_dict("list")["Response"]))
    f.close()

df_list = pd.DataFrame(arranged_json_data).to_dict("list")["Response"]

# make a function to merge dictionaries with the same key name and depth

results = {}
for d in df_list:
    results.update(d)


with open("logs/sample-3.json", "w") as f:
    f.write(json.dumps(results))
    f.close()
