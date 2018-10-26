#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

import os, sys, platform, logging, shutil, json
from pathlib import Path
try:
    from utils import get_file as dl
except ImportError:
    raise ImportError

MOUNT_POINT = "/mnt/lineage/"
RELEASE_DIR = Path('Releases')
METADATA_DIR = Path('Metadata')
LOG_FILE = "LineageOS_APK_Extractor.logs"
RELEASES_JSON = "release.json"
TRANSFER_JSON = "transfer.json"
FLAGS_SCRIPT = "flags.sh"

log = logging.getLogger()
log.setLevel(logging.DEBUG)
# Create Rotating file handler
log_file_handler = logging.FileHandler(LOG_FILE)
log_file_handler.setLevel(logging.DEBUG)
# Create console handler with a higher log level
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.INFO)
# Formatters
log_file_handler.setFormatter(logging.Formatter('[ {asctime} ] - %(name)s - [ {levelname:8s} ] - {message}', style='{'))
log_console_handler.setFormatter(logging.Formatter('[ {levelname:8s} ] - {message}', style='{'))
# Add the handlers to the logger
log.addHandler(log_file_handler)
log.addHandler(log_console_handler)
os.chdir(os.path.dirname(__file__))
# Copy Files from Mount Point /system

def copy_release_files():
    """"
    Checks if moun point is available. If true,
    Copies APKS and other release assets to ./release folder
    """
    log.info("Checking Mount point")
    if os.path.ismount(MOUNT_POINT) or os.path.isdir(MOUNT_POINT):
        try:
            log.debug('Creating Releases Folder')
            os.makedirs(RELEASE_DIR)
        except OSError:
            log.critical("Failed to create %s directory.", RELEASE_DIR)
            raise OSError
    if Path.exists(TRANSFER_JSON):
        with open(TRANSFER_JSON) as f:
            transfer = json.load(f)
        for app, path in transfer.item():
            dest = RELEASE_DIR+ '/' + app + '-' + TAG
            try:
                log.debug("Copying %s from %s", app, path)
                shutil.copy2(path, dest)
            except Exception:
                log.error("Failed to Copy %s", app)
    else:
        log.critical("%s is not preset. Cannot determine file list.", TRANSFER_JSON)
        SystemExit

def copy_metadata_files():
    log.info("Copying Metadata")
    if Path.exists(METADATA_DIR):
        try:
            log.info("Deleting already existing folder..")
            shutil.rmtree(METADATA_DIR)
        except Exception:
            log.critical("Failed to delete %s", METADATA_DIR)
            SystemExit
    else:
        try:
            log.info("creating Metadata Folder...")
            os.makedirs(METADATA_DIR)
        except Exception:
            log.critical("Failed to create metadata directory.")
            SystemExit
        log.info("Copying Metadata Files...")
        dest = METADATA_DIR + '/' + RELEASES_JSON
        try:
            shutil.copy2(RELEASES_JSON, dest)
        except:
            log.critical("Failed to copy %s.", RELEASES_JSON)
            SystemExit

def check_last_build():
    """
    Checks Last build from release.json in metadata branch
    Sets coco.json to set control data for releases...
    """
    log.info("Checking last build date...")
    if Path.exists('metadata.json') and Path.exists(RELEASES_JSON):
        with open('metadata.json') as f:
            last_metadata = json.loads((f.read))
        with open(RELEASES_JSON) as r:
            current_metadata = json.loads(r.read())
    else:
        last_build_date = last_metadata['ci']['build_date']
        log.info('Last Build was %s', last_build_date)
        last_build_tag = last_metadata['release_tag']
        log.info('Last Release Tag was %s',last_build_tag)

        current_build_date = current_metadata['ci']['build_date']
        log.info('Current Build was %s', current_build_date)
        current_build_tag = current_metadata['release_tag']
        global TAG
        TAG = current_build_tag
        log.info('Current Release Tag was %s',current_build_tag)
        if current_build_date > last_build_date  and current_build_tag == last_build_tag:
            log.info("This release %s is New. GH Pages and GH Releases will be enabled if on MASTER")
            with open(FLAGS_SCRIPT, 'w+') as flag_file:
                flag_file.write('#!/usr/bin/env bash\nexport DEPLOY=true\nexport BUILD_TAG=' + current_build_tag + '\n')
        else:
            log.info("Release is already the latest.")


def main():
    """
    Main
    """
    dl(file_name='metadata.json',file_url="https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/metadata/release.json")
    check_last_build()
    copy_release_files()
    copy_metadata_files()




if __name__ == '__main__':
    try:
        main()
    finally:
        log.removeHandler(log_file_handler)
        log.removeHandler(log_console_handler)