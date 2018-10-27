#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e
./los_extractor.py
brotli --decompress --force --verbose --ouput=system.new.dat system.new.dat.br
./sdat2img.py system.transfer.list system.new.dat system.img
sudo mount -t ext4 system.img /mnt/lineage
./copy_files.py
chmod +x ./flags.sh && source ./flags.sh