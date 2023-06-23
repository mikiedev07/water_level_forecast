from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import ExpSmoothing, ExpSmoothingForecast, ExpSmoothingMetrics, GRUForecast, GRUMetrics


@login_required
def graph_view(request):
    exp_smoothing_data = ExpSmoothing.objects.all()
    exp_smoothing_forecast_data = ExpSmoothingForecast.objects.all()
    gru_forecast_data = GRUForecast.objects.all()

    mid_exp = len(exp_smoothing_data) // 5

    # Подготовка данных для графика
    dates = [f"{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').year}-{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').month}" for data in exp_smoothing_data[4 * mid_exp:]]
    values = [data.value for data in exp_smoothing_data[4 * mid_exp:]]

    exp_forecast_dates = [f"{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').year}-{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').month}" for data in exp_smoothing_forecast_data]
    exp_forecast_values = [data.value for data in exp_smoothing_forecast_data]

    gru_forecast_dates = [
        f"{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').year}-{datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S').month}"
        for data in gru_forecast_data]
    gru_forecast_values = [data.value for data in gru_forecast_data]

    metrics_obj = ExpSmoothingMetrics.objects.first()
    mae = round(metrics_obj.mae, 2)
    now = datetime.now()

    context = {
        'vert_line_x': f'{now.year}-{now.month}',
        'exp_dates': dates + exp_forecast_dates,
        'exp_values': values + exp_forecast_values,
        'gru_dates': dates + gru_forecast_dates,
        'gru_values': values + gru_forecast_values,
        'mae': mae,
    }
    return render(request, 'data_app/index.html', context)
