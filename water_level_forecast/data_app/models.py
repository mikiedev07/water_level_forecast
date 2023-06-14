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


class GRUForecast(models.Model):
    date = models.CharField(max_length=20)
    value = models.FloatField()


class GRUParams(models.Model):
    lookback = models.PositiveIntegerField(verbose_name='Кол-во интервалов в прошлом')
    delay = models.PositiveIntegerField(verbose_name='Кол-во интервалов в будущем')
    step = models.PositiveIntegerField(verbose_name='Шаг')
    batch_size = models.PositiveIntegerField(verbose_name='Размер пакета')
    hidden_neurons = models.PositiveIntegerField(verbose_name="Кол-во скрытых нейронов в слое")
    dropout = models.FloatField(verbose_name="Прореживание")
    recurrent_dropout = models.FloatField(verbose_name="Рекуррентное Прореживание")
    steps_per_epoch = models.PositiveIntegerField(verbose_name='Кол-во шагов в эпохе')
    epochs = models.PositiveIntegerField(verbose_name="Кол-во эпох")


class GRUMetrics(models.Model):
    mae = models.FloatField(verbose_name="MAE", default=0)

    def __str__(self):
        return "Метрики"
