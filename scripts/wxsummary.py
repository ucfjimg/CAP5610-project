#!/usr/bin/env python3

import sys
from os import path
from state import States
import statistics
import matplotlib.pyplot as plt
import numpy as np
from wxstation import Stations

# Plot distribution of stations by state
stdata = States()
stat = Stations()
stsumm = [(st, len(stat.station_by_state[st]), stdata.by_abbrev(st).areakm) for st in stat.station_by_state.keys()]
stpersqkm = np.array([x[1] / int(x[2]) for x in stsumm])
#plt.hist(stpersqkm)
#plt.title('Stations per square km')
#plt.show()

#
# Read observations from a station file. Ignores the metadata for now.
# returns a tuple
# [0] is the starting year
# [1] is a list of monthly observations
#
def readobs(fname):
    lines = [x.strip()[12:] for x in open(fname).readlines()]
    
    obs = []
    
    year0 = int(lines[0][0:4])
    prev = year0 - 1
    for line in lines:
        year = int(line[0:4])
        while prev < year - 1:
            obs.append(12 * [-9999])
            prev += 1
        prev = year
        for i in range(0, 12):
            start = 4 + 9 * i
            end = start + 6
            obs.append(int(line[start:end]))

    return (year0, obs)

#
# return a subrange of an observation, given an inclusive 
# range of years
#
def obsrange(obs, start, end):
    out = []
    if start < obs[0]:
        out += (obs[0] - start) * 12 * [-9999]
        start = obs[0]
    if start <= end:
        obsnyr = len(obs[1]) // 12
        last = min(obs[0] + obsnyr - 1, end)
        i0 = (start - obs[0]) * 12
        i1 = (last - obs[0]) * 12
        out += obs[1][i0:i1]
        start = last + 1
    if start <= end:
        out += (end - start + 1) * 12 * [-9999]
    
    return out

# figure out time coverage
dsets = ['prcp', 'tmin', 'tmax', 'tavg']
totobs = 0
missing = 0
for st in stat.stations:
    stid = st.station
    root = path.join(path.split(sys.argv[0])[0], '../data/wx/obs/' + stid + '.FLs.52j.')
    for ds in dsets:
        fname = root + ds
        obs = readobs(fname)
        obs = obsrange(obs, 1990, 2010)
        totobs += len(obs)
        missing += obs.count(-9999) # missing value flag

print('%.02f%% of values are missing' % (missing * 100 / totobs))






