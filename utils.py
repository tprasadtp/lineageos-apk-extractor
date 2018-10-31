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
import time
import sys
import json
from pathlib import Path
import logging, logging.handlers
from functools import wraps
try:
    import requests
except ImportError:
    sys.exit("Failed to import requests")

# Default max attempts to download a file
REQUESTS_MAX_TRIES = 3
REQUESTS_BACKOFF = 2
log = logging.getLogger()

def retry(exceptions, tries=REQUESTS_MAX_TRIES, delay=3, backoff=REQUESTS_BACKOFF, logger=logging.getLogger('LOS_APK_Extractor')):
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
                    msg = '{}, Retrying in {} seconds...'.format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(Exception, tries=3, logger=log)
def __download_file(file_name, file_url):
    """
    Download the File from file_url, save it as output_file.
    Requires requests v2.19+. Older versions may not support
    `with` statement.
    """
    log.info('Downloading file.....')
    with requests.get(file_url, stream = True, timeout=10) as response:
        log.debug('Response code is %s', response.status_code)
        response.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def get_file(file_name, file_url):
    """
    Try to download the file with <max_attempts>
    Returns Class FileDownloadResult.
    """
    if os.path.isfile(file_name):
        log.info('File %s already exists. It will be deleted.', file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            log.critical('Failed to remove existing file : %s', file_name)
            log.error('Error was %s', e.strerror)
            sys.exit(1)
    log.info("Attempting to download : %s", file_name)
    log.info("From URL: %s", file_url)
    __download_file(file_name=file_name, file_url=file_url)

def write_json(dict={}, file_name='release.json'):
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
        with open(file_name, 'w+') as op_json:
            op_json.write(json.dumps(dict, indent=4))
            log.debug('JSON Dump is : %s', json.dumps(dict))
    except Exception as e:
        log.critical("Failed to write %s.", file_name)
        log.exception(e)
        sys.exit(1)
