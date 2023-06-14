# Generated by Django 4.1.5 on 2023-06-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0006_expsmoothingmetrics_remove_expsmoothingparams_mae_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GRUForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GRUMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mae', models.FloatField(default=0, verbose_name='MAE')),
            ],
        ),
        migrations.CreateModel(
            name='GRUParams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookback', models.PositiveIntegerField(verbose_name='Кол-во интервалов в прошлом')),
                ('delay', models.PositiveIntegerField(verbose_name='Кол-во интервалов в будущем')),
                ('step', models.PositiveIntegerField(verbose_name='Шаг')),
                ('batch_size', models.PositiveIntegerField(verbose_name='Размер пакета')),
                ('hidden_neurons', models.PositiveIntegerField(verbose_name='Кол-во скрытых нейронов в слое')),
                ('dropout', models.FloatField(verbose_name='Прореживание')),
                ('recurrent_dropout', models.FloatField(verbose_name='Рекуррентное Прореживание')),
                ('steps_per_epoch', models.PositiveIntegerField(verbose_name='Кол-во шагов в эпохе')),
                ('epochs', models.PositiveIntegerField(verbose_name='Кол-во эпох')),
            ],
        ),
    ]