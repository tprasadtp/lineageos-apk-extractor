#!/usr/bin/env bash
#  Copyright (c) 2018-2019. Prasad Tengse
#
#
set -eo pipefail

if [[ ${1} == "bullhead" ]]; then
    echo "Using Brotli and sdat2img"
    brotli --decompress --force --verbose --output=build/system.new.dat build/system.new.dat.br
    python ./vendor/sdat2img.py
    echo "Prevent destroying other metadata(guacamole)"
    mkdir -p metadata
    wget https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json -O metadata/release-guacamole.json
else
    echo "Using AB scheme"
    python3 vendor/extract-payload-bin.py build/payload.bin build/
    echo "Prevent destroying other metadata(bullhead)"
    mkdir -p metadata
    wget https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json -O metadata/release-bullhead.json
fi
