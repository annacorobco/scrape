import json
import os
import re
import requests

from typing import Tuple

FIELD_COL_MAPPING = {
    "date": 0,
    "price": 1
}
TABLE_ID = "curr_table"
TOTAL_COLS = 6   # should be calculated automatically
FILE_NAME = "data.json"


def get_data(url: str) -> Tuple[bool, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.80 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True, re.sub(r'>\s\s*<', '><', response.text)        # replace whitespaces
    return False, ''


def extract_data(html: str) -> list:
    table = re.search(r'<table .* id="{}".*</table>'.format(TABLE_ID), html)
    if table:
        table = table.group(0)
    tbody = re.search(r'<tbody>.*</tbody>', table)
    if tbody:
        tbody = tbody.group(0)

    # get real values
    values = re.findall(r'data-real-value="([0-9,.\-%]*)"', tbody)

    result_data = []
    start_i = FIELD_COL_MAPPING['date']
    # there are no classes for the columns we need, so we have to use
    # their order. Also it is better to get column indexes automatically
    # as well, by calculating it having info with the respective text "Price", "Date"
    # in the table header
    while start_i < len(values):
        try:
            # Convert data here so we have consistent data in the file
            result_data.append({
                'timestamp': int(values[start_i]),
                'price': float(values[start_i + 1].replace(',', ''))
            })
            start_i += TOTAL_COLS
        except ValueError:
            # it is bad, but just skip it
            pass
    print(result_data)
    return result_data


def save_to_file(data: list, key: str) -> None:
    contents = {}
    try:
        if os.path.getsize(FILE_NAME) > 0:
            # get saved data
            with open(FILE_NAME, "r") as f:
                contents = f.read()
            if contents:
                try:
                    contents = json.loads(contents)
                except json.JSONDecodeError:
                    pass
    except OSError as e:
        pass
    # update data
    # data for the same keys will be updated
    contents.update({
        key: data
    })
    with open(FILE_NAME, "w+") as f:
        f.write(json.dumps(contents))
