#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

# Standard Library Imports
import argparse
import json
import logging
import os
from pathlib import Path
import platform
import shutil
import sys

# Intenal Imports from project
from utils import get_file as dl
from utils import get_log_level, set_logger, write_json

MOUNT_POINT = "/mnt/lineage/"
RELEASE_DIR = Path("releases")
METADATA_DIR = Path("metadata")
DEVICE_NAME = os.environ.get("LOS_DEVICE_CODENAME", "bullhead")

RELEASE_NOTES = "metadata/Release-Notes.md"

# if os.environ.get('TRAVIS') == "true" or os.environ.get('CI') == "true":
#    print("Running on TRAVIS or other CI.")
#    TRANSFER_JSON = "transfer.json"
TRANSFER_JSON = "data/transfer.json"
# else:
#    TRANSFER_JSON = "test_transfer.json"

# Logs
# create logger
log = set_logger()


def define_tag_from_json(release_json):
    """
    Read release.json to set TAG variable
    """
    log.debug("Setting TAG Variable")
    if os.path.isfile(release_json):
        try:
            log.info("Reading json data from file.")
            with open(release_json) as r:
                jsondata = json.loads(r.read())
                global TAG
                TAG = jsondata["release"]["tag"]
                if str(TAG) == "":
                    log.critical("TAG is empty!.")
                    sys.exit(10)
        except Exception as e:
            log.critical("Failed to read from %s", release_json)
            log.exception(e)
            sys.exit(1)
    else:
        log.critical("%s is not found on the FS", release_json)
        sys.exit(1)


def copy_release_files(mount_point, transfer_json):
    """"
    Checks if mount point is available. If true,
    Copies APKS and other release assets to ./releases folder
    """
    log.info("Checking Mount point")
    if os.path.ismount(mount_point) or os.path.isdir(mount_point):
        if Path(RELEASE_DIR).exists():
            log.debug("%s folder is already present. deleting it..", RELEASE_DIR)
            try:
                shutil.rmtree(RELEASE_DIR)
            except Exception:
                log.critical("Failed to delete already existing %s", RELEASE_DIR)
                sys.exit(1)
        try:
            log.debug("Creating releases folder")
            os.makedirs(RELEASE_DIR)
        except Exception as e:
            log.critical("Failed to create %s directory.", RELEASE_DIR)
            log.exception(e)
            sys.exit(1)
        if os.path.isfile(transfer_json):
            with open(transfer_json) as t:
                transfer = json.loads(t.read())
            for app, path in transfer.items():
                fname = app + "-" + TAG + os.path.splitext(path)[1]
                try:
                    log.info("Copying %s from %s", app, path)
                    shutil.copy2(path, RELEASE_DIR / fname)
                except Exception as e:
                    log.error("Failed to Copy %s", app)
                    log.exception(e)
        else:
            log.critical(
                "%s is not present. Cannot determine file list.", transfer_json
            )
            sys.exit(1)


def copy_metadata_files():
    log.info("Copying Metadata")
    try:
        log.info("Copying README.md")
        shutil.copy2("README.md", METADATA_DIR / "README.md")
    except Exception as e:
        log.critical("Failed to copy Readme.md")
        log.exception(e)
        sys.exit(1)


def main(device, test_mode):
    """
    Main
    """
    release_josn = f"metadata/release-{device}.json"

    if test_mode:
        log.warn("Test mode is active")
        mount_point = "test/"
        transfer_json = "data/transfer-test.json"
    else:
        mount_point = MOUNT_POINT
        transfer_json = TRANSFER_JSON

    define_tag_from_json(release_josn)
    copy_metadata_files()
    copy_release_files(mount_point, transfer_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True,
    )
    parser.add_argument(
        "-d", "--device", required=True, type=str, help="Device Codename"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        help="Decrease output verbosity \
                           Default level is INFO",
    )
    parser.add_argument(
        "-t",
        "--test-mode",
        required=False,
        action="store_true",
        help="Use Test Mode without mounting img",
    )
    args = parser.parse_args()
    log.setLevel(get_log_level(args.quiet))
    main(args.device, args.test_mode)
