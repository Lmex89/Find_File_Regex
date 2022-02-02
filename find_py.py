#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re


class GetFilesAndDirs:

    __slots__ = ('string_path', 'list_of_dirs', 'list_matches', 'name_to_find')

    def __init__(self, string_path: str, name_to_find: str):
        self.string_path = string_path
        self.name_to_find = name_to_find
        self.list_of_dirs = []

    @staticmethod
    def get_full_path(str1: str, str2: str):
        my_tuple = (
            str1,
            '/',
            str2,
        )
        return ''.join(my_tuple)

    def get_dirs_and_files(self):

        read_write = os.access(self.string_path, os.W_OK) and os.access(
            self.string_path, os.R_OK)
        if not read_write:
            return {
                'dirs': [],
                'files': [],
            }
        dirs_and_files = os.listdir(self.string_path)

        list_of_files = []
        for item in dirs_and_files:
            path = self.get_full_path(self.string_path, item)
            if os.path.isdir(path):
                self.list_of_dirs.append(path)
            elif os.path.isfile(path):
                list_of_files.append(item)

        return {
            'dirs': self.list_of_dirs,
            'files': list_of_files,
        }

    def get_file_(self, string: str):

        pattern = r'((\.|\w)*%s(\w)*.*)' % self.name_to_find
        find_match = re.findall(pattern, string)
        return find_match[0] if find_match else None

    def get_file_matches(self):

        dirs_and_files = self.get_dirs_and_files()
        list_of_files = dirs_and_files['files']
        self.list_matches = []
        for item in list_of_files:
            match = self.get_file_(item)
            if match:
                full_path_str = self.get_full_path(self.string_path, match[0])
                self.list_matches.append(full_path_str)

        return {
            'parent_path': self.string_path,
            'dirs': self.list_of_dirs,
            'matches': self.list_matches
        }


class TreeFile:
    """
    {'parent_path': '/Users/sunwise/Documents/Recursive_regex',
    'dirs': ['/Users/sunwise/Documents/Recursive_regex/A/',
    '/Users/sunwise/Documents/Recursive_regex/B/'],
    'matches': []}

        """
    def __init__(self, get_files_and_dirs: GetFilesAndDirs, level: int = None):
        self._instance_ = get_files_and_dirs
        self.level = level if level is None else 3
        self._first_level = 0
        self.all_matches = []

    def _main_(self):
        first_level_path = self._instance_.get_file_matches()
        self._first_level += 1
        flag = True
        dirs = first_level_path['dirs']
        name_to_find = self._instance_.name_to_find
        for match in first_level_path['matches']:
            self.all_matches.append(match)
        result = None
        while flag:
            if len(dirs) == 0:
                flag = False
            if self._first_level > self.level:
                flag = False
            total_dirs = []
            for dir in dirs:
                instance = GetFilesAndDirs(dir, name_to_find)
                result = instance.get_file_matches()
                matches = result['matches']
                if matches:
                    for match in matches:
                        self.all_matches.append(match)
                if result.get('dirs'):
                    for dir in result.get('dirs'):
                        total_dirs.append(dir)
                    self._first_level += 1
            if total_dirs:
                dirs = total_dirs
            self._first_level += 1
        return self.all_matches


import sys

if len(sys.argv) <= 2:
    print("need more arguments for this command")
else:
    path = sys.argv[1]
    string_to_find = sys.argv[2]
    os.chdir(path)
    retval = os.getcwd()
    regex = GetFilesAndDirs(path, string_to_find)
    treenode = TreeFile(regex, level=3)
    result = treenode._main_()
    for r in result:
        print(r)
