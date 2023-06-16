from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import ExpSmoothing, ExpSmoothingForecast, ExpSmoothingMetrics


@login_required
def graph_view(request):
    exp_smoothing_data = ExpSmoothing.objects.all()
    exp_smoothing_forecast_data = ExpSmoothingForecast.objects.all()

    mid_exp = len(exp_smoothing_data) // 5

    # Подготовка данных для графика
    dates = [f"{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').year}-{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').month}" for data in exp_smoothing_data[4 * mid_exp:]]
    # dates = [data.date for data in exp_smoothing_data[4 * mid_exp:]]
    values = [data.value for data in exp_smoothing_data[4 * mid_exp:]]

    # mid_exp_forecast = len(exp_smoothing_forecast_data) // 4

    forecast_dates = [f"{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').year}-{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').month}" for data in exp_smoothing_forecast_data]
    # forecast_dates = [data.date for data in exp_smoothing_forecast_data]
    forecast_values = [data.value for data in exp_smoothing_forecast_data]

    # # Настройка меток оси x с интервалом в 2 года
    # step = 2  # Интервал в годах
    # labels = [dates[i] for i in range(len(dates)) if i % (365 * step) == 0]
    # print(dates)
    # print(range(len(dates)))
    metrics_obj = ExpSmoothingMetrics.objects.first()
    mae = round(metrics_obj.mae, 2)
    now = datetime.now()

    context = {
        'vert_line_x': f'{now.year}-{now.month}',
        'dates': dates + forecast_dates,
        'values': values + forecast_values,
        'mae': mae,
    }
    return render(request, 'data_app/index.html', context)
