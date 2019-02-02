#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e

echo "DEPLOY is set to ${DEPLOY}"
echo "BUILD_TAG is set to ${BUILD_TAG}"
echo "LOS_REL_VERSION is ${LOS_REL_VERSION}"
LOG_FILE_PREFIX="Log"

if [ "${BUILD_TAG}" == "" ] || [ "${DEPLOY}" == "" ]; then
    echo "BUILD_TAG and DEPLOY were not exported properly."
    exit 1
else
    if [ "${DEPLOY}" == "true" ]; then
        echo "Tagging Release...."
        echo "Setting Up Git Email & User"
        git config --local user.name "valarie-ci-bot"
        git config --local user.email "${GH_EMAIL}"

        echo "Deploy to Github releases is Enabled."
        if git show-ref --tags --quiet --verify -- "refs/tags/${BUILD_TAG}"; then
            echo "Tag already present."
        else
            echo "Creating Tag : ${BUILD_TAG}"
            git tag "${BUILD_TAG}"
        fi
        echo "Copying Release Logs"
        mkdir -p ./metadata/release-logs
        cp LOS_APK_Extractor.logs ./metadata/release-logs/"${LOG_FILE_PREFIX}"-B-"${TRAVIS_BUILD_NUMBER}"-"${BUILD_TAG}".log
        echo "Copying Release Notes"
        mkdir -p ./metadata/release-notes
        cp Release-Notes.md ./metadata/release-notes/Release-Notes-"${BUILD_TAG}".md

        # Tree to gh-pages
        # only on Deploy
        tree /mnt/lineage/ > ./metadata/info/tree-${LOS_REL_VERSION}.txt
    else
        # We cond deploy to github releases
        echo "Copying Build Logs"
        if [ "${LOGFILE_TS}" == "" ]; then
            LOGFILE_TS="$(date +%s)"
        fi
        mkdir -p ./metadata/logs
        cp LOS_APK_Extractor.logs ./metadata/logs/"${LOG_FILE_PREFIX}"-B-"${TRAVIS_BUILD_NUMBER}"-"${BUILD_TAG}"-"${LOGFILE_TS}".log
        echo "This Build will not be released."
    fi
    echo "RSYNC'ING to gh-deploy"
    rsync -Eav ./gh-pages/ ./gh-deploy/
    rsync -Eav ./metadata/ ./gh-deploy/
fi
