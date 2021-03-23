#!/bin/bash

state_names=(California Illinois Indiana Iowa Kansas Michigan Minnesota Missouri Nebraska NorthDakota Ohio SouthDakota Wisconsin)

echo "Running..."
for state in ${state_names[*]}
do
    python3 agriculture_summary.py $state
done

echo "Completed!"