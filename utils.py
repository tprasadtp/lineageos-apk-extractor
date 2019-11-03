# -*- coding: utf-8 -*-
#  Copyright (c) 2018-2019.
#  Prasad Tengse
#


# Standard Library Imports
import argparse
from functools import wraps
import json
import logging
import os
from pathlib import Path
import re
import sys
import time
import typing
from typing import Any

# External Imports (via PyPI or custom index)
from coloredlogs import ColoredFormatter
import requests

# Default max attempts to download a file
REQUESTS_MAX_TRIES = 3
REQUESTS_BACKOFF = 2
log = logging.getLogger()


def retry(
    exceptions, tries=REQUESTS_MAX_TRIES, delay=3, backoff=REQUESTS_BACKOFF,
):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = "{}, Retrying in {} seconds...".format(e, mdelay)
                    log.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(Exception, tries=3)
def __download_file(file_name, file_url):
    """
    Download the File from file_url, save it as output_file.
    Requires requests v2.19+. Older versions may not support
    `with` statement.
    """
    log.info("Downloading file.....")
    with requests.get(file_url, stream=True, timeout=10) as response:
        log.debug("Response code is %s", response.status_code)
        response.raise_for_status()
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def get_file(file_name, file_url):
    """
    Try to download the file with <max_attempts>
    Returns Class FileDownloadResult.
    """
    if os.path.isfile(file_name):
        log.info("File %s already exists. It will be deleted.", file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            log.critical("Failed to remove existing file : %s", file_name)
            log.error("Error was %s", e.strerror)
            sys.exit(1)
    log.info("Attempting to download : %s", file_name)
    log.info("From URL: %s", file_url)
    __download_file(file_name=file_name, file_url=file_url)


def write_json(dict, file_name="release.json"):
    """
    Write JSON containing relevant data to file.
    Args:
        dict - dictionary containing data. defaults to "METADTA"
        file_name - JSON filename. defaults to release.json
    Returns:
        None
    """
    log.debug("Writing %s", file_name)
    try:
        with open(file_name, "w+") as op_json:
            op_json.write(json.dumps(dict, indent=4))
            log.debug("JSON Dump is : %s", json.dumps(dict))
    except Exception as e:
        log.critical("Failed to write %s.", file_name)
        log.exception(e)
        sys.exit(1)


def get_log_level(q_count: int = 0) -> int:
    """
    sets log level
    :param q_count: Number of -q flags passed
    :type q_count: int or None
    :param v_count: Number of -v flags passed
    :type: v_count: int or None
    """

    if q_count is None:
        return logging.DEBUG

    if q_count <= 0:
        return logging.DEBUG
    elif q_count == 1:
        return logging.INFO
    elif q_count == 2:
        return logging.WARN
    elif q_count == 3:
        return logging.ERROR
    elif q_count == 4:
        return logging.CRITICAL
    else:
        return logging.CRITICAL


def set_logger() -> logging.Logger:
    """
    Setup logging
    Returns a log.Logger object
    """
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(
        ColoredFormatter(
            fmt="%(asctime)s.%(msecs)3d "
            "%(module)15s %(levelname)8s "
            " %(lineno)3d  %(message)s"
        )
    )
    logger.addHandler(ch)
    return logger
