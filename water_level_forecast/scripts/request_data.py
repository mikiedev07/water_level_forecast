import requests
import csv
from datetime import datetime


def days_until_past_date(target_date):
    current_date = datetime.now().date()
    delta = current_date - target_date
    return delta.days


def run():
    past_date = datetime(1993, 5, 14).date()
    days = days_until_past_date(past_date)

    REQUEST_URL = f"http://sdss.caiag.kg/sdss/service.php?mode=get_data&station=issykkul&date=1993-05-14&duration={days - 3}&descriptor=MEAN"

    with requests.Session() as s:
        download = s.get(REQUEST_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        with open('data_app/data_samples/exp/example.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in my_list:
                writer.writerow(row)
