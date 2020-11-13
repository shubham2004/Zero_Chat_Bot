# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a credit card fraud detection program 
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from minisom import MiniSom


data = pd.read_csv('Credit_Card_Applications.csv')


X= data.iloc[:, :-1].values
y =data.iloc[:, -1].values

sc =MinMaxScaler(feature_range=(0,1))
X= sc.fit_transform(X)

som = MiniSom(x= 10, y=10, input_len=15, sigma=1.0, learning_rate=0.5)
som.random_weights_init(X)
som.train_random(data=X, num_iteration =100)


from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()
mappings = som.win_map(X)
frauds = np.concatenate((mappings[(6,4)], mappings[(5,3)]), axis = 0)
frauds = sc.inverse_transform(frauds)

print('Fraud Customer IDs')
for i in frauds[:, 0]:
  print(int(i))

