#!/bin/bash
# Copyright 2018, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e
METADATA_BRANCH="gh-pages"
#GIT_DIR="${HOME}/pages"
# Checkout the branch
echo "saving PWD"
pushd $PWD
echo "Cloning ${METADATA_BRANCH} branch"
git clone --branch=${METADATA_BRANCH}    https://github.com/tprasadtp/lineageos-apk-extractor gh-deploy 2>&1 > /dev/null
#git clone --branch=${METADATA_BRANCH}    https://github.com/tprasadtp/lineageos-apk-extractor.git gh-deploy
# Update pages
rsync -Ea ./metadata/ ./gh-deploy/
cd gh-deploy || false
# Commit and push latest version
git add -A .
git config user.name  "Valarie-CI-Bot (TravisCI)"
git config user.email "${GH_EMAIL}"
git commit --allow-empty -am "CI-Updated for build ${BUILD_TAG} - with TS - ${LOGFILE_TS}"
git push -fq https://valarie-ci-bot:${GH_TOKEN}@github.com/tprasadtp/lineageos-apk-extractor ${METADATA_BRANCH} 2>&1 > /dev/null
popd