from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import functions as f
from colorama import Fore, Back, Style

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

california = fetch_california_housing()

#список объектов локальной области
print(Fore.GREEN, 'Объекты', Style.RESET_ALL)
print(dir(california))

print(california.DESCR) # описание

print(california.feature_names)

#Создание и вывод таблицы
print(Fore.GREEN, 'Таблица', Style.RESET_ALL)
data = pd.DataFrame(data=california.data, columns=california.feature_names)
data['PRICE'] = california.target

print(data.head())

# проверка на нули
print(Fore.GREEN, 'Проверка на нули', Style.RESET_ALL)
print(pd.isnull(data).any) 

# 12
f.gisto2('AveRooms', 'AveRooms')

# 14-15
print(Fore.GREEN, 'Статистические характеристики', Style.RESET_ALL)
print(data.describe())
print(Fore.GREEN, 'Коэффиценты корреляции', Style.RESET_ALL)
print(data.corr())

# 16-17
mask = np.zeros_like(data.corr())
triangle_i = np.triu_indices_from(mask)
mask[triangle_i] = True

plt.figure()
sns.heatmap(data.corr(), mask=mask, annot=True, annot_kws={'size':14})
sns.set_style('white')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

# 18 полигон распределения зависимых переменных
rm_tgt_corr=round(data['AveRooms'].corr(data['PRICE']), 3)
plt.figure(figsize=(9,6))
plt.scatter(x=data['AveRooms'], y=data['PRICE'], alpha=0.6, s=80, color='blue')
plt.title(f'AveRooms and PRICE (Correlation {rm_tgt_corr})', fontsize=14)
plt.xlabel('AveRooms')
plt.ylabel('PRICE')
plt.show()

#19 гистограмма зависимости количества комнат и цены
plt.figure()
plt.hist(data['PRICE'], bins=50)
plt.xlabel('Price')
plt.ylabel('amount of rooms')
plt.show()

# 20
prices = data['PRICE']
features = data.drop('PRICE', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features,
                                                    prices, test_size=0.2, random_state=10)

# 21
print(Fore.GREEN, 'Тренируем модель и расчитаем коэфициенты детерменации для тренировочной и тестовой выборки', Style.RESET_ALL)
regr = LinearRegression()
regr.fit(X_train, y_train)

print('Training data', regr.score(X_train, y_train))
print('Test data r-squared: ', regr.score(X_test, y_test))

print('Intercepr', regr.intercept_)
pd.DataFrame(data=regr.coef_, index=X_train.columns, columns=['coef'])

# 22 повышаем точность
print(Fore.GREEN, 'Повышаем точность', Style.RESET_ALL)
data['PRICE'].skew()
print(data['PRICE'].min)

# 23
y_log = np.log(data['PRICE'])
y_log.tail()

# 27
print(y_log.skew())

# 28
sns.displot(y_log)
plt.show()

# 29
prices = np.log(data['PRICE'])
feautures = data.drop('PRICE', axis=1)
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    prices, test_size=0.2, random_state=10)
regr = LinearRegression()
regr.fit(X_train, y_train)

# 30
print(Fore.GREEN, 'Определяем статистически важные данные', Style.RESET_ALL)
X_incl_const = sm.add_constant(X_train)
regr = LinearRegression()
regr.fit(X_train, y_train)

print('Training data', regr.score(X_train, y_train))
print('Test data r-squared: ', regr.score(X_test, y_test))

print('Intercepr', regr.intercept_, '\n')
print(pd.DataFrame(data=regr.coef_, index=X_train.columns, columns=['coef']))
print()

#32
variance_inflation_factor(exog=X_incl_const.values, exog_idx=1)

# 33
vif = [variance_inflation_factor(exog=X_incl_const.values, exog_idx=i)
       for i in range(X_incl_const.shape[1])]
print(pd.DataFrame({'coef name': X_incl_const.columns, 'vif':np.around(vif,2)}))

# 34
print(Fore.GREEN, 'Оцениваем качество выборки по Байесу', Style.RESET_ALL)
X_incl_const = sm.add_constant(X_train)
model = sm.OLS(y_train, X_incl_const)
results = model.fit()
original_coef = pd.DataFrame({'coef:':results.params, 'p-value':round(results.pvalues,3)})
print('BIC', results.bic)
print('r-squared', results.rsquared, '\n')

# 35 
#X_incl_const = sm.add_constant(X_train)
#X_incl_const = X_incl_const.drop(['INDUS', 'AGE'], axis=1)
#model = sm.OLS(y_train, X_incl_const)
#results = model.fit()
reduced_coef = pd.DataFrame({'coef:':results.params, 'p-value':round(results.pvalues,3)})
#print('BIC', results.bic)
#print('r-squared', results.rsquared)

# 36
frames = [original_coef, reduced_coef]
print(pd.concat(frames, axis=1))

#visualization 37
prices = np.log(data['PRICE'])
feautures = data.drop('PRICE', axis=1)
X_train, X_test, y_train, y_test = train_test_split(features,
                                                    prices, test_size=0.2, random_state=10)
regr = LinearRegression()
regr.fit(X_train, y_train)
X_incl_const = sm.add_constant(X_train)
model = sm.OLS(y_train, X_incl_const)
results = model.fit()
plt.scatter(x=results.fittedvalues, y=results.resid, alpha=1)
plt.xlabel('Log prices')
plt.ylabel('Residuals')
plt.title('Residuals in prices')
plt.show()
