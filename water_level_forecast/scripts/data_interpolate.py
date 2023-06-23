import pandas as pd
import csv


def run():
    with open('data_app/data_samples/rp5/cholpon.csv', encoding='utf-8') as f_read, \
            open('data_app/data_samples/rp5/changed_cholpon1.csv', 'w', encoding='utf-8') as f_write:
        for k, row in enumerate(f_read):
            if k == 0:
                f_write.write(row)
                continue
            new_row = row.rstrip("\n;")
            f_write.write(new_row + "\n")

    # ------------------------------- WATER_MEAN
    df = pd.read_csv('data_app/data_samples/sdss/issykkul_MEAN_1993-06-01.csv',
                     index_col=0,
                     sep=',',
                     date_format="%Y-%m-%dT%H:%M:%S"
                     )

    upsampled = df.resample('3H').mean()
    interpolated = upsampled.interpolate(method='linear')

    # -------------------------------- WATER_DELTA
    df = pd.read_csv('data_app/data_samples/sdss/issykkul_dVOLUME_1993-06-01.csv', index_col=0, sep=',',
                     date_format="%Y-%m-%dT%H:%M:%S")

    upsampled12 = df.resample('3H').mean()
    interpolated12 = upsampled12.interpolate(method='linear')

    merged0 = pd.merge(interpolated, interpolated12, left_index=True, right_index=True)

    # -------------------------------- NOAA BISH TEMP
    df = pd.read_csv('data_app/data_samples/noaa/bish_noaa.csv', index_col=None, sep=',', parse_dates=[2])

    df = df.drop(columns=['STATION', 'PRCP', 'SNWD'])
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.set_index('DATE')
    # print(df.head())

    upsampled1 = df.resample('3H').mean()
    interpolated1 = upsampled1.interpolate(method='linear')

    merged = pd.merge(merged0, interpolated1, left_index=True, right_index=True, how='left')
    merged = merged.fillna(0)

    # -------------------------------- CHOLPON ATA DATA
    f = pd.read_csv('data_app/data_samples/rp5/changed_cholpon1.csv',
                    delimiter=';',
                    header=0,
                    parse_dates=[0],
                    index_col=0,
                    encoding='utf-8',
                    date_format="%d.%m.%Y %H:%M",
                    comment='#',
                    ).rename(columns={"Местное время в Чолпон-Ате": "date/time"})


    def get_first_num(s):
        if isinstance(s, float):
            return s
        res = ""
        for i in s:
            if i.isdigit():
                res += i
            else:
                break
        if res == '':
            return 0
        return float(res)


    f = f.drop(
        columns=["P", "DD", "Ff", "ff10", "ff3", "N", "WW", "W1", "W2", "Tn", "Tx", "Cl", "Nh", "Cm", "Ch", "VV", "Td",
                 "RRR", "tR", "E", "Tg", "E'", "sss", "Pa"])

    f['H'] = f['H'].apply(lambda s: get_first_num(s))

    ar = f.iloc[::-1]

    upsampled2 = ar.resample("3H").mean()
    interpolated2 = upsampled2.interpolate("linear")

    merged1 = pd.merge(merged, interpolated2, left_index=True, right_index=True, how='left')
    merged1 = merged1.fillna(0)

    # ----------------------------------- REST DATA
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

    global merged_df
    previous_df = None
    for req in data_struct[2:]:
        df = pd.read_csv(f"data_app/data_samples/sdss/{req[3]}_{req[1]}_{req[4]}.csv",
                         # na_values=data_struct[param][0],
                         header=0,
                         parse_dates=[0],
                         index_col=0,
                         date_format="%Y-%m-%dT%H:%M:%S").rename(columns={req[1]: req[2]})

        upsampled = df.resample('3H').mean()
        interpolated = upsampled.interpolate(method='spline', order=2)

        if previous_df is None:
            previous_df = interpolated  # Сохранение первого датафрейма
        else:
            merged_df = pd.merge(previous_df, interpolated, left_index=True, right_index=True)
            previous_df = merged_df  # Обновление предыдущего датафрейма

    merged2 = pd.merge(merged1, merged_df, left_index=True, right_index=True, how='left')
    merged2 = merged2.fillna(0)

    merged2.to_csv("data_app/data_samples/merged.csv")


if __name__ == '__main__':
    run()
