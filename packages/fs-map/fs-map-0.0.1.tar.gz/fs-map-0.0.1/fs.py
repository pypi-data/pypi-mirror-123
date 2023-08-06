from os import listdir, mkdir, rename, replace, rmdir, remove, makedirs, removedirs, renames
from os.path import exists, getsize, isdir, isfile, normcase, isabs, join, splitdrive, split, splitext, basename, dirname, normpath, abspath, realpath, relpath
from shutil import copyfileobj, copyfile, copymode, copy, copy2, ignore_patterns, copytree, rmtree, move
from glob import glob, iglob, glob0, glob1, escape


def get_filename(path):
    '''
    Returns a file name with a suffix
    '''

    _, filename = split(path)
    return filename


def get_filename1(path):
    '''
    Returns a file name that does not contain a suffix
    '''

    filename = get_filename(path)
    filename, _ = splitext(filename)
    return filename


def get_ext(path):
    '''
    Returns the file suffix
    '''

    _, ext = splitext(get_filename(path))
    return ext


def normcase1(path):
    '''
    Converts all characters in the path to lowercase and forward slashes to backslashes
    '''

    return normcase(path).replace('\\', '/')


def normpath1(path):
    '''
    Converts forward slashes in a path to backslashes
    '''

    return normpath(path).replace('\\', '/')
