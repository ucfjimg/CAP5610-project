#!/usr/bin/env python3

import sys
from os import path

class StateAbbrev:
    def __init__(self):
        data = path.join(path.split(sys.argv[0])[0], '../data/geo/stabbrev.txt')
        pairs = [x.strip().split(',') for x in open(data).readlines()]
        self.to_abbrev = dict(pairs)
        self.to_state = dict([(x,y) for y,x in pairs])

    def state(self, abbrev):
        '''
        Given a state abbreviation, return the state name. abbrev is case insensitive
        and the returned state will be in upper case. If abbrev is invalid, returns
        None
        '''
        abbrev = abbrev.upper()
        if not abbrev in self.to_state:
            return None
        return self.to_state[abbrev]

    def abbrev(self, state):
        '''
        Given a state name, return the abbreviation. state is case insensitive
        and the returned abbreviation will be in upper case. If state is invalid, returns
        None
        '''
        state = state.upper()
        if not state in self.to_abbrev:
            return None
        return self.to_abbrev[state]


if __name__ == '__main__':
    st = StateAbbrev()
    print(st.state('fl'))
    print(st.abbrev('washington'))
    print(st.state('xx'))


