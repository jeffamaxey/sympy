#!/usr/bin/env python3


import os
from os.path import dirname, join, basename, normpath
from os import chdir
import shutil

from helpers import run


ROOTDIR = dirname(dirname(__file__))
DOCSDIR = join(ROOTDIR, 'doc')


def main(version, outputdir):
    os.makedirs(outputdir, exist_ok=True)
    build_html(DOCSDIR, outputdir, version)
    build_latex(DOCSDIR, outputdir, version)


def build_html(docsdir, outputdir, version):
    run('make', 'clean', cwd=docsdir)
    run('make', 'html', cwd=docsdir)

    builddir = join(docsdir, '_build')
    docsname = f'sympy-docs-html-{version}'
    zipname = f'{docsname}.zip'
    cwd = os.getcwd()
    try:
        chdir(builddir)
        shutil.move('html', docsname)
        run('zip', '-9lr', zipname, docsname)
    finally:
        chdir(cwd)
    shutil.move(join(builddir, zipname), join(outputdir, zipname))


def build_latex(docsdir, outputdir, version):
    run('make', 'clean', cwd=docsdir)
    run('make', 'latexpdf', cwd=docsdir)

    srcfilename = f'sympy-{version}.pdf'
    dstfilename = f'sympy-docs-pdf-{version}.pdf'
    src = join('doc', '_build', 'latex', srcfilename)
    dst = join(outputdir, dstfilename)
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
