#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re


class GetFilesAndDirs:
    
    __slots__ = ('string_path',
                 'list_of_dirs',
                 'list_matches',
                 'name_to_find'
                 )
    
    def __int__(self,string_path:str,name_to_find:str):
        self.string_path = string_path
        self.name_to_find = name_to_find
    
    def get_dirs_and_files(self):
    
        dirs_and_files = os.listdir(self.string_path)
        self.list_of_dirs = []
        list_of_files =[]
        for item in dirs_and_files:
            if os.path.isdir(item):
                self.list_of_dirs.append(item)
            elif os.path.isfile(item):
                list_of_files.append(item)

        return {
            'dirs': self.list_of_dirs,
            'files': list_of_files,
        }
    
    def get_file_(self, string):

        pattern = r'((\.|\w)*%s.*)' % self.name_to_find
        find_match = re.findall(pattern, string)
        return find_match[0] if find_match else None

    def get_file_matches(self):
         
        dirs_and_files = self.get_dirs_and_files()
        list_of_files = dirs_and_files['files']
        self.list_of_matches = []
        for item in list_of_files:
            match = self.get_file_(item)
            if match:
                self.list_of_matches.append(match[0])
        
        return {'dirs':self.list_of_dirs,'matches':self.list_matches}






regex = GetFilesAndDirs()
print(regex.get_files_matches())
