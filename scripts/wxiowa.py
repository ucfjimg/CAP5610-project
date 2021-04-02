#!/usr/bin/env python3
import pandas as pd
import numpy as np
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
data.sort_values(by='DATE', inplace=True)

# rescaler to mm
data['PRCP'] = data['PRCP'] * 0.1

# rescale to Celsius 
data['TMIN'] = data['TMIN'] * 0.1
data['TMAX'] = data['TMAX'] * 0.1

# NB this is an approximation but only one station has TAVG, and less than 10%
# of the samples actually have it. 
#
# The correlation of this approximation to the samples that do exist is 0.999,
# and the means are almost identical
#
data['TAVG'] = (data['TMIN'] + data['TMAX']) * 0.5

# throw away really old data
index = data[data.DATE == '1941-01-01'].index[0]
data = data.loc[index:]

data.to_csv(path.join(dataroot, '..', 'wx-frontier-daily.csv'))

data['YEAR'] = data.DATE.str[0:4].astype(int)
data['MONTH'] = data.DATE.str[5:7].astype(int)
data['DAY'] = data.DATE.str[8:10].astype(int)
data['CALDAY'] = data.DATE.str[5:10]


baseline_years = range(1961, 1991)
all_years = range(1941, 2021)

#
# compute percentiles needed for later extreme weather features
#
baseline = data.loc[(data.YEAR >= 1961) & (data.YEAR < 1991)]
tmax90 = baseline[['TMAX', 'CALDAY']].groupby('CALDAY').agg(lambda lst: np.percentile(lst, 90))
tmin20 = baseline[['TMIN', 'CALDAY']].groupby('CALDAY').agg(lambda lst: np.percentile(lst, 20))

GSP = []
GDD = []
GSTmax = []
GSTmin = []
frost = []
summer = []
HWI = []
CWI = []

def is_season_day(m, d):
    '''
    Returns True if the given date is both in `year` and is in the
    defined (May 10-Oct 20) growing season.
    '''
    return ((m == 5) & (d >= 10)) | ((m >= 6) & (m <= 9)) | ((m == 10) & (d <= 20))


for year in all_years:
    season = data.loc[(data.YEAR == year) & (is_season_day(data.MONTH, data.DAY))]  
    precip = season.PRCP.mean()
    # GSP: Precipitation averaged over the growing season
    GSP.append(precip)
    # GDD: Daily GDD is the mean temperature minus a reference. Growing season GDD
    # is the sum of all daily GDD's. The given reference is 10 degrees C
    gdd = (season.TAVG - 10).sum()
    GDD.append(gdd)

    # mean min and max over the season
    GSTmax.append(season.TMAX.mean())
    GSTmin.append(season.TMIN.mean())

    # Frost days - count of days with tmin < 0
    frost.append((season.TMIN < 0).sum())

    # Summer days - count of days with tmax > 25
    summer.append((season.TMAX > 25).sum())

    tmax = season.merge(tmax90, on='CALDAY')
    tmax = tmax.TMAX_x > tmax.TMAX_y
    HWI.append(sum(tmax))

    tmin = season.merge(tmin20, on='CALDAY')
    tmin = tmin.TMIN_x < tmin.TMIN_y
    CWI.append(sum(tmin))

years = pd.Series(all_years, name='YEAR')
GSP = pd.Series(GSP, name='GSP')
GDD = pd.Series(GDD, name='GDD')
GSTmax = pd.Series(GSTmax, name='GSTmax')
GSTmin = pd.Series(GSTmin, name='GSTmin')
frost = pd.Series(frost, name='frost')
summer = pd.Series(summer, name='summer')
HWI = pd.Series(HWI, name='HWI')
CWI = pd.Series(CWI, name='CWI')

data = pd.DataFrame([years, GSP, GDD, GSTmin, GSTmax, frost, summer, HWI, CWI]).T
data['YEAR'] = data.YEAR.astype(int)
print(data)

data.to_csv(path.join(dataroot, '..', 'wx-frontier-agg.csv'))
