import sys
import os
import re
from shutil import copyfile

home = os.path.expanduser('~')
target_dir = home + "/manifests/"
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

def pick_folder(folder):
    for item in os.listdir(folder):
        subpath = os.path.join(folder, item)
        if os.path.isdir(subpath):
            pick_folder(subpath)
        elif is_manifest(subpath):
            copy_file(subpath)


def is_manifest(file_name):
    return os.path.basename(file_name) == "manifest.webapp"

def copy_file(fn):
    (head, tail) = os.path.split(fn)
    parent = os.path.basename(head)
    target = target_dir + parent + "_" + tail
    print('copy {0} to {1}'.format(fn, target))
    copyfile(fn, target) 

pick_folder('/home/data/yf/kaios_code/apps')
