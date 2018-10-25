#!/usr/bin/env python
# -*- coding: utf-8 -*-
#====================================================
#          FILE: sdat2img.py
#       AUTHORS: xpirt - luxi78 - howellzhu
#          DATE: 2018-05-25 10:49:35 CEST
#====================================================

import sys, os, errno
import logging
log = logging.getLogger(__name__)
def main(TRANSFER_LIST_FILE, NEW_DATA_FILE, OUTPUT_IMAGE_FILE):
    __version__ = '1.1'

    if sys.hexversion < 0x02070000:
        log.critical ("Python 2.7 or newer is required.")
        return False
    else:
        log.debug('sdat2img binary - version: %s\n', __version__)

    def rangeset(src):
        src_set = src.split(',')
        num_set =  [int(item) for item in src_set]
        if len(num_set) != num_set[0]+1:
            log.info('Error on parsing following data to rangeset:\n%s' % src)
            sys.exit(1)

        return tuple ([ (num_set[i], num_set[i+1]) for i in range(1, len(num_set), 2) ])

    def parse_transfer_list_file(path):
        trans_list = open(TRANSFER_LIST_FILE, 'r')

        # First line in transfer list is the version number
        version = int(trans_list.readline())

        # Second line in transfer list is the total number of blocks we expect to write
        new_blocks = int(trans_list.readline())

        if version >= 2:
            # Third line is how many stash entries are needed simultaneously
            trans_list.readline()
            # Fourth line is the maximum number of blocks that will be stashed simultaneously
            trans_list.readline()

        # Subsequent lines are all individual transfer commands
        commands = []
        for line in trans_list:
            line = line.split(' ')
            cmd = line[0]
            if cmd in ['erase', 'new', 'zero']:
                commands.append([cmd, rangeset(line[1])])
            else:
                # Skip lines starting with numbers, they are not commands anyway
                if not cmd[0].isdigit():
                    log.debug('Command "%s" is not valid.' % cmd)
                    trans_list.close()
                    return False

        trans_list.close()
        return version, new_blocks, commands

    BLOCK_SIZE = 4096

    version, new_blocks, commands = parse_transfer_list_file(TRANSFER_LIST_FILE)

    if version == 1:
        log.debug('Android Lollipop 5.0 detected!\n')
    elif version == 2:
        log.debug('Android Lollipop 5.1 detected!\n')
    elif version == 3:
        log.debug('Android Marshmallow 6.x detected!\n')
    elif version == 4:
        log.debug('Android Nougat 7.x / Oreo 8.x detected!\n')
    else:
        log.warning('Unknown Android version!\n')

    # Don't clobber existing files to avoid accidental data loss
    try:
        output_img = open(OUTPUT_IMAGE_FILE, 'wb')
    except IOError as e:
        if e.errno == errno.EEXIST:
            log.error('Error: the output file %s already exists', e.filename)
            log.error('Remove it, rename it, or choose a different file name.')
            return False
        else:
            raise

    new_data_file = open(NEW_DATA_FILE, 'rb')
    all_block_sets = [i for command in commands for i in command[1]]
    max_file_size = max(pair[1] for pair in all_block_sets)*BLOCK_SIZE

    for command in commands:
        if command[0] == 'new':
            for block in command[1]:
                begin = block[0]
                end = block[1]
                block_count = end - begin
                log.debug('Copying %s blocks into position %s...', block_count, begin)

                # Position output file
                output_img.seek(begin*BLOCK_SIZE)

                # Copy one block at a time
                while(block_count > 0):
                    output_img.write(new_data_file.read(BLOCK_SIZE))
                    block_count -= 1
        else:
            log.debug('Skipping command %s...' , command[0])

    # Make file larger if necessary
    if(output_img.tell() < max_file_size):
        output_img.truncate(max_file_size)

    output_img.close()
    new_data_file.close()
    log.info('Done! Output image: %s' % os.path.realpath(output_img.name))
    return True

if __name__ == '__main__':
    TRANSFER_LIST_FILE = "system.transfer.list"
    NEW_DATA_FILE = "system.new,dat.br"
    OUTPUT_IMAGE_FILE = "system.img"
    LOG_FILE = "SD2IMG.logs"

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    l2_file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3 )
    l2_file_handler.setLevel(logging.DEBUG)
    l2_console_handler = logging.StreamHandler()
    l2_console_handler.setLevel(logging.INFO)
    l2_file_handler.setFormatter(logging.Formatter('[ {asctime} ] [ {levelname:8s} ] - {message}', style='{'))
    l2_console_handler.setFormatter(logging.Formatter('[ {levelname:8s} ] - {message}', style='{'))
    log.addHandler(l2_file_handler)
    log.addHandler(l2_console_handler)
    # Try Main
    try:
        main(TRANSFER_LIST_FILE, NEW_DATA_FILE, OUTPUT_IMAGE_FILE)
    finally:
        log.removeHandler(l2_file_handler)
        log.removeHandler(l2_console_handler)
