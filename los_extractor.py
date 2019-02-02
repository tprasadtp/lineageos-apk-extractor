#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

# Imports
import os
import shutil
import hashlib
import time
import sys
import platform
import zipfile
import json
import datetime
from pathlib import Path
import logging, logging.handlers

# Version Checks.
if int(str(sys.version_info.major) + str(sys.version_info.minor)) < 34:
    sys.exit("Needs Python 3.5+")
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Failed to import bs4")

from utils import get_file as dl
from utils import write_json

# Settings
DEVICE_NAME = os.environ.get('LOS_DEVICE_CODENAME', "bullhead")

RELEASE_NOTES = "Release-Notes.md"
RELEASE_JSON = f'release-{DEVICE_NAME}.json'
OLD_RELEASE_JSON = "old_release.json"
REL_TAG_BASE_URL = "https://github.com/tprasadtp/lineageos-apk-extractor/releases/tag/"
# Files
LOS_DL_PAGE = f'LineageOS_Downlad_Page_{DEVICE_NAME}.html'
LOG_FILE = "LOS_APK_Extractor.logs"
LOS_ZIP_FILE = f'LineageOS_{DEVICE_NAME}.zip'
LOS_SHA256_FILE = f'LineageOS_{DEVICE_NAME}_ZIP_SHA256.txt'
FLAGS_SCRIPT = "flags.sh"

# Use chunk size of 128K
FILE_HASH_BUFFER = 131072

# Arrays for LOS ZIP Data & Dict for Metadata
LOS_REL_TYPE = []
LOS_REL_VERSION = []
LOS_REL_URL = []
LOS_REL_SIZE = []
LOS_REL_DATE = []

METADATA = {}
# Defaults to false
GH_RELEASE_FLAG = False
# TS
UTC_TS = int(time.time())

if os.environ.get('FORCE_GH_RELEASE', False).lower() == "true":
    FORCE_GH_RELEASE = True
else:
    FORCE_GH_RELEASE = False

# Logs
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# Create Rotating file handler
log_file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=3 )
# Set file Log handler to Lower Log level
log_file_handler.setLevel(logging.DEBUG)
# Create console handler with a higher log level
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.INFO)
# Formatters
log_file_handler.setFormatter(logging.Formatter('[ %(asctime)s ] - [%(levelname)-8s] - %(name)s - %(message)s'))
log_console_handler.setFormatter(logging.Formatter('[ %(levelname)-8s] - %(message)s'))
# Add the handlers to the logger
log.addHandler(log_file_handler)
log.addHandler(log_console_handler)

def log_sysinfo():
    """
    Logs Basic system info
    """
    log.debug('------------------------System Info------------------------------')
    log.debug('Platform : %s, Version: %s', platform.system(), platform.version())
    log.debug('Hostname : %s', platform.node())
    log.debug('Python Version : %s', platform.python_version())
    log.debug('Platform Arch : %s', platform.architecture())
    log.debug('-----------------------------------------------------------------')


def extract_checksum_from_file(file_name):
    """
    Extract Checksum from the File.
    Returns Checksum in HeX
    """
    if os.path.isfile(file_name):
        log.debug("File's %s present on FS.", file_name)
        with open(file_name, 'r') as checksum_file:
            return checksum_file.readline().split(" ",1)[0]
    else:
        log.error("File's %s not found.", file_name)
        sys.exit(1)

def verify_sha256_checksum(file_name, checksum):
    """
    Verify checksum of a file.
    Filename        : File to Verify
    checksum        : SHA256SUM
    Returns Boolean : True if matches, False if fails.
    """
    if os.path.isfile(file_name):
        log.debug("File %s is present on the FS.", file_name)
        sha256hash = hashlib.sha256()
        with open(file_name, 'rb') as f:
            while True:
                data = f.read(FILE_HASH_BUFFER)
                if not data:
                    break
                sha256hash.update(data)
        log.debug('SHA256 hash for %s is : %s', file_name, sha256hash.hexdigest() )
        log.debug('SHA256 hash SHOULD BE : %s', checksum.lower())
    else:
        log.critical('OOOPS! File not found.')
        sys.exit('ZIP File not Found.')
    if checksum.lower() == sha256hash.hexdigest():
        log.debug('File Hashes Match.')
        return True
    else:
        log.debug('File hashes do not match.')
        return False


def extract_los_urls(device_name="marlin"):
    """
    Scrap Zip file URLs and data from lineage os download page.
    """
    log.debug('Getting Download Page for %s', device_name)
    dl(file_name=LOS_DL_PAGE, file_url=f'https://download.lineageos.org/{device_name}')
    if os.path.isfile(LOS_DL_PAGE):
        log.debug('%s file exists.', LOS_DL_PAGE)
        with open(LOS_DL_PAGE, encoding="utf-8") as los_dl_page:
            log.info('Parsing HTML page...')
            soup = BeautifulSoup(los_dl_page.read(), features="lxml")
            table = soup.find('table')
            for tr in table.find_all('tr'):
                td = tr.find_all('td')
                if len(td) == 5: # Making sure not to grab header
                    LOS_REL_TYPE.append(td[0].string)
                    LOS_REL_VERSION.append(td[1].string)
                    LOS_REL_URL.append((td[2].a).get('href'))
                    LOS_REL_SIZE.append(td[3].string)
                    LOS_REL_DATE.append(td[4].string)
        global REL_TAG
        REL_TAG = f'{LOS_REL_VERSION[0]}.{LOS_REL_DATE[0]}'
        # Debugging stuff
        log.debug('----------------------------------------------------------')
        log.debug('------------------Parsed Variables------------------------')
        log.debug('LOS_REL_TYPE = %s', LOS_REL_TYPE)
        log.debug('LOS_REL_VERSION = %s', LOS_REL_VERSION)
        log.debug('LOS_REL_URL = %s', LOS_REL_URL)
        log.debug('LOS_REL_SIZE = %s', LOS_REL_SIZE)
        log.debug('LOS_REL_DATE = %s', LOS_REL_DATE)
        log.debug('REL_TAG is %s', REL_TAG)
        log.debug('----------------------------------------------------------')
        log.debug('----------------------------------------------------------')
    else:
        log.error('File %s not found.', LOS_DL_PAGE)
        sys.exit(1)


def extract_zip_contents(zip_file, destination):
    """
    Extract contents of Zip file
    Arg:
        zip_file : path to Zipfile,
        destination:  directory to extract to
    """
    if os.path.isfile(LOS_ZIP_FILE):
        with zipfile.ZipFile(zip_file,"r") as zip_ref:
          zip_ref.extractall(destination)
    else:
        log.error('%s not found.', zip_file)
        sys.exit('ZIP is not the filesystem.')

def purge(dir, pattern):
    """
    Delete files in specified dir by pattern
    Args:
        dir : directory to scan
        pattern : regex to match
    """
    for p in Path(dir).glob(pattern):
        p.unlink()


def delete_old_files():
    log.info('Deleting old files if any....')
    shutil.rmtree('META-INF/', ignore_errors=True)
    shutil.rmtree('system/', ignore_errors=True)
    shutil.rmtree('install/', ignore_errors=True)
    log.debug('Deleting old DAT files (if any)')
    purge(dir=os.getcwd(), pattern="system.*.*")
    log.debug('Deleting old IMG file (if any)')
    purge(dir=os.getcwd(), pattern="*.img")
    purge(dir=os.getcwd(), pattern="*.bin")


def generate_release_notes(time_stamp):
    """
    Release Notes Generator.
    Use Extracted info to generate Release notes.
    Args:
        time_stamp - (str) Timestamp in human readable form.
    Returns :
        None
    """
    log.info('Generating Release Notes...')
    with open(RELEASE_NOTES, 'w+') as release_notes:
            release_notes.write('# Release notes for Tag lineage -' + REL_TAG + '\n\n')
            release_notes.write('- Release notes generated on : ' + str(time_stamp) + '\n')
            release_notes.write('- Device name : ' + DEVICE_NAME + '\n')
            release_notes.write('- Lineage OS Version : ' + LOS_REL_VERSION[0] + '\n')
            release_notes.write('- Lineage OS Type : ' + LOS_REL_TYPE[0] + '\n', )
            release_notes.write('- Zip file used : [ZIPfile]('+ LOS_REL_URL[0] + ')' + '\n')
            release_notes.write('- Lineage OS build date : ' + LOS_REL_DATE[0] + '\n')
            release_notes.write('- CI Node name : '+ platform.node() + '\n')
            release_notes.write('- Release Link : ' + REL_TAG_BASE_URL + REL_TAG + '\n\n\n')
            release_notes.write('## Tags and Downloads\n\n')
            release_notes.write('- This file is generated automatically.\n'
                                + '- Tags correspond to build date.\n'
                                + '- Every release is tagged as'
                                + '[lineage-version].[los-build-date]\n\n')
            release_notes.write('## Logs\n' +
                                'Logs related to this build are available'
                                + 'as assets or available in logs folder under `gh-pages` branch.\n')
    log.debug("Generated Release Notes.")

def set_metadata_and_get_release_flag(current_ts, last_build_ts, last_build_tag, last_release_date, last_release_bnum):
    """
    Define common Metadata like build time etc.
    Args:
        current_ts      - (int) current unix epoch
        last_build_date - (int) unix epoch during last build
        last_relase_ts  - (str) date and time of last release on github releases.
        last_build_tag  - (str) last build tag
        last_release_ci_bnum - (int) build number for last release
    Returns:
        bool - GH_RELEASE_FLAG
        Modifies global Dictionary METADATA.
    """

    # Convert to Human Readable TS
    ts_human = time.strftime('%d %b at %H:%M',  time.gmtime(UTC_TS))
    METADATA.update({ 'version' : 5,
                      'ci': {
                            'build_date' : current_ts,
                            'build_date_human'  :  ts_human,
                            'build_number' : os.environ.get('TRAVIS_BUILD_NUMBER', "NA"),
                            'node_name' : platform.node()
                            },
                      'lineage': {
                            'version' : LOS_REL_VERSION[0],
                            'build' : LOS_REL_DATE[0],
                            'build_type' : LOS_REL_TYPE[0],
                            'zip_file': LOS_REL_URL[0],
                            'device': DEVICE_NAME
                            }
                      })
    # If build timestamp for old build is less than current timestamp and
    # if tags are different, set ci.deployed to Yes. Also set DEPLOY=true
    # in flags script. Also generate Release Notes.
    #---------------------------------------------------------------------
    # Otherwise, set ci.deployed to No, and DEPLOY=false.
    # Do not generate release notes as it will not be used.
    # A global env var FORCE_GH_RELEASE is checked, if set to true, GH releases will
    # be forced.

    if (str(REL_TAG) != str(last_build_tag)) or FORCE_GH_RELEASE:
        log.info("GH Releases will be enabled if on MASTER")
        log.info("Last tag was %s", last_build_tag)
        METADATA['ci'].update({ 'deployed' : "Yes"})
        METADATA.update({ 'release' : {
                                'tag' : REL_TAG,
                                'human_ts' : ts_human,
                                'link': REL_TAG_BASE_URL + REL_TAG,
                                'ci_bnum': TRAVIS_BUILD_NUMBER
                                }
                        })
        # Generate Release Notes
        generate_release_notes(time_stamp = ts_human)
        return True
    else:
        log.info("Release is already latest. No need to deploy.")
        log.info("Last tag was %s", last_build_tag)
        METADATA['ci'].update({ 'deployed' : "No"})
        # Keep old release date as is.
        METADATA.update({ 'release' : {
                                'tag' : last_build_tag,
                                'human_ts' : last_release_date,
                                'link': REL_TAG_BASE_URL + last_build_tag,
                                'ci_bnum': last_release_bnum
                                }
                        })
        return False

def get_old_jason_data():
    """
    Download and parse old release json
    Args: None
    Returns : A tuple (int last_build_ts, str last_build_tag, str last_release_date, last_release_ci_bnum)
    """
    log.debug('Downloading OLD release.json')
    dl(file_name=OLD_RELEASE_JSON, file_url=f'https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/{RELEASE_JSON}')
    log.debug("Reading old release.json file...")
    if os.path.isfile(OLD_RELEASE_JSON):
        with open(OLD_RELEASE_JSON, 'r') as oldjson:
            last_metadata = json.loads(oldjson.read())
            try:
                # Get Last build TS unix epoch
                last_build_date = last_metadata['ci']['build_date']
                log.info('Last Build was %s', last_build_date)
                # Get Last Release Tag
                last_build_tag = last_metadata['release']['tag']
                log.info('Last Release Tag was %s', last_build_tag)
                # Also Get last Release Date
                last_release_ts = last_metadata['release']['human_ts']
                log.info('Last Release TS was %s', last_release_ts)

                last_release_ci_bnum = last_metadata['release']['ci_bnum']
                log.info('Last Release Build was %s', last_release_ci_bnum)
                # Return tuple
                return ( int(last_build_date), str(last_build_tag), str(last_release_ts), int(last_release_ci_bnum))
            except KeyError as e:
                log.critical('JSON file from repository seems to be old. update it manually to latest schema.')
                log.exception(e)
                sys.exit(10)
    else:
        log.error("Old release.json cannot be found.")
        sys.exit(1)


def write_export_script(release_flag=str(GH_RELEASE_FLAG).lower(), release_tag="NA", time_stamp=time.time()):
    """
    Writes flags.sh to disk.
    """
    log.debug('Writing %s', FLAGS_SCRIPT)
    try:
        with open(FLAGS_SCRIPT, 'w+') as flag_file:
            flag_file.write('#!/usr/bin/env bash\n'
                            + 'export DEPLOY="' + str(release_flag) +'"\n'
                            + 'export BUILD_TAG="' + str(release_tag) + '"\n'
                            + 'export LOGFILE_TS="' + str(time_stamp) + '"\n'
                            + 'export LOS_REL_VERSION="' + str(LOS_REL_VERSION[0]) + '"\n')
    except Exception as e:
        log.critical('Failed to write exporter script.')
        log.exception(e)
        sys.exit(1)


def main():

    log_sysinfo()

    # Extract URLs
    log.info('Getting LOS Download page for %s ...', DEVICE_NAME)
    extract_los_urls(device_name=DEVICE_NAME)

    # Download Zip
    log.info('Downloading ZIP File ...')
    dl(LOS_ZIP_FILE, LOS_REL_URL[0])

    # Download Checksum
    log.info('Getting Checksum File...')
    dl(LOS_SHA256_FILE, f'{LOS_REL_URL[0]}?sha256')

    # Verify Checksums
    log.info('Verifying ZIP file checksums...')
    if verify_sha256_checksum(LOS_ZIP_FILE, extract_checksum_from_file(LOS_SHA256_FILE)):
        log.info("Woohooo.. ZIP File's Checksum matches.")
    else:
        log.error("Oh dear! ZIP File is corrupt. Please try again.")
        sys.exit(1)

    # Extract Files
    log.info('Extracting from ZIP File ....')
    # Delete Files from Last Run
    delete_old_files()
    # Extract files
    extract_zip_contents(zip_file=LOS_ZIP_FILE, destination=os.getcwd())

    # Release Notes & Metadata
    log.info("Getting Info about last build & release...")
    last_build_ts, last_build_tag, last_relase_date, last_release_ci_bnum = get_old_jason_data()

    log.info('Preparing Metadata....')
    GH_RELEASE_FLAG = set_metadata_and_get_release_flag(current_ts=UTC_TS,
                                                        last_build_ts=last_build_ts,
                                                        last_build_tag=last_build_tag,
                                                        last_release_date=last_relase_date,
                                                        last_release_bnum=last_release_ci_bnum )

    log.info("Generating %s", RELEASE_JSON)
    write_json(dict=METADATA, file_name=RELEASE_JSON)

    log.info('Writing exporter script...')
    write_export_script(release_flag=str(GH_RELEASE_FLAG).lower(), release_tag=REL_TAG, time_stamp=UTC_TS)


if __name__ == '__main__':
    try:
        main()
    finally:
        log.removeHandler(log_file_handler)
        log.removeHandler(log_console_handler)
