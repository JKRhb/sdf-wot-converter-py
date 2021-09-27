#!/bin/bash
git clone https://github.com/one-data-model/playground.git
rm -fR playground/tm
mkdir -p output/tm
for filename in playground/sdfObject/*.sdf.json; do
    echo "Converting $filename ..."
    sdf-wot-converter --from-sdf "$filename" --to-tm "output/tm/$(basename "$filename" .sdf.json).tm.jsonld"
done
