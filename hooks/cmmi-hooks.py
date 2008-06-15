import os,shutil
def copyto(dest, cplist):
    if not os.path.isdir(dest):
        os.makedirs(dest)
    for file in cplist:
        winext =['.exe', '.dll']
        for ext in winext:
            if os.path.isfile(file+ext):
                file = file + ext
        
        shutil.copy(file, dest)

def bz2(options, buildout):
    compile_dir=options["compile-directory"]
    cwd = os.getcwd()
    os.chdir(compile_dir)

    lib_dest=os.path.join(options['location'], 'lib')
    lib_cplist=['libbz2.a', 'libbz2.def', 'libbz2.dsp', ]
    copyto(lib_dest, lib_cplist)

    bin_dest=os.path.join(options['location'], 'bin')
    bin_cplist=['bzdiff', 'bzip2recover', 'bzip2', 'bzgrep']
    copyto(bin_dest, bin_cplist)

    include_dest=os.path.join(options['location'], 'include')
    include_cplist=['bzlib.h', 'bzlib_private.h']
    copyto(include_dest, include_cplist)
    os.chdir(cwd)

