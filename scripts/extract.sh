#!/usr/bin/env bash
#  Copyright (c) 2018-2019. Prasad Tengse
#
#
set -eo pipefail
set -e
if [[ ${1} == "bullhead" ]]; then
    echo "Using Brotli and sdat2img"
    brotli --decompress --force --verbose --output=build/system.new.dat build/system.new.dat.br
    python ./vendor/sdat2img.py
else
    echo "Using AB scheme"
    python3 vendor/extract-payload-bin.py build/payload.bin build/
fi
