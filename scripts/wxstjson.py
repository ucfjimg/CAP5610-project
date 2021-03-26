#!/usr/bin/env python3

import wxstation
import json

st = wxstation.Stations()
blob = [{'name': x.station, 'state': x.state, 'lat': float(x.lat), 'long': float(x.long)} for x in st.stations]

print('let wxstations='+json.dumps(blob))
