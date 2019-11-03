#!/usr/bin/env bash
#  Copyright (c) 2018-2019. Prasad Tengse
#
#

function display_usage()
{
#Prints out help menu
cat <<EOF
Setup script for this project

Usage: source $(basename $0)  [options]

[-h --help]             [Display this help message]

This script by default activates and exits.
Its is *your* responsibility to create a virtual env and install
required packages.

EOF
}

function setup {
  echo -e "$((++count)). \e[36mChecking run config\e[39m"
  if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    echo -e "   \e[92mRun config checks passed\e[39m"
  else
    echo -e "   \e[91mYou should source this script instead of running it!\e[39m"
    unset count
    exit 1
  fi
  echo -e "$((++count)). \e[36mActivating venv\e[39m"
  if [[ -d .venv ]]; then
    source .venv/bin/activate
     echo -e "$((++count)). \e[36mAdding current directory to PYTHONPATH\e[39m"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
  else
    echo -e "   \e[91mFailed to find virtual env .venv. Please create one and run \e[39m"
    echo -e "   \e[92msource venv/bin/activate && pip install -r requirements.txt \e[39m"
  fi
}

function main {
  count=0
  # No args just run the setup function
  echo -e "\e[91mThis script is now deprecated use direnv instead.\e[39m"
  echo -e "\e[92mYou can follow the instructions here https://direnv.net/ \e[39m"
  echo -e "\e[92mThis script however will be kept here for compatibility reasons. \e[39m"
  echo ""

  if [[ $# -eq 0 ]]; then
    setup
  fi;

  while [[ ${1} != "" ]]; do
    case ${1} in
      -h | --help )          display_usage;;
      * )                    echo -e "\e[91mInvalid argument(s). See usage below. \e[39m";display_usage;;
    esac
    shift
  done
  unset count

}

main "$@"
