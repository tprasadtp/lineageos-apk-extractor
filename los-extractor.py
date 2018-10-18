# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License
"""

# Imports
import logging
import logging.handlers
import os, shutil
try:
    import requests
except ImportError as e:
    raise

# Define URLs
los_zip_url = "https://static.prasadt.com/logo64/ubuntu.png"
los_zip_sha256_url = "https://static.prasadt.com/logo64/linuxmint.png"
LOG_FILE = "Lineage-APK-Extractor.logs"
MAX_GET_FILE_RETRIES = 3

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
log_file_handler.setFormatter(logging.Formatter('{asctime} - {name} - {levelname:8s} - {message}', style='{'))
log_console_handler.setFormatter(logging.Formatter('{levelname:8s} - {message}', style='{'))
# Add the handlers to the logger
log.addHandler(log_file_handler)
log.addHandler(log_console_handler)

def __close_logs():
    """
    Closes all Log Handlers.
    Reserved for Future: Close & flush file handlers
    """
    log.removeHandler(log_file_handler)
    log.removeHandler(log_console_handler)
    logging.shutdown()

def download_file(file_url, file_name):
    """
    Download the File from file_url, save it as output_file.
    If file already exists its deleted. Requires requests
    v2.19+. Older versions may not support `with` staement.
    Returns: True if error free or False if fails.
    """
    if os.path.isfile(file_name):
        log.info('%s exists.', file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            log.critical('Failed to remove existing File : %s', file_name)
            log.error('Error was %s', e.strerror)
            os._exit(2)
    log.info('Downloading File: %s, from URL: %s', file_name, file_url)
    try:
        with requests.get(file_url, stream = True, timeout=10) as response:
            log.debug('Response code is %s', response.status_code)
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.HTTPError as err_http:
        log.error('Something went wrong while peocessing the request.. We got the response code below. Thats all we know.' )
        log.error('Error Code is : %s', err_http)
        return False
    except requests.exceptions.ConnectionError as err_conn:
        log.error('Failed to Get %s. Reason: %s', file_name, err_conn)
    else:
        log.info('Successfully Downloaded File: %s', file_url)
        return True


download_file(los_zip_url, 'zipfile.png')
download_file(los_zip_sha256_url, 'shasum.png')


__close_logs()