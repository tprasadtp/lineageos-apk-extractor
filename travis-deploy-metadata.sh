#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e
METADATA_BRANCH= "metadata"
# Checkout the branch
git clone --branch=${METADATA_BRANCH}    https://${GH_TOKEN}@github.com/$TRAVIS_REPO_SLUG gh-deploy 2>&1 > /dev/null
cd gh-deploy || false
# Update pages
rsync -Ea /metadata/ .
# Commit and push latest version
git add -A .
git config user.name  "Valarie-CI-Bot"
git config user.email "${GH_EMAIL}"
git commit -m "CI-Updated for build ${BUILD_TAG} - with TS - ${LOGFILE_TS}"
git push -fq origin ${METADATA_BRANCH} 2>&1 > /dev/null
popd