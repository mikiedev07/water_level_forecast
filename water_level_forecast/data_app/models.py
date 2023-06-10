from django.db import models


class ExpSmoothing(models.Model):
    date = models.CharField(max_length=20)
    value = models.FloatField()


class ExpSmoothingForecast(models.Model):
    date = models.CharField(max_length=20)
    value = models.FloatField()


class ExpSmoothingParams(models.Model):
    interp_frequency = models.CharField(max_length=5, verbose_name="Дискрета для интерполяции")
    seasonal_periods = models.PositiveIntegerField(verbose_name="Сезонность ряда")
    forecast_horizon = models.PositiveIntegerField(verbose_name="Горизонт прогноза")

    def __str__(self):
        return "Гиперпараметры модели"


class ExpSmoothingMetrics(models.Model):
    mae = models.FloatField(verbose_name="MAE", default=0)
    rmse = models.FloatField(verbose_name="RMSE", default=0)
    mape = models.FloatField(verbose_name="MAPE", default=0)
    smape = models.FloatField(verbose_name="SMAPE", default=0)

    def __str__(self):
        return "Метрики"
