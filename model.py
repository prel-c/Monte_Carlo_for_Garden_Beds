import random
from tqdm import tqdm
import pandas as pd
import math
from utils import create_data, poliv

columns = ['Rainfall', 'Evaporation'] #тут надо указать названия столбцов
periods = [(str(i)+'-'+'12', str(i+1)+'-'+'02') for i in range(2008, 2009, 1)] #периоды из датасета
data = create_data(col=columns, per=periods)
print("данные извлечены и собраны в data")

simulate = 100
probability = 0.999 #достоверность симуляций
threshold = math.ceil(((1 - probability) * simulate))

k_list = [i/10 for i in range(0, 21, 1)] #коэффициент запаса
N_list = [i for i in range(0, 10000, 1000)] #насос (л/день)
G_list = [5000] #водовоз (л)
R_start_list = [i for i in range(0, 50000, 2000)] #размер нашей цистерны

result = [['-' for N in range(len(N_list))] for _ in range(len(k_list))]

total_cases = len(k_list) * len(N_list) * len(G_list) * len(R_start_list)
print(f'Запускаем {simulate} симуляций с {total_cases} вариантами параметров')

with tqdm(total=total_cases, desc="Варианты параметров", unit="case") as outer:
    for k in range(len(k_list)):
        for N in range(len(N_list)):
            for G in range(len(G_list)):
                for R_start in range(len(R_start_list)):
                    Day_off_count = 0
                    Day_car_count = 0

                    for t in range(simulate):
                        random.shuffle(data['Rainfall'])

                        Day_off, Day_car, Day_full = poliv(N_list[N], G_list[G], R_start_list[R_start], k_list[k], data)

                        #print('вероятность нехватки воды:', Day_off, len(data), Day_off / len(data))
                        if Day_off / len(data) > 0.001:
                            Day_off_count += 1
                            #print('услвие на полив не выполнено')

                        #print('вероятность вызова машины:', Day_car, len(data), Day_car / len(data))
                        if Day_car > 0:
                            Day_car_count += 1
                            #print('услвие на машину не выполнено')
                        
                        if Day_car_count >= threshold or Day_off_count >= threshold:
                            break

                    if Day_car_count < threshold and Day_off_count < threshold:
                        result[k][N] = R_start_list[R_start]
                        break

                    #print('вероятность вызвать машину хоть раз', Day_car_count / simulate)
                    #print('вероятность не полить больше 0.1% от всех дней', Day_off_count / simulate)

                    outer.update(1)

#Таблица общаяя
df = pd.DataFrame(result, index=k_list, columns=N_list)
df.to_csv('result.csv', index=True, index_label = 'k\\N')

#Таблица - min R и k при заданном N
result_N = [[], []]

for col in df.columns:
    minR = '-'
    minK = '-'
    for row in df.index:
        val = df[col][row]
        if val != '-' and (minR == '-' or val < minR):
            minR = val
            minK = row
    result_N[0].append(minR)
    result_N[1].append(minK)

df_N = pd.DataFrame(result_N, index=['R_min', 'k'], columns=N_list)
df_N.to_csv('result_N.csv', index=True, index_label = 'N')

#Таблица - min N и k при заданном R
dict_R = {}
result_R = [[], [], []]
for col in df.columns:
    for row in df.index:
        val = df[col][row]
        if val != '-' and (val not in dict_R or col < dict_R[val][0]):
            dict_R[val] = (col, row)

for i in dict_R.keys():
    result_R[0].append(i)
    result_R[1].append(dict_R[i][0])
    result_R[2].append(dict_R[i][1])

df_N = pd.DataFrame(result_R[1:], index=['N_min', 'k_min'], columns=result_R[0])
df_N.to_csv('result_R.csv', index=True, index_label = 'R')
