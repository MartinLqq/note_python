from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mygit',  # Required
    version='0.0.1',  # Required
    author='Example Author',
    author_email='author@example.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',  # text/plain, text/x-rst
    url='https://github.com/pypa/sampleproject',
    keywords='example',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.5',  # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    install_requires=['requests'],  # https://packaging.python.org/en/latest/requirements.html
    extras_require={  # pip install example-pkg[dev]
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data = {
                   'mygit': ['package_data.dat'],
               },
    data_files=[('my_data', ['data/data_file'])],
    entry_points={  # provide a command called `example_pkg` which executes the function `main`
        'console_scripts': [
            'mygit=mygit:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)