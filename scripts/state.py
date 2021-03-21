#!/usr/bin/env python3

import sys
from os import path
from stabbrev import StateAbbrev

class State:
    def __init__(self, st, hdr, data):
        for name, value in zip(hdr, data):
            setattr(self, name, value)
        self.stabbrev = st.abbrev(self.state)

class States:
    def __init__(self):
        data = path.join(path.split(sys.argv[0])[0], '../data/geo/state.txt')
        data = [x.strip().split(',') for x in open(data).readlines()]
        # strip header
        hdr = data[0]
        data = data[1:]
        st = StateAbbrev()
        data = [State(st, hdr, x) for x in data]
        self.abbrev = {}
        self.state = {}
        for state in data:
            self.abbrev[state.stabbrev] = state
            self.state[state.state] = state
        
    def by_abbrev(self, abbrev):
        '''
        Look up state data by case-insensitive abbreviation. Returns
        a State object, or None if the abbreviation is invalid.
        '''
        abbrev = abbrev.upper()
        if not abbrev in self.abbrev:
            return None
        return self.abbrev[abbrev]


if __name__ == '__main__':
    st = States()
    print(st.by_abbrev('fl').areakm)
