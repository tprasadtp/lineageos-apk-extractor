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
# Imports
import argparse
import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
import platform
import shutil
import sys
import time
import zipfile

# Intenal Imports from project
from utils import get_file as dl
from utils import get_log_level, set_logger, write_json

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Failed to import bs4")


# Settings
METADATA_DIR = Path("metadata")
BUILD_DIR = Path("build")
RELEASE_NOTES = "Release-Notes.md"
OLD_RELEASE_JSON = "build/old_release.json"
REL_TAG_BASE_URL = "https://github.com/tprasadtp/lineageos-apk-extractor/releases/tag/"
# Files
FLAGS_SCRIPT = "build/flags.sh"

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

if os.environ.get("FORCE_GH_RELEASE", "false").lower() == "true":
    FORCE_GH_RELEASE = True
else:
    FORCE_GH_RELEASE = False

# Logs
# create logger
log = set_logger()


def log_sysinfo():
    """
    Logs Basic system info
    """
    log.debug("------------------------System Info--------------------------")
    log.debug(f"Platform : %s, {platform.system()}")
    log.debug(f"Version : {platform.version()}")
    log.debug(f"Hostname : {platform.node()}")
    log.debug(f"Python Version : {platform.python_version()}")
    log.debug(f"Platform Arch : {platform.architecture()}")
    log.debug("-------------------------------------------------------------")


def extract_checksum_from_file(file_name):
    """
    Extract Checksum from the File.
    Returns Checksum in HeX
    """
    if os.path.isfile(file_name):
        log.debug("File's %s present on FS.", file_name)
        with open(file_name, "r") as checksum_file:
            return checksum_file.readline().split(" ", 1)[0]
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
        with open(file_name, "rb") as f:
            while True:
                data = f.read(FILE_HASH_BUFFER)
                if not data:
                    break
                sha256hash.update(data)
        log.debug("SHA256 hash for %s is : %s", file_name, sha256hash.hexdigest())
        log.debug("SHA256 hash SHOULD BE : %s", checksum.lower())
    else:
        log.critical("OOOPS! File not found.")
        sys.exit("ZIP File not Found.")
    if checksum.lower() == sha256hash.hexdigest():
        log.debug("File Hashes Match.")
        return True
    else:
        log.debug("File hashes do not match.")
        return False


def extract_los_urls(device_name):
    """
    Scrap Zip file URLs and data from lineage os download page.
    """
    log.debug("Getting Download Page for %s", device_name)
    los_dl_page_url = f"build/LineageOS_Downlad_Page_{device_name}.html"
    dl(
        file_name=los_dl_page_url,
        file_url=f"https://download.lineageos.org/{device_name}",
    )
    if os.path.isfile(los_dl_page_url):
        log.debug("%s file exists.", los_dl_page_url)
        with open(los_dl_page_url, encoding="utf-8") as los_dl_page_url:
            log.info("Parsing HTML page...")
            soup = BeautifulSoup(los_dl_page_url.read(), features="lxml")
            table = soup.find("table")
            for tr in table.find_all("tr"):
                td = tr.find_all("td")
                if len(td) == 5:  # Making sure not to grab header
                    LOS_REL_TYPE.append(td[0].string)
                    LOS_REL_VERSION.append(td[1].string)
                    LOS_REL_URL.append((td[2].a).get("href"))
                    LOS_REL_SIZE.append(td[3].string)
                    LOS_REL_DATE.append(td[4].string)
        global REL_TAG
        REL_TAG = f"{LOS_REL_VERSION[0]}.{LOS_REL_DATE[0]}"
        # Debugging stuff
        log.debug("------------------Parsed Variables------------------------")
        log.debug("LOS_REL_TYPE = %s", LOS_REL_TYPE)
        log.debug("LOS_REL_VERSION = %s", LOS_REL_VERSION)
        log.debug("LOS_REL_URL = %s", LOS_REL_URL)
        log.debug("LOS_REL_SIZE = %s", LOS_REL_SIZE)
        log.debug("LOS_REL_DATE = %s", LOS_REL_DATE)
        log.debug("REL_TAG is %s", REL_TAG)
        log.debug("----------------------------------------------------------")
    else:
        log.error("File %s not found.", los_dl_page_url)
        sys.exit(1)


def extract_zip_contents(zip_file, destination):
    """
    Extract contents of Zip file
    Arg:
        zip_file : path to Zipfile,
        destination:  directory to extract to
    """
    log.info("Extracting ZIP File")
    if os.path.isfile(zip_file):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(destination)
    else:
        log.error("%s not found.", zip_file)
        sys.exit("ZIP is not the filesystem.")


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
    log.info("Deleting old files if any....")
    shutil.rmtree("build/META-INF/", ignore_errors=True)
    shutil.rmtree("build/system/", ignore_errors=True)
    shutil.rmtree("build/install/", ignore_errors=True)
    log.debug("Deleting old DAT files (if any)")
    purge(dir="build/", pattern="system.*.*")
    log.debug("Deleting old IMG file (if any)")
    purge(dir="build/", pattern="*.img")
    purge(dir="build/", pattern="*.bin")


def generate_release_notes(time_stamp, device_name):
    """
    Release Notes Generator.
    Use Extracted info to generate Release notes.
    Args:
        time_stamp - (str) Timestamp in human readable form.
    Returns :
        None
    """
    log.info("Generating Release Notes...")
    _build_number = os.environ.get("TRAVIS_BUILD_NUMBER", "NA")
    _build_url = os.environ.get(
        "TRAVIS_JOB_WEB_URL",
        "https://travis-ci.com/tprasadtp/lineageos-apk-extractor/builds",
    )
    with open("build/" + RELEASE_NOTES, "w+") as release_notes:
        release_notes.write("## Release notes for lineage - " + REL_TAG + "\n\n")
        release_notes.write("| Lineage OS | Value |\n")
        release_notes.write("| -------- | ----- |\n")
        release_notes.write("| device   | " + device_name + "\n")
        release_notes.write("| version  | " + LOS_REL_VERSION[0] + "\n")
        release_notes.write("| type     | " + LOS_REL_TYPE[0] + "\n",)
        release_notes.write("| Zip file | [Link](" + LOS_REL_URL[0] + ")" + "\n")
        release_notes.write("| build    | " + LOS_REL_DATE[0] + "\n\n")
        release_notes.write("### Builder \n\n")
        release_notes.write(
            f"- Builder  : Python {platform.python_version()}, Arch - {platform.architecture()}\n"
        )
        release_notes.write(f"- Build Number : [{_build_number}]({_build_url}) \n")
        release_notes.write(f"- CI Node name : " + platform.node() + "\n")
        release_notes.write(f"- Release :  [Link]({REL_TAG_BASE_URL}{REL_TAG}) \n\n\n")
        release_notes.write("### Tags and Downloads\n\n")
        release_notes.write(
            "- This file is generated automatically.\n"
            + "- Tags correspond to lineage os build date.\n"
            + "- Every release is tagged as"
            + "[lineage-version].[los-build-date]\n\n"
        )
        release_notes.write("> Generated on : " + str(time_stamp) + "\n\n")
    log.debug("Generated Release Notes.")


def set_metadata_and_get_release_flag(
    current_ts,
    last_build_ts,
    last_build_tag,
    last_release_date,
    last_release_bnum,
    device_name,
):
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
    ts_human = time.strftime("%d %b at %H:%M", time.gmtime(UTC_TS))
    METADATA.update(
        {
            "version": 5,
            "ci": {
                "build_date": current_ts,
                "build_date_human": ts_human,
                "build_number": os.environ.get("TRAVIS_BUILD_NUMBER", "NA"),
            },
            "lineage": {
                "version": LOS_REL_VERSION[0],
                "build": LOS_REL_DATE[0],
                "build_type": LOS_REL_TYPE[0],
                "zip_file": LOS_REL_URL[0],
                "device": device_name,
            },
        }
    )
    # If build timestamp for old build is less than current timestamp and
    # if tags are different, set ci.deployed to Yes. Also set DEPLOY=true
    # in flags script. Also generate Release Notes.
    # ---------------------------------------------------------------------
    # Otherwise, set ci.deployed to No, and DEPLOY=false.
    # Do not generate release notes as it will not be used.
    # A global env var FORCE_GH_RELEASE is checked, if set to true, GH releases will
    # be forced.

    if (str(REL_TAG) != str(last_build_tag)) or FORCE_GH_RELEASE:
        log.info("GH Releases will be enabled if on MASTER")
        log.info("Last tag was %s", last_build_tag)
        METADATA["ci"].update({"deployed": "yes"})
        METADATA.update(
            {
                "release": {
                    "tag": REL_TAG,
                    "human_ts": ts_human,
                    "link": REL_TAG_BASE_URL + REL_TAG,
                    "ci_bnum": os.environ.get("TRAVIS_BUILD_NUMBER", "NA"),
                }
            }
        )
        # Generate Release Notes
        generate_release_notes(time_stamp=ts_human, device_name=device_name)
        return True
    else:
        log.info("Release is already latest. No need to deploy.")
        log.info("Last tag was %s", last_build_tag)
        METADATA["ci"].update({"deployed": "no"})
        # Keep old release date as is.
        METADATA.update(
            {
                "release": {
                    "tag": last_build_tag,
                    "human_ts": last_release_date,
                    "link": REL_TAG_BASE_URL + last_build_tag,
                    "ci_bnum": last_release_bnum,
                }
            }
        )
        return False


def get_old_jason_data(release_json):
    """
    Download and parse old release json
    Args: None
    Returns : A tuple (int last_build_ts, str last_build_tag, str last_release_date, last_release_ci_bnum)
    """
    log.debug("Downloading OLD release.json")
    dl(
        file_name=OLD_RELEASE_JSON,
        file_url=f"https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/{release_json}",
    )
    log.debug("Reading old release.json file...")
    if os.path.isfile(OLD_RELEASE_JSON):
        with open(OLD_RELEASE_JSON, "r") as oldjson:
            last_metadata = json.loads(oldjson.read())
            try:
                # Get Last build TS unix epoch
                last_build_date = last_metadata["ci"]["build_date"]
                log.info("Last Build was %s", last_build_date)
                # Get Last Release Tag
                last_build_tag = last_metadata["release"]["tag"]
                log.info("Last Release Tag was %s", last_build_tag)
                # Also Get last Release Date
                last_release_ts = last_metadata["release"]["human_ts"]
                log.info("Last Release TS was %s", last_release_ts)

                last_release_ci_bnum = last_metadata["release"]["ci_bnum"]
                log.info("Last Release Build was %s", last_release_ci_bnum)
                # Return tuple
                return (
                    int(last_build_date),
                    str(last_build_tag),
                    str(last_release_ts),
                    int(last_release_ci_bnum),
                )
            except KeyError as e:
                log.critical(
                    "JSON file from repository seems to be old. update it manually to latest schema."
                )
                log.exception(e)
                sys.exit(10)
    else:
        log.error("Old release.json cannot be found.")
        sys.exit(1)


def write_export_script(release_flag, release_tag, time_stamp):
    """
    Writes flags.sh to disk.
    """
    log.debug("Writing %s", FLAGS_SCRIPT)
    try:
        with open(FLAGS_SCRIPT, "w+") as flag_file:
            flag_file.write(
                "#!/usr/bin/env bash\n"
                + 'export DEPLOY="'
                + str(release_flag)
                + '"\n'
                + 'export BUILD_TAG="'
                + str(release_tag)
                + '"\n'
                + 'export LOS_REL_VERSION="'
                + str(LOS_REL_VERSION[0])
                + '"\n'
            )
    except Exception as e:
        log.critical("Failed to write exporter script.")
        log.exception(e)
        sys.exit(1)


def main(codename, skip_download=False):

    log_sysinfo()

    release_json = f"release-{codename}.json"

    if METADATA_DIR.is_dir():
        log.info("metadata directory alredy exists")
    else:
        if METADATA_DIR.exists():
            METADATA_DIR.unlink()
        log.info("Creating metadata directory")
        METADATA_DIR.mkdir(parents=True, exist_ok=True)

    if BUILD_DIR.is_dir():
        log.info("build directory alredy exists")
    else:
        if BUILD_DIR.exists():
            BUILD_DIR.unlink()
        log.info("Creating build directory")
        BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Extract URLs
    log.info("Getting LOS Download page for %s ...", codename)
    extract_los_urls(device_name=codename)

    # Download Zip
    log.info("Downloading ZIP File ...")
    los_zip_file = f"build/LineageOS_{codename}.zip"

    if not skip_download:
        dl(los_zip_file, LOS_REL_URL[0])
    else:
        log.warn("Skipping ZIP download")
    # Download Checksum
    log.info("Getting checksum File...")
    los_sha256_file = f"build/LineageOS_{codename}_ZIP_SHA256.txt"

    if not skip_download:
        dl(los_sha256_file, f"{LOS_REL_URL[0]}?sha256")
    else:
        log.warn("Skip downloading checksums")

    # Verify Checksums
    log.info("Verifying ZIP file checksums...")
    if verify_sha256_checksum(
        los_zip_file, extract_checksum_from_file(los_sha256_file)
    ):
        log.info("Woohooo.. ZIP File's Checksum matches.")
    else:
        log.error("Oh dear! ZIP File is corrupt. Please try again.")
        sys.exit(1)

    # Extract Files
    log.info("Extracting from ZIP File ....")
    # Delete Files from Last Run
    delete_old_files()
    # Extract files
    extract_zip_contents(zip_file=los_zip_file, destination="build/")

    # Release Notes & Metadata
    log.info("Getting Info about last build & release...")
    (
        last_build_ts,
        last_build_tag,
        last_relase_date,
        last_release_ci_bnum,
    ) = get_old_jason_data(release_json)

    log.info("Preparing Metadata....")
    GH_RELEASE_FLAG = set_metadata_and_get_release_flag(
        current_ts=UTC_TS,
        last_build_ts=last_build_ts,
        last_build_tag=last_build_tag,
        last_release_date=last_relase_date,
        last_release_bnum=last_release_ci_bnum,
        device_name=codename,
    )

    log.info("Generating %s", release_json)
    write_json(dict=METADATA, file_name=f"metadata/{release_json}")

    log.info("Writing exporter script...")
    write_export_script(
        release_flag=str(GH_RELEASE_FLAG).lower(),
        release_tag=REL_TAG,
        time_stamp=UTC_TS,
    )


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
                           Default level is DEBUG",
    )
    parser.add_argument(
        "-s",
        "--skip-zip-download",
        required=False,
        action="store_true",
        help="Skip Downloading Large ZIP",
    )
    args = parser.parse_args()
    log.setLevel(get_log_level(args.quiet))
    main(codename=args.device, skip_download=args.skip_zip_download)
