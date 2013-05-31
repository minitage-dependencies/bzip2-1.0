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
    try:
        os.chdir(compile_dir)
        VER = options['ver'].strip()
        CVER = VER[:-2]
        uname = os.uname()[0].lower()

        os.environ['CFLAGS'] = os.environ.get('CFlAGS', '') + ' -fPIC'
        for k in ['CFLAGS', 'CPPFLAGS', 'CXXFLAGS']:
            if k in os.environ:
                del os.environ[k]

        def make_install():
            lib_dest=os.path.join(options['location'], 'lib')
            bin_dest=os.path.join(options['location'], 'bin')
            
            lib_cplist=['libbz2.a', 'libbz2.def', 'libbz2.dsp',]
            shared = [f for f in os.listdir('.') if f.startswith('libbz2')]
            lib_cplist.extend(shared)
            copyto(lib_dest, lib_cplist)
            for ext in '.so', '.dylib', '.dll':
                libs = [
                    'libbz2.%s%s' % (VER, ext),
                    'libbz2%s.%s' % (ext, VER),
                ]
                dest = os.path.join(lib_dest, 'libbz2%s' % ext)
                bin_dest = os.path.join(bin_dest, 'libbz2%s' % ext)
                for lib in libs:
                    if (
                        os.path.exists(os.path.join(options['location'], 'lib', lib)) 
                        and not os.path.exists(dest) 
                        and not sys.platform.startswith('win')
                    ):
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
        if uname == 'darwin':
            makefile = open('Makefile-libbz2_so').read()
            makefile = makefile.replace(
                "-soname", 
                "-compatibility_version,%s -Wl,-current_version,%s -Wl,-install_name" % (
                CVER,VER))
            makefile = makefile.replace("libbz2.so.%s"%VER, "libbz2.%s.dylib"%VER)
            makefile = makefile.replace("libbz2.so.%s"%CVER, "libbz2.%s.dylib"%CVER)
            fic = open('Makefile-libbz2_so', 'w')
            fic.write(makefile)
            fic.flush()
            fic.close()
        make_install()
        subprocess.call([options['make-binary'], 'clean'])
        subprocess.call([options['make-binary'], '-f', 'Makefile-libbz2_so'])
        make_install()
    finally:
        os.chdir(cwd)

