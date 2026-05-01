import pandas as pd
import numpy as np
import random

def create_data(file_name : str = "Weather_data.csv", col : list | str = None, per : list = None) -> dict:
    """
    Создаёт словарь с ключами из col,
    в периодs указанные в per (формат ГГГГ-ММ-ДД),
    пример: per = [('2008-02-02', '2008-02-22'), ('2008-06-20', '2008-07-14')]
    если период не указан, то используется [('2008-02-01', '2017-06-25')].
    нужно укзать массив из картежей вида ('ГГГГ-ММ-ДД', 'ГГГГ-ММ-ДД'),
    даты будут взяты по всем периодам включая конец и начало!
    если col не указанно, то берутся все столбцы,
    столбец Data будет взят в любом случае.
    Каждлый ключ - название строки,
    при обращений по ключу вовращает массив данных с 2/1/2008 по 6/25/2017
    """

    file_base = pd.read_csv(file_name, index_col=0, parse_dates=["Date"])
    
    #print(file.head(), file.loc["2008-02-01"])
    
    if col == None:
        col = file_base.columns

    if per == None:
        per = [('2008-02', '2008-06')]
        file = file_base
    else:
        slice_list = []
        for p in per:
            slice = file_base.loc[p[0] : p[1]]
            #print('slice=', slice)
            slice_list.append(slice)
        file = pd.concat(slice_list)
        #print('slise_llst0=', slice_list[0],'slise_llst1=' , slice_list[1])
        #print('file=', file.head(), file.loc["2008-02-04"])
    
    
    data_csv = {'Date':[]}

    for i in col:
        data_csv[str(i)] = []

    #print(data.keys())

    for date, line in file.iterrows():
        #3print("line:", line, 'date:', date)
        data_csv["Date"].append(date)
        for i in col:
            #print('i:', i)
            if i != "Date":
                data_csv[i].append(line[i])

    return data_csv

def f(q):
    p = np.random.rand()

    if p <= q:
        return 0
    return 1

def poliv(N, G, R_start, k, data, s = 500, q=0.05):

    Kc = random.randint(3, 12) / 10
    v = 0
    d = 0 #флаг вызова машины
    R = R_start
    day_off = 0 #счётчик сколько дней мы не смогли полить
    day_car = 0 #счётчик сколько дней мы вызывали машину
    day_full = 0 #счётчик сколько дней рещервуар был полный
    day = 0
    v_list = []

    for i in range(len(data['Date'])):

        v = s * (data['Evaporation'][i] * Kc - data['Rainfall'][i])
        if v < 0:
            v = 0
        v_list.append(v)
        

        R = R - v + f(q) * N + d * G
        if R < 0:
            R = 0
            day_off += 1
            #print('Не смогли сегодня полить доконца')

        if R > R_start:
            R = R_start
            day_full += 1
            #print('Резервуар заполнен')

        if v * k >= R:
            d = 1
            day_car += 1
            #print('Вызываем машину на завтра')
        else:
            d = 0

        #print(f'Day{day}, v={v}, R={R}')
        day += 1

    #print(f"не смогли полить {day_off} дней")
    #print(f"машину вызывали {day_car} дней")
    #rint(f"резервуар был заполнен {day_full} дней")

    #count += 1
    #print('прошло симуляций', count)
    #print('среднее потребление воды:', sum(v_list)//len(v_list))

    return day_off, day_car, day_full


if __name__ == '__main__':
    columns = ['Date', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation'] #тут надо указать названия столбцов которые хочешь получить
    periods = [(str(i)+'-'+'12', str(i+1)+'-'+'02') for i in range(2008, 2016, 1)] #периоды
    data = create_data(col=columns, per=periods) #это сами данные за все дни
    print("данные извлечены и собраны в data")

    k = 100 #количество дней, которые ты хочешь вывести и положить в days
    days = [] #это массив в котором будут хранится данные по первым k дням
    print(f'данные за первые {k} дней')
    for i in range(k): #пример того, как можно извлекать данные
        day = []
        for column in columns:
            day.append(data[column][i])
        days.append(day)
        print(f'день {i}:', day)
    
    #print(days, sep='\n')