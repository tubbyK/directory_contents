from os import path, listdir
import json
from shutil import copy
from datetime import datetime

class directory:
    def __init__(self, fld_path: str, dir_content_file: str = 'contents.txt'):
        self.parent_fld = fld_path
        self.dir_content_file_path = fld_path + '\\' + dir_content_file
        self.dir_content_file_exists = self.file_exists()
        self.version = self.compute_version()
        self.dir_content = {}

    @property
    def parent_fld(self):
        return self.__parent_fld

    @parent_fld.setter
    def parent_fld(self, parent_fld):
        self.__parent_fld = parent_fld

    @property
    def dir_content_file_path(self):
        return self.__dir_content_file_path

    @dir_content_file_path.setter
    def dir_content_file_path(self, dir_content_file_path):
        self.__dir_content_file_path = dir_content_file_path

    @property
    def dir_content_file_exists(self):
        return self.__dir_content_file_exists

    @dir_content_file_exists.setter
    def dir_content_file_exists(self, dir_content_file_exists):
        self.__dir_content_file_exists = dir_content_file_exists

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def dir_content(self):
        return self.__dir_content

    @dir_content.setter
    def dir_content(self, dir_content):
        self.__dir_content = dir_content

    # check if file exists
    def file_exists(self):
        if path.isfile(self.dir_content_file_path):
            return True
        else:
            return False

    # get version number by reading from current directory content file
    def compute_version(self):
        if self.dir_content_file_exists:
            with open(self.dir_content_file_path, 'r') as json_file:
                return json.load(json_file)['version'] + 1
        else:
            return 1

    # get directory contents recursively
    def path_to_dict(self, fpath: str, d: {}):
        name = path.basename(fpath)
        if path.isdir(fpath):
            if name not in d:
                count = len([1 for item in listdir(fpath) if path.isfile(path.join(fpath,item)) and path.splitext(item)[-1]!='.lnk'])
                d[name] = {'count': count, 'files': []}
            for x in listdir(fpath):
                self.path_to_dict(path.join(fpath, x), d[name])
        else:
            d['files'].append(name)
        return d

    # generate the content
    def generate_content(self):
        self.dir_content['modified_date'] = datetime.today().strftime('%Y-%m-%d')
        self.dir_content['base_path'] = self.parent_fld.replace('\\','/')
        self.dir_content['version'] = self.version
        self.dir_content['content'] = self.path_to_dict(fpath=self.parent_fld, d={})

    # archive old directory list file
    def archive_file(self):
        if self.dir_content_file_exists:
            arc_file_name = self.dir_content_file_path.split('.')[0] + '_ver ' + str(self.version-1) + '.txt'
            copy(self.dir_content_file_path, arc_file_name)

    # write the content to file
    def write_content(self):
        if bool(self.dir_content):
            # archive file before write
            self.archive_file()
            with open(self.dir_content_file_path, 'w', encoding='utf8') as json_file:
                json.dump(self.dir_content, json_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    d = directory(r'c:\self\data')
    d.generate_content()
    d.write_content()