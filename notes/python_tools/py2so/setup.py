from distutils.core import setup
from Cython.Build import cythonize


# [] 内是要打包的文件名，可指定多个文件
setup(
    ext_modules=cythonize([
        "src/foo.py",
        "src/bar.py"
    ]),
)
