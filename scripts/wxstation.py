#!/usr/bin/env python3

import sys
from os import path

class Station:
    def __init__(self, line):
        self.station = line[0:11]
        self.lat = line[11:20]
        self.long = line[21:30]
        self.state = line[38:40]
        self.name = line[41:71].strip()
    
    def __str__(self):
        return '%s %s %s' % (self.station, self.state, self.name)

    def __repr__(self):
        return '%s %s %s' % (self.station, self.state, self.name)

class StationData:
    def __init__(self, stid, type):
        dataroot = path.join(path.split(sys.argv[0])[0], '../data/wx/obs')
        fn = '%s.FLs.52j.%s' % (stid, type)
        fname = path.join(dataroot, fn)
        lines = [x.strip()[12:] for x in open(fname).readlines()]    
        self.obs = {}
        for line in lines:
            year = int(line[0:4])
            self.obs[year] = [int(line[4+i:10+i]) for i in range(0, 12*9, 9)]

    def sample(self, year, month):
        '''
        For given year and month (0 = Jan, 11= Dec), return the observation
        in this data set or None if there is no observed data
        '''
        if not year in self.obs or month < 0 or month > 11:
            return None
        sample = self.obs[year][month]
        
        if sample == -9999:
            return None
        return sample

    def isample(self, year, month):
        '''
        For given year and month (0 = Jan, 11= Dec), return the observation
        in this data set. If there is no sample, attempt to interpolate the
        sample between the previous and following months. None can still
        be returned if there is no adjacent data to interpolate.
        '''
        s = self.sample(year, month)
        if s != None:
            return s

        if month > 0:
            prev = self.sample(year, month-1)
        else:
            prev = self.sample(year-1, 11)

        if month < 11:
            next = self.sample(year, month+1)
        else:
            next = self.sample(year+1, 0)

        if prev == None or next == None:
            return None

        return (prev + next) / 2

class Stations:
    def __init__(self):
        stations = path.join(path.split(sys.argv[0])[0], '../data/wx/ushcn-v2.5-stations.txt')
        self.stations = [Station(x.strip()) for x in open(stations).readlines()]

        self.states = list(set([st.state for st in self.stations]))
        self.states.sort()
        self.station_by_state = dict(zip(self.states, [[] for _ in self.states]))
        for st in self.stations:
            self.station_by_state[st.state].append(st)

