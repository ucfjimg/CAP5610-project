#!/usr/bin/env python3

import csv
import sys
from os import path

class Station:
    def __init__(self, hdr, data):
        for name, value in zip(hdr, data):
            setattr(self, name, value)
        self.lat = float(self.lat)
        self.long = float(self.long)
    
    def __str__(self):
        return '%s %s %s %s %s' % (self.station, self.state, self.county, self.zipcode, self.name)

    def __repr__(self):
        return self.__str__()

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
        stations = path.join(path.split(sys.argv[0])[0], '../data/wx/wxextstat.csv')
        f = open(stations, encoding='utf-8')
        reader = csv.reader(f)
        header = next(reader)
        self.stations = [Station(header, x) for x in reader]

        self.states = list(set([st.state for st in self.stations]))
        self.states.sort()
        self.station_by_state = dict(zip(self.states, [[] for _ in self.states]))
        for st in self.stations:
            self.station_by_state[st.state].append(st)

