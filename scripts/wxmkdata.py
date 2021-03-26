#!/usr/bin/env python3

import sys
from state import States
from os import path
import wxstation

stns = wxstation.Stations()
dsets = ['prcp', 'tmin', 'tmax', 'tavg']
ystart = 1960
yend = 2021

# big empty data structure to hold multi-dimensional data
data = {}
for ds in dsets:
    data[ds] = {}
    for st in stns.states:
        data[ds][st] = {}
        for year in range(ystart, yend+1):
            data[ds][st][year] = 12 * [(0,0)]

# add in observations from relevant stations
for st in stns.states:
    for stn in stns.station_by_state[st]:
        for dset in dsets: 
            stdata = wxstation.StationData(stn.station, dset)
            for year in range(ystart, yend+1):
                for month in range(0, 12):
                    s = stdata.isample(year, month)
                    if s != None:
                        old = data[dset][st][year][month]
                        data[dset][st][year][month] = (old[0] + s, old[1] + 1)

# get mean of data across all stations
for ds in dsets:
    # if temperature, divide by 100 to get degrees C, else
    # divide by 10 to get millimeters precipitation
    scale = 0.01
    if ds == 'prcp':
        scale = 0.1
    for st in stns.states:
        for year in range(ystart, yend+1):
            data[ds][st][year] = [x/y*scale if y != 0 else None for x,y in data[ds][st][year]]

# print it out in a CSV format 
print('type,state,year,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec')
for ds in dsets:
    for st in stns.states:
        for year in range(ystart, yend+1):
            prefix = [ds, st, str(year)]
            samples = ['%.2f' % x if x != None else '' for x in data[ds][st][year]]
            print(','.join(prefix + samples))
