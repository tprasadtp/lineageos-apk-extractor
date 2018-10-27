#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e
echo "Cloning Brotli Repo"
git clone https://github.com/google/brotli
cd brotli
./configure-cmake --disable-debug
make
sudo make install