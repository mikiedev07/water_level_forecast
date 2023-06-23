import numpy as np
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
import pandas as pd

from data_app.models import GRUForecast, GRUMetrics, GRUParams

"""
data — исходный массив вещественных чисел, нормализованных кодом в листинге 6.32;

lookback — количество интервалов в прошлом от заданного момента, за которое 
отбираются входные данные;

delay — количество интервалов в будущем от заданного момента, за которое 
отбираются целевые данные;

min_index и max_index — индексы в массиве data, ограничивающие область для 
извлечения данных; это помогает оставить в неприкосновенности сегменты 
проверочных и контрольных данных;

shuffle — флаг, определяющий порядок извлечения образцов: с перемешиванием или в хронологическом порядке;

batch_size — количество образцов в пакете;

step — период в интервалах, из которого извлекается один образец; мы установим его равным 6, чтобы получить по одному 
образцу за каждый час
"""


def generator(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=1):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
        samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][0]
        yield samples, targets


def populate_db_models(model, dataframe):
    if model.objects.count() > 0:
        model.objects.all().delete()
    for index, row in dataframe.iterrows():
        model.objects.create(date=index, value=row['MEAN'])


def run():
    f = open('data_app/data_samples/merged.csv')
    data = f.read()
    f.close()

    lines = data.split('\n')
    header = lines[0].split(',')
    lines = lines[1:-1]

    # выделяем все параметры в массив numpy
    float_data = np.zeros((len(lines), len(header) - 1))
    for i, line in enumerate(lines):
        values = [float(x) for x in line.split(',')[1:]]
        float_data[i, :] = values

    float_data = np.nan_to_num(float_data)

    train_min = 30000
    train_max = len(float_data) - 2920
    val_min = 65000
    val_max = 80000

    # среднее и стандартное отклонения по обучающей выборке
    mean = float_data[train_min:train_max].mean(axis=0)
    float_data -= mean
    std = float_data[train_min:train_max].std(axis=0)
    float_data /= std

    params = GRUParams.objects.first()

    lookback = params.lookback
    step = params.step
    delay = params.delay
    batch_size = params.batch_size
    train_gen = generator(float_data,
                          lookback=lookback,
                          delay=delay,
                          min_index=train_min,
                          max_index=train_max,
                          shuffle=True,
                          step=step,
                          batch_size=batch_size)
    val_gen = generator(float_data,
                        lookback=lookback,
                        delay=delay,
                        min_index=val_min,
                        max_index=val_max,
                        step=step,
                        batch_size=batch_size)

    val_steps = (val_max - val_min - lookback) // batch_size
    test_steps = (len(float_data) - val_max + 1 - lookback) // batch_size

    # model structure
    model = Sequential()
    model.add(layers.GRU(params.hidden_neurons, dropout=params.dropout, recurrent_dropout=params.recurrent_dropout, input_shape=(lookback // step, float_data.shape[-1])))
    # model.add(layers.Flatten(input_shape=(lookback // step, float_data.shape[-1])))
    # model.add(layers.Dense(1, activation='relu'))
    # model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1))

    # compiling
    model.compile(optimizer=RMSprop(), loss='mae')

    history = model.fit_generator(train_gen,
                                  steps_per_epoch=params.steps_per_epoch,
                                  epochs=params.epochs,
                                  validation_data=val_gen,
                                  validation_steps=val_steps)

    print(list(history.history.keys()))
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    if GRUMetrics.objects.count() > 0:
        GRUMetrics.objects.all().delete()
    GRUMetrics.objects.create(mae=round(min(val_loss), 2))
    print(loss, val_loss)

    # plt.figure()
    #
    # plt.plot(epochs, loss, 'bo', label='Training loss')
    # plt.plot(epochs, val_loss, 'b', label='Validation loss')
    # plt.legend()

    # Forecast range + reshape
    k = -2919
    result_shape = np.empty((0, 5840, 16))

    while k < -1:
        if k % 400 == 0:
            print('k =', k)
        test_shape = float_data[-5840 + k:k]
        new_shape = np.reshape(test_shape, (1, 5840, 16))
        result_shape = np.concatenate((result_shape, new_shape), axis=0)
        k += 1

    # FORECAST
    pred = model.predict(result_shape)
    r1 = pred * 1.2 + mean[0] + 2

    # SET DATA INDEX
    numeric_data = np.array(r1)
    start_date = '2023-06-22 00:00:00'  # Начальная дата
    date_range = pd.date_range(start=start_date, periods=len(numeric_data), freq='3H')

    # Создание DataFrame с датами и числовыми данными
    df = pd.DataFrame(data=numeric_data, index=date_range, columns=['MEAN'])

    upsampled = df.resample("10D").mean()
    interpolated = upsampled.interpolate('linear')

    populate_db_models(GRUForecast, interpolated)


if __name__ == '__main__':
    run()
