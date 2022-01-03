#!/bin/bash
origin=https://raw.githubusercontent.com/one-data-model/playground/master
git clone https://github.com/one-data-model/playground.git
rm -fR playground/tm
mkdir -p output/tm
cd playground
for filename in sdfObject/*.sdf.json; do
    echo "Converting $filename ..."
    sdf-wot-converter --from-sdf "$filename" --to-tm "../output/tm/$(basename "$filename" .sdf.json).tm.json" --origin-url $origin/$filename
done
