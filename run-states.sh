#!/usr/bin/env bash

for f in states/*.{pvsm,py}; do
    echo
    echo "computing $f"
    paraview --state=$f
    echo
    echo "done $f"
done
