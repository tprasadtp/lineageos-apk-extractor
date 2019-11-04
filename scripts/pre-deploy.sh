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
            git tag "${BUILD_TAG}"
            export TRAVIS_TAG="${BUILD_TAG}"
            git push --tags --quiet https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG} > /dev/null 2>&1
        fi

    else
        echo "This Build will not be released."
    fi
fi
