# excel-to-json

#### Description
This is an app that converts an excel file to a json file following a format: 

```
{
    "column_name": "row_value"
}
```

#### Installation
You can just clone the repository
`git clone <todo: update this with remote repo url>`

Then run:

   - `python3 -m venv venv`
   - For windows: `venv\Scripts\activate.bat` or something similar on your end. As long as you run `activate.bat`
   - `pip install -r requirements.txt`

#### Usage
`venv\Scripts\python.exe main.py` or `venv/Scripts/python.exe main.py`

To specify what file to convert, change the `excelFile` value in `config.json` to the desired one.