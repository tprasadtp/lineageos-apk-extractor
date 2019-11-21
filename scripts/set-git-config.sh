#!/usr/bin/env bash
set -e
echo "Setting git conf user.email"
git config --global user.email "${GH_EMAIL}" && echo "Done"
echo "Setting git conf user.name"
git config --global user.name "valarie-ci-bot" && echo "Done"
