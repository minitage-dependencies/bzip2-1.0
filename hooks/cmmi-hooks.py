import os,shutil
def copyto(dest, cplist):
    if not os.path.isdir(dest):
        os.mkdir(dest)
    for file in cplist:
        shutil.copy(file, dest)

def bz2(options,buildout):
    compile_dir=options["compile-directory"]
    if os.path.isdir(compile_dir):
        contents = os.listdir(compile_dir)
        if len(contents) == 1:
            os.chdir(compile_dir)
            os.chdir(contents[0])

    lib_dest=options['location']+"/lib"
    lib_cplist=['libbz2.a', 'libbz2.def', 'libbz2.dsp', ]
    copyto(lib_dest,lib_cplist)

    bin_dest=options['location']+"/bin"
    bin_cplist=['bzdiff', 'bzip2recover', 'bzip2', 'bzgrep']
    copyto(bin_dest,bin_cplist)

    include_dest=options['location']+"/include"
    include_cplist=['bzlib.h', 'bzlib_private.h']
    copyto(include_dest,include_cplist)

