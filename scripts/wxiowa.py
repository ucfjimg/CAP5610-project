#!/usr/bin/env python3
import pandas as pd
from os import path
import sys

'''
Extract data from the three Iowa stations used by the Frontiers paper
'''

data = ['USC00135230.csv', 'USC00137572.csv', 'USW00014940.csv']
dataroot = path.join(path.split(sys.argv[0])[0], '../data/wx/ghcnd')
data = map(lambda x: path.join(dataroot, x), data)
data = list(map(pd.read_csv, data))

# all 3 frames have precipitation
fields = ['DATE', 'PRCP']

m0 = data[0][fields].merge(data[1][fields], on='DATE', how='outer')
m0['PRCP0'] = m0['PRCP_x']
m0['PRCP1'] = m0['PRCP_y']
m0 = m0.drop(columns=['PRCP_x', 'PRCP_y'])
m1 = m0.merge(data[2][fields], on='DATE', how='outer')
m1['PRCP'] = m1[['PRCP0', 'PRCP1', 'PRCP']].mean(axis=1)
prcp = m1.drop(columns=['PRCP0', 'PRCP1'])

# only two of them have temps
temps = list(filter(lambda x: 'TMIN' in x.columns, data))
temps = list(map(lambda x: x[['DATE', 'TMIN', 'TMAX']], temps))
m0 = temps[0].merge(temps[1], on='DATE', how='outer')
m0['TMIN'] = m0[['TMIN_x', 'TMIN_y']].mean(axis=1)
m0['TMAX'] = m0[['TMAX_x', 'TMAX_y']].mean(axis=1)
temp = m0.drop(columns=['TMIN_x', 'TMIN_y', 'TMAX_x', 'TMAX_y'])

data = prcp.merge(temp, on='DATE', how='outer')

# rescaler to mm
data['PRCP'] = data['PRCP'] * 0.1

# rescale to Celsius 
data['TMIN'] = data['TMIN'] * 0.1
data['TMAX'] = data['TMAX'] * 0.1

# throw away really old data
index = data[data.DATE == '1941-01-01'].index[0]
data = data.loc[index:]
data.to_csv(path.join(dataroot, '..', 'wx-frontier-daily.csv'))

