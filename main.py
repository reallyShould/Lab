import matplotlib.pyplot as pypl

import functions as f

variables = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6]

n = list(set(variables))
#
x = []
for i in n:
    x.append(variables.count(i))
#
norm = []
for i in n:
    norm.append(round(i / n[-1], 3))

#выборочное среднее 
vMid = 0
for a in range(len(n)):
    vMid += n[a] * x[a]
vMid /= len(variables)

#дисперсия
depression = 0
for i in range(len(n)):
    depression += x[i] * (n[i] - vMid)**2
depression /= len(variables) - 1

#стандартное отклонение
stand = 0
for i in range(len(n)):
    stand += (x[i] - vMid)**2
stand = (stand/len(variables))**0.5

print('Варианты       ', n)
print('Частота        ', x)
print('Нормализация   ', norm)
print('\nВыборочное среднее:    ', vMid)
print('Мода:                  ', n.index(x.index(f.maxOfList(x))+1)+1)
print('Медиана                ', f.mediana(variables))
print('Выборочная дисперсия:  ', depression)
print('Стандартное отклонение:', stand)
print('Коэффицент вариации:   ', depression / vMid)
print('Размах:                ', n[-1] - n[0])

pypl.bar(x=n, height=x, bottom=0)
pypl.show()
