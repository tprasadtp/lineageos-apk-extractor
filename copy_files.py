#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

import os
import sys
import platform
import logging, logging.handlers
import shutil
import json
from pathlib import Path
try:
    from utils import get_file as dl
except ImportError as e:
    print(str(e))
    sys.exit(1)

MOUNT_POINT = "/mnt/lineage/"
RELEASE_DIR = Path('releases')
METADATA_DIR = Path('metadata')
LOG_FILE = "LOS_APK_Extractor.logs"
RELEASE_JSON = "release.json"
RELEASE_NOTES = "Release_Notes.md"

#if os.environ.get('TRAVIS') == "true" or os.environ.get('CI') == "true":
#    print("Running on TRAVIS or other CI.")
TRANSFER_JSON = "transfer.json"
#else:
#    TRANSFER_JSON = "test_transfer.json"

log = logging.getLogger()
log.setLevel(logging.DEBUG)
# Create Rotating file handler
log_file_handler = logging.FileHandler(LOG_FILE)
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

# Copy Files from Mount Point /system

def define_tag_from_json():
    """
    Read release.json to set TAG variable
    """
    log.debug("Setting TAG Variable")
    if os.path.isfile(RELEASE_JSON):
        try:
            log.info('Reading json data from file.')
            with open(RELEASE_JSON) as r:
                jsondata = json.loads(r.read())
                global TAG, GH_RELEASES_DEPLOY_FLAG
                TAG = jsondata['release']['tag']
                GH_RELEASES_DEPLOY_FLAG = jsondata['ci']['deployed']
                print(f'Git Flag: <{GH_RELEASES_DEPLOY_FLAG}>')
                if str(TAG) == "":
                    log.critical('TAG is empty!.')
                    sys.exit(10)
                if str(GH_RELEASES_DEPLOY_FLAG).lower() != "true" and str(GH_RELEASES_DEPLOY_FLAG).lower() != "false" :
                    log.critical('Invalid deploy flag. It can either be <true> or <false>')
                    sys.exit(10)
        except Exception as e:
            log.critical('Failed to read from %s', RELEASE_JSON)
            log.exception(e)
            sys.exit(1)
    else:
        log.critical('%s is not found on the FS', RELEASE_JSON)
        sys.exit(1)

def copy_release_files():
    """"
    Checks if moun point is available. If true,
    Copies APKS and other release assets to ./release folder
    """
    log.info("Checking Mount point")
    if os.path.ismount(MOUNT_POINT) or os.path.isdir(MOUNT_POINT):
        if Path(RELEASE_DIR).exists():
            log.debug('%s already present. deleting it..', RELEASE_DIR)
            try:
                shutil.rmtree(RELEASE_DIR)
            except Exception:
                log.critical("Failed to delete already existing %s", RELEASE_DIR)
                sys.exit(1)
        try:
            log.debug('Creating Releases Folder')
            os.makedirs(RELEASE_DIR)
        except Exception as e:
            log.critical("Failed to create %s directory.", RELEASE_DIR)
            log.exception(e)
            sys.exit(1)
        if os.path.isfile(TRANSFER_JSON):
            with open(TRANSFER_JSON) as t:
                transfer = json.loads(t.read())
            for app, path in transfer.items():
                fname = app + '-' + TAG + os.path.splitext(path)[1]
                try:
                    log.info("Copying %s from %s", app, path)
                    shutil.copy2(path, RELEASE_DIR / fname)
                except Exception as e:
                    log.error("Failed to Copy %s", app)
                    log.exception(e)
            # Copy Release Notes
            if str(GH_RELEASES_DEPLOY_FLAG).lower() == "true":
                log.info('Copying Release Notes...')
                try:
                    shutil.copy2(RELEASE_NOTES, RELEASE_DIR / RELEASE_NOTES)
                except Exception as e:
                    log.critical("Failed to copy Release Notes to upload folder.")
                    log.exception(e)
                    sys.exit(1)
            else:
                log.info("GH Releases is not enabled. Not Copying Release Notes.")
        else:
            log.critical("%s is not present. Cannot determine file list.", TRANSFER_JSON)
            sys.exit(1)

def copy_metadata_files():
    log.info("Copying Metadata")
    if Path(METADATA_DIR).exists():
        try:
            log.info("Deleting already existing folder..")
            shutil.rmtree(METADATA_DIR)
        except Exception as e:
            log.critical("Failed to delete %s", METADATA_DIR)
            log.exception(e)
            sys.exit(1)
    try:
        log.info("Creating Metadata Folder...")
        os.makedirs(METADATA_DIR)
    except Exception as e:
        log.critical("Failed to create metadata directory.")
        log.exception(e)
        sys.exit(1)
    try:
        log.info('Copying %s', RELEASE_JSON)
        shutil.copy2(RELEASE_JSON, METADATA_DIR / RELEASE_JSON)
    except Exception as e:
        log.critical("Failed to copy %s.", RELEASE_JSON)
        log.exception(e)
        sys.exit(1)

def main():
    """
    Main
    """
    define_tag_from_json()
    copy_metadata_files()
    copy_release_files()

if __name__ == '__main__':
    try:
        main()
    finally:
        log.removeHandler(log_file_handler)
        log.removeHandler(log_console_handler)