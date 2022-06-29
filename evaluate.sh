# Install libyang
git clone https://github.com/CESNET/libyang.git
cd libyang
git checkout tags/v1.0.225
mkdir build; cd build
cmake ..
make
sudo make install
cd ../../

# Install nlohmann/json
git clone https://github.com/nlohmann/json.git
cd json
git checkout -b release/3.10.2
cmake -S . -B build
sudo cmake --build build --target install -j$(nproc)
cd ..

# Install nlohmann/json-schema-validator
git clone https://github.com/pboettch/json-schema-validator.git
cd json-schema-validator
mkdir build
cd build
cmake -DJSON_VALIDATOR_HUNTER=ON ..
make
sudo make install
cd ../../

# Install sdf-yang-converter
git clone https://github.com/jkiesewalter/sdf-yang-converter.git
cd sdf-yang-converter
mkdir build
cd build
cmake ..
make
cd ../../

# Clone yang Repository
git clone https://github.com/YangModels/yang.git

# Clone oneDM Repository
git clone https://github.com/one-data-model/playground.git
rm -fR playground/tm
mkdir -p output/tm
touch results.csv
wot_file_name=wot.td.json
yang_file_name=yang.yang
echo "Filename,SDF <-> WoT,SDF <-> YANG" >> results.csv
for filename in playground/sdfObject/sdfobject*.sdf.json; do
    echo "Converting $filename ..."
    wot_success=0
    yang_success=0

    rm -f $wot_file_name
    start="$(date -u +%s.%N)"
    sdf-wot-converter sdf-to-tm -i "$filename" -o $wot_file_name
    end="$(date -u +%s.%N)"
    wot_duration="$(bc <<<"$end-$start")"
    if [ -e "$wot_file_name" ]; then
        echo WoT conversion took $wot_duration seconds
    else
        echo WoT conversion failed
        wot_duration="Failed"
    fi

    cd sdf-yang-converter
    rm -f $yang_file_name
    start="$(date -u +%s.%N)"
    ./converter -f ../$filename -o $yang_file_name  -c ../yang
    end="$(date -u +%s.%N)"
    yang_duration="$(bc <<<"$end-$start")"
    if [ -e "$wot_file_name" ]; then
        echo YANG conversion took $yang_duration seconds
    else
        echo YANG conversion failed
        yang_duration="Failed"
    fi
    cd ..

    echo "$filename,$wot_duration,$yang_duration" >> results.csv
done
