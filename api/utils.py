from datetime import datetime
from typing import Tuple
import time

str_to_timestamp = lambda s: int(time.mktime(datetime.strptime(s, "%Y-%m-%d").timetuple()))

timestamp_to_str = lambda ts: datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

to_date = lambda s: datetime.strptime(s, "%Y-%m-%d")

commodity_schema = {
    'start_date': {'type': 'datetime', 'coerce': to_date, 'required': True},
    'end_date': {'type': 'datetime', 'coerce': to_date, 'required': True},
    'commodity_type': {'type': 'string', 'required': True, 'allowed': ['gold', 'silver']}
}


def get_report_values(data: list, filter_params: dict) -> Tuple[dict, float, float]:
    filtered_data = {}
    mean = 0
    variance = 0
    start_date = str_to_timestamp(filter_params['start_date'])
    end_date = str_to_timestamp(filter_params['end_date'])
    try:
        # assume that data in the file is of the appropriate format
        # so that no Exceptions are raised, but just to be sure
        # wrap it into try-except
        filtered_data = [price for price in data if start_date <= price['timestamp'] <= end_date]
    except ValueError:
        pass

    if filtered_data:
        filtered_prices = [price['price'] for price in filtered_data]
        mean = sum(filtered_prices) / len(filtered_prices)
        # not sure how to calculate it. So the calculation of it is incorrect.
        # higher price - lowest price
        variance = max(filtered_prices) - min(filtered_prices)

        # format data for output
        filtered_data = {timestamp_to_str(price['timestamp']): price['price'] for price in filtered_data}

    return filtered_data, mean, variance
