# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
import hashlib
import json
import os
import shutil
import sys
import zipfile
from uuid import uuid4
from pkg_resources import parse_version as get_version
from a28 import log, utils


# try import the requests module
try:
    import requests
except ImportError:
    log.fatal('the requests module is required, please pip install requests')
    sys.exit(1)


def options(mainparser):
    """Argparse options added to the cli."""
    parser = mainparser.add_parser(
        'package',
        aliases=['pkg'],
        help='package actions'
    )
    subparser = parser.add_subparsers(
        dest='package',
        required=True,
        help='package',
    )
    parser_init = subparser.add_parser(
        'init',
        help='Initialize a package',
    )
    parser_init.set_defaults(func=initialize)
    parser_init.add_argument(
        'path',
        default='.',
        help='package path default \'.\'',
    )
    parser_init.add_argument(
        '-s',
        '--scope',
        required=True,
        help='package scope eg. group-name',
    )
    parser_init.add_argument(
        '-n',
        '--name',
        required=True,
        help='package mnamespace eg. pkg-name',
    )
    parser_init.add_argument(
        '-t',
        '--type',
        required=True,
        choices=[
            'api', 'app', 'chat', 'event',
            'interface', 'logger', 'metadata',
            'preference', 'realtime', 'repository',
            'ui', 'units'
        ],
        help='package type',
    )
    parser_init.add_argument(
        '--bin',
        action='store_true',
        help='create the bin directory',
    )
    parser_init.add_argument(
        '--script',
        action='store_true',
        help='create the scripts directory',
    )
    parser_init.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force overwriting package.json',
    )
    parser_build = subparser.add_parser(
        'build',
        help='build package',
    )
    parser_build.set_defaults(func=build)
    parser_build.add_argument(
        '--src',
        required=True,
        help='package source directory',
    )
    parser_build.add_argument(
        '--dest',
        default='',
        help='destination directory',
    )
    parser_install = subparser.add_parser(
        'install',
        help='install package',
    )
    parser_install.set_defaults(func=install)
    parser_install.add_argument(
        '--pkg',
        required=True,
        help='package a28 package file',
    )


def initialize(args):
    """Initialize a package in a specified directory."""
    (path, name, scope, schema) = _get_init_args(args)
    log.info(f'initializing @{scope}/{name} in {path}')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    subdirs = ['extensions', 'plugins']
    json_file = os.path.join(path, 'package.json')
    exists = os.path.isfile(json_file)
    description = f'{schema} package created using the A28 command by {scope}.'
    json_data = {
        'name': f'@{scope}/{name}',
        'description': description,
        'version': '0.1.0',
    }

    if args.bin:
        log.debug('adding bin')
        subdirs.append('bin')
        json_data['bin'] = {}
    if args.script:
        log.debug('adding scripts')
        subdirs.append('script')
        json_data['scripts'] = {}
    if args.type == 'application':
        subdirs.append('plugin')
    _build_structure(path, subdirs)
    message = 'overwrite package.json?'
    if not exists or args.force or utils.confirm(message):
        log.info('creating package.json')
        with open(json_file, 'w') as pkg_file:
            json.dump(json_data, pkg_file, indent=4)
    else:
        log.info('not overwriting package.json')


def build(args):
    """Build package."""
    src = args.src
    dest = args.dest
    meta = get_info(src)
    pkg = package(src, dest, meta)
    utils.message(pkg)


def install(args):
    """install / update the local package."""
    pkg_hash = generate_hash(args.pkg)
    meta = extract_meta(args.pkg)
    meta['hash'] = pkg_hash
    install_local(args.pkg, meta)
    utils.message('installed {}'.format(meta['name']))


def extract_meta(pkg):
    """Extract the meta information from a packaged package."""
    with zipfile.ZipFile(pkg, 'r') as zf:
        package = next(x for x in zf.namelist() if x.endswith('package.json'))
        with zf.open(package) as index:
            return get_info(index, True)


def get_info(src, extracted=False):
    """Get information about a package by using a combination of the data in
    the src package.json file and the index.json file if available.
    """
    if extracted:
        data = json.load(src)
    else:
        package = os.path.join(src, 'package.json')
        with open(package) as package_data:
            data = json.load(package_data)

    # load the index data
    index = os.path.join(utils.STORAGE, 'index.json')
    with open(index) as index_data:
        i_data = json.load(index_data)

    # copy data from the index package if exists
    if data['name'] in i_data['packages']:
        i_package = i_data['packages'][data['name']]
        data['identifier'] = i_package['identifier']
    else:
        data['identifier'] = str(uuid4())
    return data


def install_local(pkg, meta):
    """Install a package locally by calling the
    update_index function."""
    dest = os.path.join(utils.STORAGE, 'cache')
    shutil.copy(pkg, dest)
    index = os.path.join(utils.STORAGE, 'index.json')
    with open(index, 'r+') as index_data:
        update_index(index_data, meta)


def update_index(index_data, meta):
    '''Updates the index.json without touching the etag.json file.
    This will be overwritten when a new official index.json
    is published.'''
    data = json.load(index_data)
    data['packages'][meta['name']] = meta
    if meta['name'] not in data['required']:
        data['required'].append(meta['name'])
    index_data.seek(0)
    json.dump(data, index_data, indent=4)
    index_data.truncate()


def package(src, dest, meta):
    """Build an a28 package from the provided src directory. The package will
    be saved to the dest directory. A package needs to be provided containing
    at least an identifier and a version number."""
    version = meta['version']
    identifier = meta['identifier']
    filename = '{}-{}.{}'.format(identifier, version, 'a28')
    filename = os.path.join(dest, filename)

    if not os.path.exists(dest):
        os.makedirs(dest)

    a28 = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    exclude = (['build', '.vscode'])
    for root, dirs, files in os.walk(src, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for current in files:
            i_file = os.path.join(root, current)
            fl = os.path.relpath(
                os.path.join(root, current),
                os.path.join(src, '..', '..'),
            )
            a28.write(i_file, fl)
    a28.close()
    return filename


def fetch(url='https://packages.a28.io/index.json', dest=None):
    """Fetch the index from it's online source."""
    etag = os.path.join(utils.STORAGE, 'index.etag')
    request = requests.head(url, allow_redirects=True)
    latest = request.headers['ETag']
    request.close()

    with open(etag, 'w+') as file:
        current = file.read().replace('\n', '')
        if get_version(latest) > get_version(current):
            file.write(latest)
            request = requests.get(url, allow_redirects=True)
            with open(dest, 'wb') as index:
                index.write(request.content)
            request.close()


def generate_hash(pkg):
    """Generate a hash for a package."""
    sha256_hash = hashlib.sha256()
    with open(pkg, 'rb') as f:
        # read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def prebuild(src):
    """Execute any pre-build scripts. Usually used to create installable
    tarballs for applications.
    """


def _get_init_args(args):
    path = os.path.realpath(args.path)
    if not utils.valid_string(args.name):
        raise ValueError(f'{args.name} is not a valid name')
    name = args.name.lower()
    if not utils.valid_string(args.scope):
        raise ValueError(f'{args.scope} is not a valid scope')
    scope = args.scope.lower()
    if not utils.valid_string(args.type, min_length=2):
        raise ValueError(f'{args.type} is not a valid name')
    schema = args.type.lower()
    return (path, name, scope, schema)


def _build_structure(path, subdirs):
    for subdir in subdirs:
        os.makedirs(os.path.join(path, subdir), exist_ok=True)
