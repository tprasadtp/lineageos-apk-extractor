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

echo "Setting Up Git Email & User"
git config --global user.name "valarie-ci-bot"
git config --global user.email "${GH_EMAIL}"


if [ "${BUILD_TAG}" == "" ] || [ "${DEPLOY}" == "" ]; then
    echo "BUILD_TAG and DEPLOY were not exported properly."
    exit 1
else
    if [ "${DEPLOY}" == "true" ]; then
        echo "Tagging Release...."
        echo "Deploy to Github releases is Enabled."
        if git show-ref --tags --quiet --verify -- "refs/tags/${BUILD_TAG}"; then
            echo "Tag is already present"
        else
            echo "Creating Tag : ${BUILD_TAG}"
            #git tag "${BUILD_TAG}"
            export TRAVIS_TAG="${BUILD_TAG}"
        fi

        export GH_PAGES_COMMIT_MSG_PREFIX="release"

        echo "Copying Release Notes"
        mkdir -p ./metadata/release-notes
        cp ./build/Release-Notes.md ./metadata/release-notes/Release-Notes-"${BUILD_TAG}".md
    else
        export GH_PAGES_COMMIT_MSG_PREFIX="metadata"
        echo "This Build will not be released."
    fi
fi
