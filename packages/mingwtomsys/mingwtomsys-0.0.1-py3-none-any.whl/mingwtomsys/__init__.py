import argparse
import json
import os
import subprocess
import copy
import re
from distutils.dir_util import copy_tree
import shutil

APPNAME = 'mingw-to-msys'

MINGW_URL = 'https://github.com/msys2/MINGW-packages.git'
MSYS_URL = 'https://github.com/msys2/MSYS2-packages.git'

"""
Install build tools:

pacman -S --needed base-devel msys2-devel
cd ${package-name}
makepkg

Install package:

pacman -U ${package-name}*.pkg.tar.zst

"""

def makedirs(path):
    try:
        os.makedirs(path)
    except:
        pass

def config_path():
    return os.path.join(os.environ['APPDATA'], APPNAME, 'config.json')

def load_config():
    try:
        with open(config_path(), encoding='utf-8') as f:
            return json.load(f)
    except:
        pass

def save_config(config):
    makedirs(os.path.dirname(config_path()))
    with open(config_path(), 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=1, ensure_ascii=False)

def unquote(txt):
    if len(txt) > 0 and txt[0] == '"' and txt[-1] == '"':
        return txt[1:-1]
    return txt

def unprefix(txt):
    return txt.replace('${MINGW_PACKAGE_PREFIX}-', '')

def get_dependencies(path):
    res = dict()
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    for cat in ['depends', 'makedepends', 'checkdepends']:
        m = re.search('\\b' + cat + '\\s*=\\s*\\(([^)]*)\\)', txt, re.MULTILINE)
        if m:
            res[cat] = [unquote(unprefix(name)) for name in re.split('\\s+', m.group(1)) if not name.startswith('#') and len(name) > 0]
        else:
            res[cat] = []
    return res

def transform_pkgbuild(path, pkgbuild_rev, pkgbuild_relpath):
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    txt = re.sub('\\s*--prefix=\\$\\{MINGW_PREFIX\\}\\s*',' ', txt)
    txt = txt.replace('${MINGW_PREFIX}/bin/python', '/usr/bin/python')
    txt = txt.replace('${MINGW_PACKAGE_PREFIX}-', '')
    txt = txt.replace('mingw-w64-', '')
    txt = re.sub("arch=\\([^)]*\\)", "arch=('i686' 'x86_64')", txt)
    txt = re.sub('mingw_arch=\\([^)]*\\)\\s*', '', txt)
    txt = re.sub('pkgrel=[0-9]+','pkgrel=1', txt)
    txt = txt.replace('${MINGW_PREFIX}', '')
    txt = "# converted with {} from {} {}\n".format(APPNAME, "MINGW-packages/{}".format(pkgbuild_relpath), "https://github.com/msys2/MINGW-packages/blob/{}/{}".format(pkgbuild_rev, pkgbuild_relpath)) + txt
    with open(path, 'wb') as f:
        f.write(txt.replace('\r\n','\n').encode('utf-8'))

def get_head_rev(path):
    return subprocess.check_output(['git','rev-parse', 'HEAD'], cwd=path).decode('utf-8').strip()

def mingw_pgkbuild_path(config, p):
    return os.path.join(config['mingw'], 'mingw-w64-{}'.format(p), 'PKGBUILD')

def mingw_package_path(config, p):
    return os.path.dirname(mingw_pgkbuild_path(config, p))

def main():
        
    parser = argparse.ArgumentParser(prog=APPNAME)

    parser.add_argument('command', choices={'deps', 'dependencies', 'clone', 'convert', 'graph', 'open', 'view'})

    parser.add_argument('--mingw', help='path to mingw packages')
    parser.add_argument('--msys', help='path to msys packages')
    parser.add_argument('--output', '-o', help='directory to save output')

    parser.add_argument('--skip-check', action='store_true', help='skip checkdepends on building dependency graph')
    parser.add_argument('--skip-packages', nargs='+', help='list of packages to skip on building dependency graph')

    parser.add_argument('--packages','--package','-p', nargs='+')

    #makedirs(os.path.dirname(config_path()))

    args = parser.parse_args()
    #print(args)

    config = load_config()
    if config is None:
        config = dict()
    
    if 'msys' not in config:
        config['msys'] = None
    if 'mingw' not in config:
        config['mingw'] = None
    
    orig_config = copy.copy(config)
    
    mingw = args.mingw
    msys = args.msys
    output = args.output
    command = args.command
    packages = args.packages
    skip_packages = args.skip_packages
    if skip_packages is None:
        skip_packages = []
    
    if command in ['clone']:
        if output is None:
            print("Specify output directory")
            exit(1)
        if shutil.which('git') is None:
            print('Cannot find git')
            exit(1)
        subprocess.run(['git','clone', MINGW_URL], cwd=output)
        subprocess.run(['git','clone', MSYS_URL], cwd=output)
        msys = os.path.join(output, 'MSYS2-packages')
        mingw = os.path.join(output, 'MINGW-packages')

    if mingw:
        config['mingw'] = mingw

    if msys:
        config['msys'] = msys

    if orig_config != config:
        save_config(config)

    if config['mingw'] is None:
        print("specify path to mingw packages")
        exit(1)

    if config['msys'] is None:
        print("specify path to msys packages")
        exit(1)
    
    if command in ['deps', 'dependencies']:
        for p in packages:
            #path = os.path.join(config['mingw'], 'mingw-w64-{}'.format(p), 'PKGBUILD')
            path = mingw_pgkbuild_path(config, p)
            deps = get_dependencies(path)
            print(p)
            for k,v in deps.items():
                print(k, v)
    
    if command in ['convert']:
        if output is None:
            print("specify output directory")
            exit(1)
        for p in packages:
            src = mingw_package_path(config, p)
            dst = os.path.join(output, p)
            copy_tree(src, dst)
            path = os.path.join(output, p, 'PKGBUILD')

            pkgbuild_rev = get_head_rev(config['mingw'])
            pkgbuild_relpath = os.path.join('mingw-w64-{}'.format(p), 'PKGBUILD').replace('\\','/')

            transform_pkgbuild(path, pkgbuild_rev, pkgbuild_relpath)
            print("{} converted to {}".format(src, dst))

    if command in ['graph']:
        res = dict()
        
        queue = packages[:]
        while len(queue) > 0:
            p = queue[0]
            queue = queue[1:]
            if p in skip_packages:
                continue
            if p in res:
                continue
            res[p] = []
            path = mingw_pgkbuild_path(config, p)
            if not os.path.isfile(path):
                continue
            #print(p)
            deps = get_dependencies(path)
            #print(deps)
            
            for k in ['depends', 'makedepends', 'checkdepends']:
                if k == 'checkdepends' and args.skip_check:
                    continue
                res[p] += deps[k]
                queue += deps[k]
        txt = ""
        for k, deps in res.items():
            txt += "".join(['  "{}" -> "{}";\n'.format(k, v) for v in deps if k not in skip_packages and v not in skip_packages])
        #print(txt)
        txt = "digraph G {\n" + txt + "}\n"
        print(txt)

    if command in ['open', 'view']:
        p = packages[0]
        path = mingw_pgkbuild_path(config, p)
        editor = os.environ.get('EDITOR')
        if editor is None:
            editor = 'vim'
        if editor == 'code':
            command = ['code','-r', path]
        else:
            command = [editor, path]
        #print(command)
        subprocess.run(command)

if __name__ == '__main__':
    main()
