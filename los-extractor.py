# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

# Imports
import os, shutil, hashlib, atexit, sys, re
import logging
import logging.handlers
from inspect import signature
try:
    import requests, backoff
    from requests import exceptions, HTTPError, ConnectionError, Timeout
except ImportError:
    raise SystemExit
try:
    from bs4 import BeautifulSoup
except ImportError:
    # Try importing if bs4 is installed from source
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        raise SystemExit

# Define URLs
#los_zip_url = "https://mirrorbits.lineageos.org/full/marlin/20181016/lineage-15.1-20181016-nightly-marlin-signed.zip"
#los_zip_sha256_url = los_zip_url + "?sha256"
# Files
LOG_FILE = "Lineage-APK-Extractor.logs"
LOS_ZIP_FILE = "lineage.zip"
LOS_SHA256_FILE = "lineage.sha256.txt"
# Default max attempts to download a file
MAX_GET_FILE_RETRIES = 3
# Use chunk size of 128K
FILE_HASH_BUFFER = 131072

# Arrays for LOS ZIP Data
LOS_REL_TYPE = []
LOS_REL_VERSION = []
LOS_REL_URL = []
LOS_REL_SIZE = []
LOS_REL_DATE = []

# Logs
log = logging.getLogger('LOS_APK_Extractor')
log.setLevel(logging.DEBUG)
# Create Rotating file handler
log_file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3 )
# Set file Log handler to Lower Log level
log_file_handler.setLevel(logging.DEBUG)
# Create console handler with a higher log level
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.INFO)
# Formatters
log_file_handler.setFormatter(logging.Formatter('[ {asctime} ] [ {levelname:8s} ] - {message}', style='{'))
log_console_handler.setFormatter(logging.Formatter('[ {levelname:8s} ] - {message}', style='{'))
# Add the handlers to the logger
log.addHandler(log_file_handler)
log.addHandler(log_console_handler)

logging.getLogger('backoff').addHandler(log_file_handler)
logging.getLogger('backoff').setLevel(logging.ERROR)


@atexit.register
def __close_logs(exit_code):
    """
    Closes all Log Handlers.
    Exits with code.
    """
    log.removeHandler(log_file_handler)
    log.removeHandler(log_console_handler)
    params = len(signature(__close_logs).parameters)
    if params == 1:
        sys.exit(exit_code)
    elif params > 1:
        sys.exit(101)

@backoff.on_exception(backoff.expo,
                      (requests.exceptions.HTTPError,
                       requests.exceptions.ConnectionError,
                       requests.exceptions.TooManyRedirects,
                       requests.exceptions.Timeout),
                      max_tries=3,
                      max_time=300)
def __download_file(file_name, file_url):
    """
    Download the File from file_url, save it as output_file.
    If file already exists its deleted. Requires requests
    v2.19+. Older versions may not support `with` statement.
    Returns: True if error free or False if fails.
    """
    if os.path.isfile(file_name):
        log.info('%s exists.', file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            log.critical('Failed to remove existing File : %s', file_name)
            log.error('Error was %s', e.strerror)
            __close_logs(2)
    log.info('Downloading File: %s.', file_name)
    log.debug('From URL: %s', file_url)
    try:
        with requests.get(file_url, stream = True, timeout=10) as response:
            log.debug('Response code is %s', response.status_code)
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.HTTPError as err_http:
        log.debug('Something went wrong while processing the request.. We got the response code below. Thats all we know.' )
        log.debug('Error Code is : %s', err_http)
        return False
    except requests.exceptions.ConnectionError as err_conn:
        log.debug('Failed to Get %s. Reason: %s', file_name, err_conn)
    else:
        return True

class FileDownloadResult(object):
    """
    File Download result class.
    self.res for result
    self.attempt last attempt.
    """
    __slots__ = ["res", "attempt"]
    def __init__(self, res, attempt):
        self.res = res
        self.attempt = attempt

def get_file(file_name, file_url, max_attempts = MAX_GET_FILE_RETRIES):
    """
    Try to download the file with <max_attempts>
    Returns Class FileDownloadResult.
    """
    log.info("Attempting to Download %s", file_name)
    for download_counter in range (1, max_attempts+1, 1):
        log.debug("Attempt %d, to get %s", download_counter, file_url )
        download_file_result = __download_file(file_name, file_url)
        if download_file_result:
            log.debug("Success!. Retrieved from %s", file_url)
            break
        else:
            log.debug("Failed to retrieve the file.%d attempts remaining", max_attempts-download_counter)
    return FileDownloadResult(download_file_result, download_counter)

def verify_sha256_checksum(file_name, checksum):
    """
    Verify checksum of a file.
    Filename        : File to Verify
    checksum        : SHA256SUM
    Returns Boolean : True if matches, False if fails.
    """
    if os.path.isfile(file_name):
        log.debug("File %s is present on FS.", file_name)
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
        log.critical('File not found.')
        __close_logs(3)
    if checksum.lower() == sha256hash.hexdigest():
        log.debug('File Hashes Match.')
        return True
    else:
        log.debug('File hashes do not match.')
        return False

def extract_checksum_from_file(file_name):
    """
    Extract Checksum from the File.
    Returns Checksum in HeX
    """
    if os.path.isfile(file_name):
        log.debug("File %s is present on FS.", file_name)
        with open(file_name, 'rt') as checksum_file:
            return checksum_file.readline().split(" ",1)[0]
    else:
        log.error("File %s not found.", file_name)

@backoff.on_exception(backoff.expo,
                      (requests.exceptions.HTTPError,
                       requests.exceptions.ConnectionError,
                       requests.exceptions.TooManyRedirects,
                       requests.exceptions.Timeout),
                      max_tries=3,
                      max_time=300)
def scrap_los_download_page(device_name=marlin):
    """
    Scrap Zip file URLs and data from lineage os download page.
    """
    try:
        log.debug('Getting Download Page for %s', device_name)
        los_download_page = requests.get("https://download.lineageos.org/marlin")
    except requests.exceptions.HTTPError as err_http:
        log.debug('HTTP Error.')
        log.debug('Error Code is : %s', err_http)
        return False
    except requests.exceptions.ConnectionError as err_conn:
        log.debug('Failed to Connect. Reason: %s', err_conn)
    log.info('Parsing download page...')
    soup = BeautifulSoup(los_download_page.content, features="lxml")
    table = soup.find('table')
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        if len(td) == 5: # Making sure not to grab header
            LOS_REL_TYPE.append(td[0].string)
            LOS_REL_VERSION.append(td[1].string)
            LOS_REL_URL.append((td[2].a).get('href'))
            LOS_REL_SIZE.append(td[3].string)
            LOS_REL_DATE.append(td[4].string)
    log.debug('----------------------------------------------------------')
    log.debug('------------------Parsed Variables------------------------')
    log.debug('LOS_REL_TYPE = %s', LOS_REL_TYPE)
    log.debug('LOS_REL_VERSION = %s', LOS_REL_VERSION)
    log.debug('LOS_REL_URL = %s', LOS_REL_URL)
    log.debug('LOS_REL_SIZE = %s', LOS_REL_SIZE)
    log.debug('LOS_REL_DATE = %s', LOS_REL_DATE)
    log.debug('----------------------------------------------------------')
    log.debug('----------------------------------------------------------')

# Download Zip
ZipDownloadResult = get_file(LOS_ZIP_FILE, los_zip_url, max_attempts=3)
if ZipDownloadResult.res:
    log.info("Successfully downloaded Lineage ZIP file")
else:
    log.error("Failed to download file, even after %s attempts.", ZipDownloadResult.attempt)
    __close_logs(21)
# Download Checksum
ChecksumDownloadResult = get_file(LOS_SHA256_FILE, los_zip_sha256_url, max_attempts=3)
if ChecksumDownloadResult.res:
    log.info("Successfully downloaded Checksum file.")
else:
    log.error("Failed to download Checksum file, even after %s attempts.", ChecksumDownloadResult.attempt )
    __close_logs(22)

# Verify Checksums
if verify_sha256_checksum(LOS_ZIP_FILE, extract_checksum_from_file(LOS_SHA256_FILE)):
    log.info("File's Checksum matches.")
else:
    log.error("File is corrupt. Please try again.")
    __close_logs(11)

__close_logs(0)