import pandas as pd
import matplotlib.pyplot as plt
from darts.metrics import *
from darts.models import *
from darts import TimeSeries
from data_app.models import (
    ExpSmoothing,
    ExpSmoothingForecast,
    ExpSmoothingParams,
    ExpSmoothingMetrics
)


def populate_db_models(model, dataframe):
    if model.objects.count() > 0:
        model.objects.all().delete()
    for index, row in dataframe.iterrows():
        model.objects.create(date=index, value=row['MEAN'])


def run():
    # Загрузка данных из CSV-файла
    df = pd.read_csv('data_app/data_samples/exp/example.csv', parse_dates=['date/time'], index_col='date/time')

    params = ExpSmoothingParams.objects.first()

    df.dropna(inplace=True)
    df = df.asfreq(params.interp_frequency, method='ffill')
    series = TimeSeries.from_dataframe(df)

    populate_db_models(ExpSmoothing, df)

    # metrics
    start = pd.Timestamp('051510')
    df_metrics = pd.DataFrame()

    def plot_backtest(series, forecast, model_name):
        idx = -144
        series[idx:].plot(label='Actual Values')
        forecast[idx:].plot(label='Forecast')
        plt.title(model_name)
        plt.show()

    # autocorelation
    # fig, ax = plt.subplots(figsize=(8, 5))
    # plot_acf(df, ax=ax)

    # Predict
    model = ExponentialSmoothing(seasonal_periods=params.seasonal_periods)
    model_name = 'Exponential Smoothing'

    forecast = model.historical_forecasts(series, start=start, forecast_horizon=params.forecast_horizon, verbose=True)
    # plot_backtest(series, forecast, model_name)

    ExpSmoothingMetrics.objects.create(
        mae=round(mae(series, forecast), 2),
        rmse=round(rmse(series, forecast), 2),
        mape=round(mape(series, forecast), 2),
        smape=round(smape(series, forecast), 2)
    )

    model.fit(series)
    forecast = model.predict(params.forecast_horizon)

    populate_db_models(ExpSmoothingForecast, forecast.pd_dataframe())

    # plot_backtest(series, forecast, model_name)
    # print(forecast.pd_dataframe())
    # print(df_metrics)

    # plt.show()
