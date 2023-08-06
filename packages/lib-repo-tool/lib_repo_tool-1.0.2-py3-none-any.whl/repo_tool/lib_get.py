import argparse

import oss2
import os
import json
import zipfile
import shutil

from . import common
from .lib_repo import LibRepo, LibData

from .common import get_bucket, zip_dir, unzip_file, upload_file, download_file, OSS_BASE_PATH, get_lib_zip_file_name, get_lib_zip_file_key, get_platform_name, available_build_names, available_arches

import logging
logger = logging.getLogger(__name__)

DEPENDENCY_JSON_FILE_NAME = 'dependencies.json'


def get_default_dep_path():
    return os.path.join(os.getcwd(), DEPENDENCY_JSON_FILE_NAME)


def get_dep(dep_path):
    with open(dep_path, 'r') as f:
        return json.load(f)


def download_lib(lib_data: LibData, to_path: str):
    file_key = lib_data.file_key()
    _, zip_name = os.path.split(file_key)
    local_path = lib_data.gen_path()
    local_path = os.path.join(to_path, local_path)
    if os.path.exists(local_path):
        print(f'[warning] {local_path} already exist.')
        return

    zip_file = os.path.join(local_path, zip_name)

    os.makedirs(local_path)
    download_file(file_key, zip_file)

    unzip_file(zip_file, local_path)
    os.remove(zip_file)


def parse_args():
    description = "Download dependencies lib."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--platform', help='Platform', choices=common.available_platforms())
    parser.add_argument('--arch', help='Lib architecture', choices=common.all_available_arches())
    parser.add_argument('--build', help='Lib build type', choices=common.available_build_names())
    parser.add_argument('--dep', help='The dependencies json file in which the libs will be download from lib repo')
    parser.add_argument('--dest', help='Where download the libs to')

    sub_parsers = parser.add_subparsers(dest='sub_command')
    list_parser = sub_parsers.add_parser('list')

    return parser.parse_args()


def list_command(args):
    print(str(LibRepo().pull_repo()))


def lib_get():
    args = parse_args()

    if args.sub_command == 'list':
        return list_command(args)

    def strip(s):
        return s.strip() if s else None

    if not args.dep:
        args.dep = get_default_dep_path()
    if not args.dest:
        args.dest, _ = os.path.split(args.dep)
    if not args.platform:
        args.platform = get_platform_name()

    deps = get_dep(args.dep)
    libs = []
    repo = LibRepo().pull_repo()

    platform = strip(args.platform)
    arch = strip(args.arch)
    build = strip(args.build)
    for name, ver in deps.items():
        name = strip(name)
        ver = strip(ver)
        lib = LibData(name=name, version=ver, platform=platform, arch=arch, build=build)
        if repo.exist(lib):
            libs.append(lib)
            continue

        compatible_libs = repo.find_compatible_libs(name, ver, platform, arch, build)
        if compatible_libs:
            libs.extend(compatible_libs)
        else:
            print(f'[error] can not find lib from repo. name: {name}, version: {ver}, platform: {platform}, architecture: {arch}, build: {build}')

    for lib in libs:
        download_lib(lib, args.dest)


if __name__ == '__main__':
    lib_get()
