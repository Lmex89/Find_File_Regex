#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re


class Fzfpython:

    __slots__ = ('string_to_find', 'base_dir', 'matches')

    def __init__(self, string_to_find):
        self.string_to_find = string_to_find
        self.base_dir = os.getcwd()
        self.matches = list()

    def get_dirs_and_files(self):

        dirs_and_files = os.listdir()
        dirs = []
        files = []
        for item in dirs_and_files:
            if os.path.isdir(item):
                dirs.append(item)
            elif os.path.isfile(item):
                files.append(item)

        return {
            'dirs': dirs,
            'files': files,
        }

    def get_file_(self, string):

        pattern = r'((\.|\w)*%s.*)' % self.string_to_find
        find_match = re.findall(pattern, string)

        """ 
        a_list = ["ark", "disembark", "quack", "rock", "pork"]
        r = re.compile(".*rk")
        filtered_list = list(filter(r.match, a_list))

        print(filtered_list)
        OUTPUT
        """
        return find_match[0] if find_match else None

    def get_file_re(self, list_of_files, name_to_find):

        result = []
        for item in list_of_files:
            match = self.get_file_(item)
            if match:
                result.append(match[0])
        return result

    def get_files_matches(self):

        files = self.get_dirs_and_files()['files']
        dirs = self.get_dirs_and_files()['dirs']

        first_matches = self.get_file_re(files, self.string_to_find)

        if first_matches:
            for item in first_matches:
                if item not in ['.']:
                    self.matches.append(self.base_dir + '/'+item)
        if not dirs:
            return self.matches
        for idir in dirs:
            os.chdir(self.base_dir)
            new_path = self.base_dir + '/' + idir
            os.chdir(new_path)
            files = self.get_dirs_and_files()['files']
            _dirs = self.get_dirs_and_files()['dirs']
            next_file_matches = self.get_file_re(
                files, self.string_to_find)

            if next_file_matches:
                for item in next_file_matches:
                    if item not in ['.'] and len(item) > 1:
                        self.matches.append(new_path+'/'+item)
        return self.matches or None


regex = Fzfpython('dev')
print(regex.get_files_matches())
