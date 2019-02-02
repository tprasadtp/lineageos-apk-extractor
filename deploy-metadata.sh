#!/bin/bash
# Copyright 2019, Prasad Tengse
# This Project is Licensed under MIT License.
# If you have not received a copy of the license,
# you can find it at the link below.
# https://opensource.org/licenses/MIT
set -e

echo "Setting Up Git Email & User"
git config --local user.name "Valarie CI Bot"
git config --local user.email "${GH_EMAIL}"

echo "Copy Current build metadata to deploy folder"
rsync -Eav ./metadata/ ./gh-pages/

(
cd ./gh-pages || false
git checkout gh-pages
git add -A
git commit -s -m "B-${TRAVIS_BUILD_NUMBER} for L-${TRAVIS_TAG}"

echo "Pushing metadata"
git push origin --quiet https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG} > /dev/null 2>&1
)
