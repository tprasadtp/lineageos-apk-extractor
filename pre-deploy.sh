#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e

echo "DEPLOY is set to ${DEPLOY}"
echo "BUILD_TAG is set to ${BUILD_TAG}"

echo "Tagging Release...."

echo "Setting Up Git Email & User"
git config --local user.name "valarie-ci-bot"
git config --local user.email "${GH_EMAIL}"

if [ "${BUILD_TAG}" != "" ] || [ "${DEPLOY}" != "" ]; then
    git tag "${BUILD_TAG}"
else
    echo "BUILD_TAG and DEPLOY are not exported properly."
    exit 1
fi

echo "Copying Logs"
mkdir -p ./metadata/logs
cp LineageOS_APK_Extractor.logs ./metadata/logs/LineageOS_APK_Extractor-"${BUILD_TAG}".log

echo "Copying Release Notes"
mkdir -p ./metadata/release-notes
cp Release_Notes.md ./metadata/release-notes/Release-Notes-"${BUILD_TAG}".md

# Install gems
#gem install octokit
#gem install optparse
