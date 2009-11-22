import os,shutil
import sys

import subprocess

def copyto(dest, cplist):
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for file in cplist:
        winext =['.exe', '.dll']
        for ext in winext:
            if os.path.isfile(file+ext):
                file = file + ext

        if os.path.exists(file):
            shutil.copy(file, dest)

#def bz2(options, buildout), *a, **kw):
def bz2(options, buildout):
    compile_dir=options["compile-directory"]
    cwd = os.getcwd()
    os.chdir(compile_dir)

    os.environ['CFLAGS'] = os.environ.get('CFlAGS', '') + ' -fPIC'
    for k in ['CFLAGS', 'CPPFLAGS', 'CXXFLAGS']:
        if k in os.environ:
            del os.environ[k]

    def make_install():
        lib_dest=os.path.join(options['location'], 'lib')
        bin_dest=os.path.join(options['location'], 'bin')
        
        lib_cplist=['libbz2.a', 'libbz2.def', 'libbz2.dsp', ]
        shared = [f for f in os.listdir('.') if f.startswith('libbz2')]
        lib_cplist.extend(shared)
        copyto(lib_dest, lib_cplist)
        for ext in '.so', '.dll', '.dylib':
            lib = 'libbz2%s.1.0.4' % ext
            dest = os.path.join(lib_dest, 'libbz2%s' % ext)
            bin_dest = os.path.join(bin_dest, 'libbz2%s' % ext)
            if os.path.exists(lib) and not os.path.exists(dest) and not sys.platform.startswith('win'):
                os.symlink(lib, dest)
            if os.path.exists(lib) and sys.platform.startswith('win'):
                shutil.copy2(lib, dest)
                shutil.copy2(lib, bin_dest)
                shutil.copy2(lib, '%s.dll' % dest.replace('.so', ''))
                shutil.copy2(lib, '%s.dll' % bin_dest.replace('.so', ''))
                shutil.copy2(lib, '%s-1.0.4.dll' % dest.replace('.so', ''))
                shutil.copy2(lib, '%s-1.0.4.dll' % bin_dest.replace('.so', ''))
                shutil.copy2(lib, '%s-1.0.dll' % dest.replace('.so', ''))
                shutil.copy2(lib, '%s-1.0.dll' % bin_dest.replace('.so', ''))
                

        bin_dest=os.path.join(options['location'], 'bin')
        bin_cplist=['bzdiff', 'bzip2recover', 'bzip2', 'bzgrep', 'bzip2-shared']
        copyto(bin_dest, bin_cplist)
        include_dest=os.path.join(options['location'], 'include')
        include_cplist=['bzlib.h', 'bzlib_private.h']
        copyto(include_dest, include_cplist)


    make_install()

    if not sys.platform == 'darwin':
        subprocess.call([options['make-binary'], 'clean'])
        subprocess.call([options['make-binary'], '-f', 'Makefile-libbz2_so'])
        #if sys.platform.startswith('win'):
        #    subprocess.call([options['make-binary'], '-f', 'makefile.msc'])
        make_install()

    os.chdir(cwd)

