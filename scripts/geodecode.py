#!/usr/bin/env python3

import csv
from sklearn.metrics.pairwise import haversine_distances
import math
from os import path
import stabbrev
import sys

class Location:
    def __init__(self, lat, lng, zipcode, state, abbrev, county):
        self.lat = lat
        self.lng = lng
        self.zipcode = zipcode
        self.state = state
        self.stabbrev = abbrev
        self.county = county

    def __str__(self):
        return '(%8.5f,%8.5f) Zip=%s State=%s(%s) County=%s' % (self.lat, self.lng, self.zipcode, self.state, self.stabbrev, self.county)

    def __repr__(self):
        return self.__str__()

class Geodecode:
    '''
    Find information about a location by lat/lng
    '''
    # The Earth's radius, in km
    _earth_radius = 6371

    # number of bins in accel struct
    _bins = 20

    def __init__(self):
        self.stabbrev = stabbrev.StateAbbrev()

        # geolocation data with more precise lat/long
        data = path.join(path.split(sys.argv[0])[0], '../data/geo/gaz2016zcta5centroid.csv')
        with open(data) as csvfile:
            reader = csv.reader(csvfile)
            rows = [x for x in reader]

        # strip header
        rows = rows[1:]
        self.locdata = [(float(lat), float(lng), zipcode) for lat, lng, zipcode in rows]

        # metadata
        data = path.join(path.split(sys.argv[0])[0], '../data/geo/uszips.csv')
        with open(data) as csvfile:
            reader = csv.reader(csvfile)
            rows = [x for x in reader]

        fields = ['zip', 'state_name', 'county_name']
        hdr = rows[0]
        fields = [hdr.index(x) for x in fields]
        rows = rows[1:]
        metadata = [[row[x] for x in fields] for row in rows]
        self.metadata = dict([(x[0], x[1:]) for x in metadata])

        self._bin_data()


    def _bin_data(self):
        '''
        This is a quick and dirty quad-tree like structure, except we're
        going to just divide space up into evenly divided bins rather than
        build the actual tree to account for varying density
        '''
        lats = [x for x, _, _ in self.locdata]
        lngs = [x for _, x, _ in self.locdata]

        self.minlat = min(lats)
        self.minlng = min(lngs)
        self.maxlat = max(lats)
        self.maxlng = max(lngs)
        self.dlat = (self.maxlat - self.minlat) / Geodecode._bins 
        self.dlng = (self.maxlng - self.minlng) / Geodecode._bins 

        self.locbins = [[[] for _ in range(0, Geodecode._bins)] for _ in range(0, Geodecode._bins)]
        
        for pt in self.locdata:
            lat, lng = self._coord_bins(pt[0], pt[1])
            self.locbins[lat][lng].append(pt)

    def _coord_bins(self, lat, lng):
        '''
        Return the bin the given lat, long falls into in the acceleration
        index
        '''
        lat = max(0, min(Geodecode._bins-1, int((lat - self.minlat) / self.dlat)))
        lng = max(0, min(Geodecode._bins-1, int((lng - self.minlng) / self.dlng)))
        return (lat, lng)

    def geodist(pt0, pt1):
        '''
        Return the approximate distance in kilometres between pt0 and pt1,
        where each point is a (latitude, longitude) pair.
        '''
        pt0 = [math.radians(x) for x in pt0]
        pt1 = [math.radians(x) for x in pt1]
        return haversine_distances([pt0, pt1])[1][0] * Geodecode._earth_radius

    def decode(self, pt):
        '''
        Approximate the zipcode at the given point pt, which is a 
        (latitude, longitude) pair, by finding the closest zip code 
        centroid.
        '''
        bestd = float(2 * math.pi * Geodecode._earth_radius)
        bestzc = None

        bin0, bin1 = self._coord_bins(pt[0], pt[1])

        for i in range(bin0-1, bin0+2):
            for j in range(bin1-1, bin1+2):
                if i < 0 or i >= Geodecode._bins or j < 0 or j >= Geodecode._bins:
                    continue
                for (lat, lng, zc) in self.locbins[i][j]:
                    d = Geodecode.geodist(pt, (lat, lng))
                    if d < bestd:
                        bestd = d
                        bestzc = zc
        
        county = ''
        state = ''
        if bestzc in self.metadata:
            state, county = self.metadata[bestzc]

        return Location(pt[0], pt[1], bestzc, state, self.stabbrev.abbrev(state), county)
    
    def counties(self):
        return list(set([(self.stabbrev.abbrev(st), county) for st, county in self.metadata.values()]))

    def zipcodes(self):
        return self.metadata.keys()


if __name__ == '__main__':
    ucf = [28.6031184, -81.1984448]
    g = Geodecode()

    print('UCF is : %s' % g.decode(ucf))
