#!/usr/bin/env python3

import sys
from os import path
from xml.dom import minidom
import stabbrev
import json

data = path.join(path.split(sys.argv[0])[0], '../data/geo/gadm36_USA_1.kml')
doc = minidom.parse(data)
doc = doc.getElementsByTagName('Document')[0]

states = {}
sa = stabbrev.StateAbbrev()

for pm in doc.getElementsByTagName('Placemark'):
    ed = pm.getElementsByTagName('ExtendedData')[0]
    state = None
    for sd in ed.getElementsByTagName('SimpleData'):
        if sd.getAttribute('name') == 'NAME_1':
            state = sd.firstChild.data
    
    state = sa.abbrev(state)
    if state == None:
        continue

    print(state)
    mg = pm.getElementsByTagName('MultiGeometry')[0]

    polygons = []
    for pg in mg.getElementsByTagName('Polygon'):
        ob = pg.getElementsByTagName('outerBoundaryIs')[0]
        lr = pg.getElementsByTagName('LinearRing')[0]
        co = pg.getElementsByTagName('coordinates')[0]
        coords = co.firstChild.data.split(' ')
        coords = [x.split(',') for x in coords]
        coords = [[float(x) for x in y] for y in coords]
        polygons.append(coords)
    states[state] = polygons 

open('stategeom.js', 'w').write('let stategeom=' + json.dumps(states))



    
