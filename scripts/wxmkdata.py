#!/usr/bin/env python3

import codecs
import sys
from state import States
from os import path
import wxstation
import geodecode

gd = geodecode.Geodecode()

stns = wxstation.Stations()
dsets = ['prcp', 'tmin', 'tmax', 'tavg']
ystart = 1960
yend = 2021

STATE = 'state'
COUNTY = 'county'
ZIP = 'zip'

res = STATE
args = sys.argv[1:]
if len(args) > 0:
    what = args[0]
    if what == 'state':
        res = STATE
    elif what == 'county':
        res = COUNTY
    elif what == 'zip':
        res = ZIP
    else:
        print('Unknown resolution %s' % what)
        sys.exit(1)
        
    
# states of interest
soi = ['CA', 'IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']

    
space = []
if res == STATE:
    space = stns.states
elif res == COUNTY:
    space = gd.counties()
elif res == ZIP:
    space = gd.zipcodes() 
    
# big empty data structure to hold multi-dimensional data
data = {}
for ds in dsets:
    data[ds] = {}
    for st in space:
        data[ds][st] = {}
        for year in range(ystart, yend+1):
            data[ds][st][year] = 12 * [(0,0)]


# bucket stations based on the desired resolution in 'res'
stations = {}

for stn in stns.stations:
    if res == STATE:
        key = stn.state
    elif res == ZIP:
        key = stn.zipcode
    elif res == COUNTY:
        key = (stn.state, stn.county)

    if not key in stations:
        stations[key] = []
    stations[key].append(stn)

# add in observations from relevant stations
for key in stations.keys():
    for stn in stations[key]:
        for dset in dsets: 
            stdata = wxstation.StationData(stn.station, dset)
            for year in range(ystart, yend+1):
                for month in range(0, 12):
                    s = stdata.isample(year, month)
                    if s != None:
                        old = data[dset][key][year][month]
                        data[dset][key][year][month] = (old[0] + s, old[1] + 1)

# get mean of data across all stations
for ds in dsets:
    # if temperature, divide by 100 to get degrees C, else
    # divide by 10 to get millimeters precipitation
    scale = 0.01
    if ds == 'prcp':
        scale = 0.1
    for key in data[ds].keys():
        for year in range(ystart, yend+1):
            data[ds][key][year] = [x/y*scale if y != 0 else None for x,y in data[ds][key][year]]

# print it out in a CSV format 
sys.stdout = codecs.getwriter(encoding='utf-8')(sys.stdout.detach())
print('type,state,year,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec')
for ds in dsets:
    for key in data[ds].keys():
        for year in range(ystart, yend+1):
            k = key
            if res == COUNTY:
                k = '%s:%s' % key
            prefix = [ds, k, str(year)]
            samples = ['%.2f' % x if x != None else '' for x in data[ds][key][year]]
            print(','.join(prefix + samples))
