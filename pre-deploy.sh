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
    if [ "${DEPLOY}" == "true" ]; then
        echo "Deploy to Github releases is Enabled."
        if git show-ref --tags --quiet --verify -- "refs/tags/${BUILD_TAG}"; then
            echo "Tag already present. Deleting it."
            git tag -d "${BUILD_TAG}"
        fi
        echo "Creating Tag : ${BUILD_TAG}"
        git tag "${BUILD_TAG}"
        echo "Copying Release Logs"
        mkdir -p ./metadata/release-logs
        cp LOS_APK_Extractor.logs ./metadata/release-logs/LOS_APK_Extractor-"${BUILD_TAG}".log
        echo "Copying Release Notes"
        mkdir -p ./metadata/release-notes
        cp Release_Notes.md ./metadata/release-notes/Release-Notes-"${BUILD_TAG}".md
    else
        echo "Copying Build Logs"
        if [ "${LOGFILE_TS}" == "" ]; then
            LOGFILE_TS="$(date +%s)"
        fi
        mkdir -p ./metadata/logs
        cp LOS_APK_Extractor.logs ./metadata/logs/LOS_APK_Extractor-"${BUILD_TAG}"-"${LOGFILE_TS}".log
        echo "This Build will not be released."
    fi
else
    echo "BUILD_TAG and DEPLOY were not exported properly."
    exit 1
fi





# Install gems
#gem install octokit
#gem install optparse
