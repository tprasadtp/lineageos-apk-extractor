# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License.
If you have not received a copy of the license,
you can find it at the link below.
https://opensource.org/licenses/MIT
"""

# Imports
import os, shutil, hashlib, atexit
import sys, platform, zipfile, subprocess, json
from pathlib import Path
import logging, logging.handlers
# For Retries
import time
from functools import wraps

# Version Checks.
if int(str(sys.version_info.major) + str(sys.version_info.minor)) < 34:
    raise Exception("Needs Python version 3.5 & above.")
try:
    import requests
except ImportError:
        raise SystemExit
try:
    from bs4 import BeautifulSoup
except ImportError:
    # Try importing if bs4 is installed from source
#    raise SystemExit
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        raise SystemExit

# Settings
DEVICE_NAME = "bullhead"
RELEASE_NOTES = "release_notes.md"
RELEASE_JSON = "release.json"
# Files
LOG_FILE = "Lineage-APK-Extractor.logs"
LOS_ZIP_FILE = "LineageOS.zip"
LOS_SHA256_FILE = "Lineage_ZIP_SHA256.txt"

# Default max attempts to download a file
REQUESTS_MAX_TRIES = 3
REQUESTS_BACKOFF = 2
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


@atexit.register
def __close_logs():
    """
    Closes all Log Handlers.
    Exits with code.
    """
    log.removeHandler(log_file_handler)
    log.removeHandler(log_console_handler)

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

def log_sysinfo():
    """
    Logs Basic system info
    """
    log.debug('------------------------System Info------------------------------')
    log.debug('Platform : %s, Version: %s', platform.system(), platform.version())
    log.debug('Hostname: %s', platform.node())
    log.debug('Python Version: %s', platform.python_version())
    log.debug('Platform Arch: %s', platform.architecture())
    log.debug('-----------------------------------------------------------------')

@retry(Exception, tries=3, logger=log)
def __download_file(file_name, file_url):
    """
    Download the File from file_url, save it as output_file.
    Requires requests v2.19+. Older versions may not support
    `with` statement.
    """
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
        log.info('%s exists.', file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            log.critical('Failed to remove existing File : %s', file_name)
            log.error('Error was %s', e.strerror)
            __close_logs()
            raise OSError
    log.info("Attempting to download : %s", file_name)
    log.info("From URL: %s", file_url)
    __download_file(file_name=file_name, file_url=file_url)


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
        log.critical('File not found.')
        __close_logs()
        raise Exception('File not found.')
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
    get_file(file_name="los-dl.html", file_url="https://download.lineageos.org/"+device_name)
    if os.path.isfile("los-dl.html"):
        log.debug('los-dl.html file exists.')
        with open("los-dl.html", encoding="utf-8") as los_dl_page:
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
        # Debugging stuf
        log.debug('----------------------------------------------------------')
        log.debug('------------------Parsed Variables------------------------')
        log.debug('LOS_REL_TYPE = %s', LOS_REL_TYPE)
        log.debug('LOS_REL_VERSION = %s', LOS_REL_VERSION)
        log.debug('LOS_REL_URL = %s', LOS_REL_URL)
        log.debug('LOS_REL_SIZE = %s', LOS_REL_SIZE)
        log.debug('LOS_REL_DATE = %s', LOS_REL_DATE)
        log.debug('----------------------------------------------------------')
        log.debug('----------------------------------------------------------')
    else:
        log.error('File los-dl.html not found.')
        SystemExit('File los-dl.html is not found.')


def extract_zip_contents(zip_file, destination):
    """
    Extract contents of Zip file
    Arg:
        zip_file : path to Zipfile,
        destination:  directory to extract to
    """
    if os.path.isfile("los-dl.html"):
        with zipfile.ZipFile(zip_file,"r") as zip_ref:
          zip_ref.extractall(destination)
    else:
        log.error('%s not found.', zip_file)
        SystemError('ZIP is not the filesystem.')

def purge(dir, pattern):
    """
    Delete files in specified dir by pattern
    Args:
        dir : directory to scan
        pattern : regex to match
    """
    for p in Path(dir).glob(pattern):
        p.unlink()


def __delete_old_dat_files():
    log.info('Deleting old files if any....')
    shutil.rmtree('META-INF/', ignore_errors=True)
    shutil.rmtree('system/', ignore_errors=True)
    shutil.rmtree('install/',ignore_errors=True)
    log.debug('Deleting DAT files...')
    purge(dir=os.getcwd(), pattern="system.*.*")
    log.debug('Deleting *.img')
    purge(dir=os.getcwd(), pattern="*.img")
    purge(dir=os.getcwd(), pattern="*.bin")


def convert_dat_file():
    """
    Convert dat to img using sdat2img.py
    """
    log.info('Converting DAT file to img file')
    if os.path.isfile('sdat2img.py'):
        import sdat2img
        try:
            sdat2img.main(TRANSFER_LIST_FILE="system.transfer.list", NEW_DATA_FILE="system.new.dat.br",OUTPUT_IMAGE_FILE="system.img")
        except Exception:
            log.critical('Failed to convert DAT file to image file')
            SystemExit
    else:
        log.error('sdat2img.py is not in current directory.')
        SystemExit('sdat2img.py is missing.')

def generate_release_notes():
    """
    Release Notes Generator.
    Use Extracted info to generate Relase notes.
    """
    if os.path.isfile(RELEASE_NOTES):
        log.info('Release notes.txt exists')
        try:
            log.debug('Deleting old release notes')
            os.remove(RELEASE_NOTES)
        except OSError as e:
            log.critical('Failed to remove existing release notes.')
            log.error('Error was %s', e.strerror)
            __close_logs()
            raise OSError
    log.info('Generating Release Notes...')
    with open(RELEASE_NOTES, 'w+') as release_notes:
            release_notes.write('# Release notes for Tag lineage -' + LOS_REL_DATE[0] + '\n\n')
            ts = time.strftime('%I:%M %p %Z on %b %d, %Y')
            release_notes.write('- Release notes generated on : ' + ts + '\n')
            release_notes.write('- Lineage OS Version : ' + LOS_REL_VERSION[0] + '\n')
            release_notes.write('- Lineage OS Type : ' + LOS_REL_TYPE[0] + '\n', )
            release_notes.write('- Zip file used : [ZIPfile]('+ LOS_REL_URL[0] + ')' + '\n')
            release_notes.write('- LOS was built on : ' + LOS_REL_DATE[0] + '\n\n\n')
            release_notes.write('## Tags and Downloads\n')
            release_notes.write('- This is generated automatically.\n' +
                                '- Tags correspond to build date.\n' +
                                '- Every release is tagged lineage-[lineage-version]-build-date\n\n')
            release_notes.write('## Logs\n' +
                                'Logs related to this Build are available as assets or available in logs folder in `metadata` branch.\n')
    log.debug("Generated Release Notes")

def generate_json_metadata():
    """
    Generate metadata
    Build Date, LOS_REL_VERSION
    """
    log.info('Generating Metadata JSON for gh-pages')
    metadata = {}
    metadata.update({ 'version' : 1,
                      'lineage_build_date' : LOS_REL_DATE[0],
                      'last_build_passed' : "True",
                      'lineage_version' : LOS_REL_VERSION[0],
                      'release_tag' : LOS_REL_VERSION[0] + '-' + LOS_REL_DATE[0]
                    })
    with open(RELEASE_JSON, 'w+') as release_json:
        release_json.write(json.dumps(metadata))
        log.debug('JSON Dump is : %s',json.dumps(metadata))

def main():
    # Log Basic Info
    os.chdir(os.path.dirname(__file__))
    log_sysinfo()
    # Extract URLs
    log.info('Getting LOS Download page for %s...', DEVICE_NAME)
    extract_los_urls(device_name=DEVICE_NAME)
    # Download Zip
    log.info('Downloading ZIP File...')
    get_file(LOS_ZIP_FILE, LOS_REL_URL[0])
    # Download Checksum
    log.info('Getting Checksum File...')
    get_file(LOS_SHA256_FILE, LOS_REL_URL[0]+"?sha256")
    # Verify Checksums
    log.info('Verifying Checksums...')
    if verify_sha256_checksum(LOS_ZIP_FILE, extract_checksum_from_file(LOS_SHA256_FILE)):
        log.info("File's Checksum matches.")
    else:
        log.error("File is corrupt. Please try again.")
        __close_logs()
        raise Exception('ZIP File is corrupt or modified')
    # Extract Files
    log.info('Extracting from ZIP File ....')
    extract_zip_contents(zip_file=LOS_ZIP_FILE, destination=os.getcwd())
    __delete_old_dat_files()
    #convert_dat_file()
    generate_release_notes()
    generate_json_metadata()


if __name__ == '__main__':
    try:
        main()
    finally:
        log.removeHandler(log_file_handler)
        log.removeHandler(log_console_handler)