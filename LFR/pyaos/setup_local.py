#from distutils.core import setup
#from distutils.extension import Extension
from platform import architecture, platform
from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy
import os
import struct
import glob
import sys
import shutil

arch = 'x86'
if struct.calcsize("P")*8 == 64:
    arch = 'x64'

system = 'windows' # 'linux' or 'osx'

vcpkg_triplet = f'{arch}-{system}'

vcpkg_path = os.getenv('VCPKG_ROOT')
assert vcpkg_path is not None, "Could not find vcpkg path! Make sure vcpkg is installed and define its path in an environment variable VCPKG_ROOT"
vcpkg_installed = os.path.join( vcpkg_path, 'installed', vcpkg_triplet )

thirdpartylibs = ["glad", "glfw3", "assimp", "bz2", "zlib", "libpng", "jpeg", "Irrlicht"]
libraries = []
for lb in thirdpartylibs:
    libraries.extend([os.path.splitext(os.path.split(lib)[1])[0] for lib in (glob.glob( os.path.join(vcpkg_installed, "lib",  f'*{lb}*') ))])


#ext = Extension('glesLFR', sources=["glesLFRPyth.pyx","src\glesLFR.cpp","src\LFGenerator.cpp","src\stb_image.cpp","src\glad.c"], language="c++",)

#setup(name="glesLFR", ext_modules = cythonize([ext]),cmdclass = {'build_ext': build_ext})
ext_modules = [
    Extension("pyaos", 
        sources=["pyaos.pyx","../src/AOS.cpp","../src/image.cpp","../src/utils.cpp","../src/gl_utils.cpp"],
        libraries=libraries,
        include_dirs=[numpy.get_include(), "../include", os.path.join(vcpkg_installed, "include")],
        library_dirs=[ os.path.join(vcpkg_installed, "lib")],
        language="c++",
        #extra_compile_args=["-MT"], #<--for static
        #extra_compile_args=["-ggdb", "-lpthread","/INCLUDE:../include/","/link","/LIBPATH:../lib/", "-llibassimp.so","-Wall"]
)
]

def copy_dlls():
    dlls = [ os.path.join(vcpkg_installed, "bin", f'*{lb}*') for lb in thirdpartylibs ]
    dlls.extend( [ os.path.join(vcpkg_installed, "debug", "bin", f'*{lb}*') for lb in thirdpartylibs ] ) # sometimes the debug dlls are also needed!
    print( 'DLLs to copy: ' + str(dlls) )
    for dll in dlls:
        for file in glob.glob(dll):
            shutil.copy(file, os.path.join("..","python"))

package_data = {}
if system == 'windows':
    copy_dlls()
    package_data = {'pyaos': ['*.dll']}


# Building
setup(
    name = "pyaos",
    ext_modules = ext_modules,
    include_dirs=[numpy.get_include(), "../include", os.path.join(vcpkg_installed, "include")],

    #ext_modules = cythonize([ext_modules]),
    cmdclass = {'build_ext': build_ext},
    #include_dirs=[numpy.get_include(),"../include"]
    package_data=package_data, # copy the DLLs in vcpkg/installed/.../bin e.g. assimp*.dll
    script_args = ["build_ext", "--inplace"],
)          

