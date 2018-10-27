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

# Settings
DEVICE_NAME = "bullhead"
RELEASE_NOTES = "Release_Notes.md"
RELEASE_JSON = "release.json"
OLD_RELEASE_JSON = "old_release.json"
REL_TAG_BASE_URL = "https://github.com/tprasadtp/lineageos-apk-extractor/releases/tag/"
# Files
LOS_DL_PAGE = "LineageOS_Downlad_Page.html"
LOG_FILE = "LineageOS_APK_Extractor.logs"
LOS_ZIP_FILE = "LineageOS.zip"
LOS_SHA256_FILE = "LineageOS_ZIP_SHA256.txt"
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
# Logs
log = logging.getLogger()
log.setLevel(logging.DEBUG)
# Create Rotating file handler
log_file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3 )
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
    dl(file_name=LOS_DL_PAGE, file_url="https://download.lineageos.org/"+device_name)
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
        REL_TAG= LOS_REL_VERSION[0] + '.' +LOS_REL_DATE[0]
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


def generate_release_notes():
    """
    Release Notes Generator.
    Use Extracted info to generate Release notes.
    """
    if os.path.isfile(RELEASE_NOTES):
        log.info('%s exists.', RELEASE_NOTES)
        try:
            log.info('Deleting old release notes')
            os.remove(RELEASE_NOTES)
        except OSError as e:
            log.critical('Failed to remove existing release notes.')
            log.error('Error was %s', e.strerror)
            sys.exit()
    log.info('Generating Release Notes...')
    with open(RELEASE_NOTES, 'w+') as release_notes:
            release_notes.write('# Release notes for Tag lineage -' + REL_TAG + '\n\n')
            ts = time.strftime('%I:%M %p %Z on %b %d, %Y')
            release_notes.write('- Release notes generated on : ' + ts + '\n')
            release_notes.write('- Lineage OS Version : ' + LOS_REL_VERSION[0] + '\n')
            release_notes.write('- Lineage OS Type : ' + LOS_REL_TYPE[0] + '\n', )
            release_notes.write('- Zip file used : [ZIPfile]('+ LOS_REL_URL[0] + ')' + '\n')
            release_notes.write('- Lineage OS build date : ' + LOS_REL_DATE[0] + '\n')
            release_notes.write('- CI Node name : '+ platform.node() + '\n')
            release_notes.write('- Release Link : ' + REL_TAG_BASE_URL + REL_TAG + '\n\n\n')
            release_notes.write('## Tags and Downloads\n\n')
            release_notes.write('- This is generated automatically.\n'
                                + '- Tags correspond to build date.\n'
                                + '- Every release is tagged '
                                + '[lineage-version].[build-date]\n\n')
            release_notes.write('## Logs\n' +
                                'Logs related to this Build are available'
                                + 'as assets or available in logs folder in `metadata` branch.\n')
    log.debug("Generated Release Notes")

def set_flags_and_metadata():
    """
    Set conditional flags and generate release tags & variable exporter scripts.
    Also generate metadata json
    """
    log.info('Downloading OLD release.json')
    dl(file_name=OLD_RELEASE_JSON, file_url="https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/metadata/release.json")
    log.info('Preparing Metadata....')
    METADATA.update({ 'version' : 2,
                      'ci': {
                            'build_date' : int(time.time()),
                            'build_ts'  : time.strftime('%I:%M %p %Z on %b %d, %Y'),
                            'node_name' : platform.node()
                            },
                      'lineage': {
                            'build' : LOS_REL_DATE[0],
                            'build_type' : LOS_REL_TYPE[0],
                            'zip_file': LOS_REL_URL[0]
                            },
                      'release' : {
                            'tag' : REL_TAG,
                            'link': REL_TAG_BASE_URL + REL_TAG
                            }
                      })

    log.info("Checking last build date...")
    if os.path.isfile(OLD_RELEASE_JSON):
        with open(OLD_RELEASE_JSON, 'r') as oldjson:
            last_metadata = json.loads(oldjson.read())
        last_build_date = last_metadata['ci']['build_date']
        log.info('Last Build was %s', last_build_date)
        last_build_tag = last_metadata['release']['tag']
        log.info('Last Release Tag was %s',last_build_tag)
        # If build timestamp for old build is less than current timestamp and
        # if tags are different, set ci.deployed to true. Also set DEPLOY=true
        # in flags script. Also generate Release Notes.
        #---------------------------------------------------------------------
        # Otherwise, set ci.deployed to flase, and DEPLOY=false.
        # Do not generate release notes as it will not be used.
        if int(time.time()) > last_build_date  and REL_TAG != last_build_tag:
            log.info("This release is New. GH Releases will be enabled if on MASTER")
            METADATA.update({
                             'ci': {
                                   'deployed' : "true"
                                    }
                            })
            try:
                with open(FLAGS_SCRIPT, 'w+') as flag_file:
                    log.info('Generating Exporter Scripts...')
                    flag_file.write('#!/usr/bin/env bash\nexport DEPLOY="true"\nexport BUILD_TAG="' + REL_TAG + '"\n')
            except Exception:
                log.critical('Failed to write exporter script.')
                sys.exit(1)

            ##################################################################
            # Generate Release Notes
            ##################################################################
            generate_release_notes()
            ##################################################################
        else:
            log.info("Release is already the latest.")
            METADATA.update({
                             'ci': {
                                   'deployed' : "false"
                                    }
                            })
            try:
                with open(FLAGS_SCRIPT, 'w+') as flag_file:
                    flag_file.write('#!/usr/bin/env bash\nexport DEPLOY="false"\nexport BUILD_TAG="' + REL_TAG + '"\n')
            except Exception:
                log.critical('Failed to write exporter script.')
                sys.exit(1)
        # Write METADATA to json
        log.info("Generating %s", RELEASE_JSON)
        if Path.exists(RELEASE_JSON):
            log.info('%s exists.', RELEASE_JSON)
            try:
                log.info('Deleting old %s file...', RELEASE_JSON)
                shutil.rmtree(RELEASE_JSON)
            except OSError as e:
                log.critical('Failed to remove existing %s.', RELEASE_JSON)
                log.error('Error was %s', e.strerror)
                sys.exit(1)
        try:
            with open(RELEASE_JSON, 'w+') as release_json:
                release_json.write(json.dumps(METADATA, indent=4))
                log.debug('JSON Dump is : %s', json.dumps(METADATA))
        except Exception:
            log.critical("Failed to write %s.", RELEASE_JSON)
            sys.exit(1)
    else:
        log.critical('File %s which holds Metadata from previous build cannot be found. This will also result in %s not being generated.', OLD_RELEASE_JSON, RELEASE_JSON)
        sys.exit(2)
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
    dl(LOS_SHA256_FILE, LOS_REL_URL[0]+"?sha256")

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

    # Extract
    extract_zip_contents(zip_file=LOS_ZIP_FILE, destination=os.getcwd())

    # Release Notes & Metadata
    set_flags_and_metadata()


if __name__ == '__main__':
    try:
        main()
    finally:
        log.removeHandler(log_file_handler)
        log.removeHandler(log_console_handler)