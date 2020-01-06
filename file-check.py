#!/bin/bash/python3
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
import time
from datetime import datetime
from os import listdir
from os.path import isfile, isdir
from re import findall

global new_log, files

def check_summ(path : str):
    with open(path, 'r') as f:
        hash = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        f.close()
    return hash

def get_time(firstline = False):
    if not firstline:
        time = datetime.strftime(datetime.now(), "%H:%M:%S")
        return time
    time = datetime.strftime(datetime.now(), "%H:%M:%d:%m:%Y")
    return time

def catpath(path : str, file : str):
    catpath = path + '/' + file
    return catpath

def log_write(path : str, hash: str, status : str):
    global new_log
    with open(new_log, 'a') as log:
        log.write('---' + path + ' ' + hash + ' ' + status + ' ' + get_time() + '\n')
        log.close()

def check_file(path : str):
    global files
    hash = check_summ(path)
    if path in files.keys():
        if os.path.exists(path):
            item = files.pop(path)
            if item[0] == hash:
                    status = 'OLD'
            else:
                status = 'EDITED'
    else:
        status = 'NEW'
    log_write(path, hash, status)

def check_deleted(path : str):
    global files
    del_keys = []
    for key in files.keys():
        if key.find(path) != -1:
            if len(key.split('/')) == len(path.split('/')) + 1:
                del_keys.append(key)
                log_write(key, files[key][0], 'DELETED')

    for key in del_keys:
        files.pop(key)

def is_file(line : list):
    if line[0].startswith('---'): return True
    return False

def write_dir(path : str):
    global new_log
    with open(new_log, 'a') as log:
        log.write(path + '\n\n')
        log.close()

def firstline():
    global new_log
    with open(new_log, 'a') as log:
        time = get_time(True)
        log.write(time)
        log.write('\n')
        log.close()

def traveler(path : str):
    files = [f for f in listdir(path) if isfile(catpath(path, f))]
    for file in files:
        check_file(catpath(path, file))
    check_deleted(path)
    write_dir(path)
    dirs = [d for d in listdir(path) if isdir(catpath(path, d))]
    for dir in dirs:
        traveler(catpath(path, dir))

def create_name(logfile : str):
    try:
        num = findall('\d+', logfile)[0]
    except IndexError:
        num = '0'
    name = logfile.split('/')[-1].split(num)[0]
    global new_log
    num = int(num) + 1
    new_log = name + str(num)
    return


if __name__ == '__main__':

    print('Enter a path to the logfile:')
    logfile = str(input())

    create_name(logfile)
    try:
        with open(logfile, 'r') as log:
            global files
            files = {}
            path = ''
            log.readline()
            for line in log:
                line = line.split()
                if line: 
                    if is_file(line):
                        files[line[0][3:]] = line[1:3] #hash+status
                    elif path == '': #if its his first directory
                        path = line[0]
            log.close()

            firstline()
            traveler(path)
    except:
        print('Unable to open')
        time.sleep(3)
        sys.exit()
