import requests
import csv
from datetime import datetime


def days_until_past_date(target_date):
    current_date = datetime.now().date()
    delta = current_date - target_date
    return delta.days


def run():

    # SDSS data request
    data_struct = [
        ["-nan", "MEAN", "WaterMean", "issykkul", "1993-06-01"],
        ["-nan", "dVOLUME", "DeltaVolume", "issykkul", "1993-06-01"],
        ["-nan", "Rain_Tot", "balyRainTot", 'baly', "2018-05-19"],
        ["-nan", "Rain_Tot", "goluRainTot", 'golu', "2014-01-01"],
        ["-nan", "S1_ice", "goluIceContent", 'golu', "2014-01-01"],
        ["-999", "SH", "goluSnowDensity", 'golu', "2014-01-01"],
        ["-nan", "AirTC", "taraAirTemp", 'tara', "2018-05-19"],
        ["-nan", "AirTC", "zokaAirTemp", 'zoka', "2018-05-19"],
        ["-nan", "Rain_Tot", "taraRainTot", 'zoka', "2018-05-19"],
    ]

    def days_between(start_date):
        current_date = datetime.now().date()
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        days = (current_date - start_date).days
        return days

    for req in data_struct:
        days = days_between(req[4])
        REQUEST_URL = f"http://sdss.caiag.kg/sdss/service.php?mode=get_data&station={req[3]}&date={req[4]}&duration={days - 3}&descriptor={req[1]}"

        with requests.Session() as s:
            download = s.get(REQUEST_URL)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            with open(f'data_app/data_samples/sdss/{req[3]}_{req[1]}_{req[4]}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for row in my_list:
                    writer.writerow(row)

    # NOAA data request
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    REQUEST_URL = f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=PRCP,SNWD,TAVG,TMAX,TMIN&stations=KG000038353&startDate=1997-12-01&endDate={now_str}&includeStationName=false"

    with requests.Session() as s:
        download = s.get(REQUEST_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        with open(f'data_app/data_samples/noaa/bish_noaa.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in my_list:
                writer.writerow(row)
