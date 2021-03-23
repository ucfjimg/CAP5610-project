#!/bin/bash

state_names=(California Illinois Indiana Iowa Kansas Michigan Minnesota Missouri Nebraska NorthDakota Ohio SouthDakota Wisconsin)

echo "Running..."
for state in ${state_names[*]}
do
    python3 $1 $state
done

echo "Completed!"