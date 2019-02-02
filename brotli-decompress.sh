#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e

if [[ ${LOS_DEVICE_CODENAME} == "bullhead" ]]; then
  brotli --decompress --force --verbose --output=system.new.dat system.new.dat.br
elif [[ ${LOS_DEVICE_CODENAME} == "hammerhead" ]];then
  echo "No need to decompress..."
else
  echo "Device name not configured assuming latest format.."
  brotli --decompress --force --verbose --output=system.new.dat system.new.dat.br
fi
