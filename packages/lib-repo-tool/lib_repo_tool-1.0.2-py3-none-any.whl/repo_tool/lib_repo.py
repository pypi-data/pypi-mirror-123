import json
import os
import argparse
import shutil
from dataclasses import dataclass, asdict
from typing import List, Optional

from .common import available_arches, available_build_names, available_platforms
from . import common
from dacite import from_dict
from tabulate import tabulate

import logging
logger = logging.getLogger(__name__)


@dataclass
class LibData:
    name: str
    version: Optional[str]
    platform: Optional[str]
    arch: Optional[str]
    build: Optional[str]

    @classmethod
    def from_dict(cls, data) -> "LibData":
        return from_dict(LibData, data)

    def to_dict(self):
        return asdict(self)

    def file_key(self):
        if not self.name:
            raise Exception(f'invalid lib data: {self}')
        file_key = os.path.join(common.OSS_BASE_PATH, self.gen_path())
        file_key = os.path.join(file_key, self.get_zip_file_name())

        file_key = file_key.replace('\\', '/')

        return file_key

    def gen_path(self):
        p = self.name
        if self.version:
            p = os.path.join(p, self.version)
        if self.platform:
            p = os.path.join(p, self.platform)
        if self.arch:
            p = os.path.join(p, self.arch)
        if self.build:
            p = os.path.join(p, self.build)

        return p

    def get_zip_file_name(self):
        return self.name + "_lib.zip"

    def __str__(self):
        return f'{self.name}\t{self.version}\t{self.platform}\t{self.arch}\t{self.build}'


class LibRepo:
    def __init__(self):
        self.libs: Optional[list[LibData]] = None
        self.__repo_file_key = os.path.join(common.OSS_BASE_PATH, 'repo.json')
        self.__repo_file_key = self.__repo_file_key.replace('\\', '/')
    def pull_repo(self) -> "LibRepo":
        content = common.get_file_obj_2_str(self.__repo_file_key)
        if not content:
            return self

        libs_data = json.loads(content)
        self.libs = [LibData.from_dict(lib) for lib in libs_data]

        return self

    def push_repo(self) -> "LibRepo":
        if not self.libs:
            return self

        libs = [lib.to_dict() for lib in self.libs]
        common.upload_file_obj(self.__repo_file_key, json.dumps(libs))

        return self

    def add_new_lib(self, lib: LibData):
        if not self.libs:
            self.libs = []
        if self.exist(lib):
            raise Exception('already exist')
        self.libs.append(lib)
        self.push_repo()

    def remove_lib(self, lib: LibData):
        if not self.exist(lib):
            raise Exception('Not exist')

        self.libs.remove(lib)
        self.push_repo()
        common.remove_file(lib.file_key())

    def bulk_remove_libs(self, libs: List[LibData]):
        if not libs:
            return

        for l in libs:
            if not self.exist(l):
                raise Exception(f'Not exist, lib: {l}')

        for l in libs:
            self.libs.remove(l)
        self.push_repo()

        file_keys = [l.file_key() for l in libs]
        common.bulk_remove_files(file_keys)


    def exist(self, lib: LibData):
        if not self.libs:
            return False

        return any(lb == lib for lb in self.libs)

    def find_compatible_libs(self, name: str, ver: str, platform: str, arch=None, build=None):
        libs = []
        if not arch and not build:
            for b in available_build_names():
                for p in available_arches(platform):
                    lib = LibData(name=name, version=ver, platform=platform, arch=p, build=b)
                    if self.exist(lib):
                        libs.append(lib)
        if arch and not build:
            for b in available_build_names():
                lib = LibData(name=name, version=ver, platform=platform, arch=arch, build=b)
                if self.exist(lib):
                    libs.append(lib)
        if not arch and build:
            for p in available_arches(platform):
                lib = LibData(name=name, version=ver, platform=platform, arch=p, build=build)
                if self.exist(lib):
                    libs.append(lib)

        return libs

    def __str__(self):
        def sort_key(lib: LibData):
            return f'{lib.name}-{lib.version}-{lib.platform}-{lib.arch}-{lib.build}'
        sorted_libs = sorted(self.libs, key=sort_key)

        table_headers = ['Name', 'Version', 'Platform', 'Architecture', 'Build']
        table_rows = []
        for l in sorted_libs:
            cells = [l.name, l.version, l.platform, l.arch or '', l.build or '']
            table_rows.append(cells)

        return str(tabulate(table_rows, headers=table_headers))


def update_lib(local_path: str, lib: LibData):
    if not os.path.exists(local_path):
        logger.error(f'Lib path not exit: {local_path}')
        raise Exception('lib path not exist!')

    zip_file_name = lib.get_zip_file_name()
    zip_file_path = os.path.join(local_path, zip_file_name)
    common.zip_dir(local_path, zip_file_path)

    file_key = lib.file_key()
    common.upload_file(zip_file_path, file_key)
    os.remove(zip_file_path)

    repo = LibRepo()
    repo.pull_repo()
    if not repo.exist(lib):
        repo.add_new_lib(lib)


def parse_args():
    description = "Upload your lib to cloud"
    parser = argparse.ArgumentParser(description=description)
    sub_parsers = parser.add_subparsers(dest='sub_command')
    add_parser = sub_parsers.add_parser('add')
    add_parser.add_argument('-p', '--path', help='The library folder you want to upload.', required=True)
    add_parser.add_argument('-n', '--name', help='The library name.', required=True)
    add_parser.add_argument('-v', '--version', help='The library version.')
    add_parser.add_argument('-s', '--platform', help='Platform the library running.', choices=common.available_platforms())
    add_parser.add_argument('-a', '--arch', help='The library architecture.', choices=common.all_available_arches())
    add_parser.add_argument('-b', '--build', help='The library build type.', choices=common.available_build_names())

    remove_parser = sub_parsers.add_parser('remove')
    remove_parser.add_argument('-n', '--name', help='The library name.', required=True)
    remove_parser.add_argument('-v', '--version', help='The library version.')
    remove_parser.add_argument('-s', '--platform', help='Platform the library running.', choices=common.available_platforms())
    remove_parser.add_argument('-a', '--arch', help='The library architecture.', choices=common.all_available_arches())
    remove_parser.add_argument('-b', '--build', help='The library build type.', choices=common.available_build_names())

    return parser.parse_args()


def __strip_or_none(s):
    if not s:
        return None
    s = s.strip()
    return s if s else None


def execute_add(args):
    if not args.path:
        while True:
            path = input("Input the lib local path you want to upload: ")
            if path:
                args.path = path
                break
    if not args.name:
        while True:
            name = input("Input the lib name you want to upload: ")
            if name:
                args.name = name.strip()
                break
    if not args.platform:
        platform = input("Input the platform for the lib you want to upload: ")
        args.platform = platform
    if not args.arch:
        arch = input("Input the architecture for the lib you want to upload: ")
        args.arch = arch
    if not args.build:
        build = input("Input the build type for the lib you want to upload: ")
        args.build = build

    lib_data = LibData(name=args.name, version=__strip_or_none(args.version),
                       platform=__strip_or_none(args.platform),
                       arch=__strip_or_none(args.arch),
                       build=__strip_or_none(args.build))

    lib_repo = LibRepo().pull_repo()
    upload = True
    if lib_repo.exist(lib_data):
        while True:
            override = input("The lib you want to upload has existed in repo. Do you want to override that? yes/no")
            if override == 'yes':
                upload = True
                break
            elif override == 'no':
                upload = False
                break
            else:
                logger.info("Please input yes or no")

    if upload:
        update_lib(args.path, lib_data)


def execute_remove(args):
    lib_repo = LibRepo().pull_repo()
    platform = __strip_or_none(args.platform)
    platforms = [platform] if platform else available_platforms()

    all_libs = []
    for p in platforms:
        libs = lib_repo.find_compatible_libs(name=__strip_or_none(args.name), ver=__strip_or_none(args.version), platform=p, 
                                            arch=__strip_or_none(args.arch), build=__strip_or_none(args.build))
        if libs:
            all_libs.extend(libs)

    lib_repo.bulk_remove_libs(all_libs)
    


def lib_repo():
    args = parse_args()

    if args.sub_command == 'add':
        execute_add(args)
    elif args.sub_command == 'remove':
        execute_remove(args)

    

if __name__ == "__main__":
    lib_repo()


