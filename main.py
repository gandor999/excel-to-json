from operator import itemgetter
import pandas as pd
import json
from util.util import (
    excel_to_json_by_sheet,
    write_to_file,
    transform_to_schema,
    read_file,
)

config = read_file("config.json")

(
    excel_filename,
    json_file_to_transform,
    root_element_name,
    transform,
) = itemgetter(
    "excelFilename", "jsonFileToTransForm", "rootElementName", "transform"
)(config)


sheet_names = pd.ExcelFile(excel_filename).sheet_names

excel_dict = {}

for sheet in sheet_names:
    excel_dict[sheet] = excel_to_json_by_sheet(excel_filename, sheet)

if transform:
    transform_to_schema("WS Response.json", "Response")

write_to_file(f"{excel_filename}.json", json.dumps(excel_dict))
