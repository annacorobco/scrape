import json

from flask import Flask
from flask import jsonify
from flask import request
from cerberus import Validator

from utils import commodity_schema, get_report_values

app = Flask(__name__)
DATA_FILE_PATH = 'scrape_websites/data.json'


@app.route('/commodity', methods=['GET', ])
def commodity_info():
    get_params = request.args.to_dict()
    v = Validator(commodity_schema)
    if not v.validate(get_params):
        return jsonify({'success': False, 'errors': v.errors})

    filtered_data = {}
    mean = 0
    variance = 0
    with open(DATA_FILE_PATH, 'r') as f:
        data = f.read()

    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            jsonify({'success': False, 'errors': 'Cannot load data from file'})

        data = data.get(get_params['commodity_type'])
        filtered_data, mean, variance = get_report_values(data=data, filter_params=get_params)

    return jsonify({'success': True, 'data': filtered_data, 'mean': mean, 'variance': variance})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
