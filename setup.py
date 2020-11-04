"""
    Setup script for uchart, a tool for managing JRC user charts
"""
import io
import re

from glob import glob
from os.path import abspath, dirname, join, splitext, basename
from setuptools import setup, find_packages

from uchart import __version__

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Atanasov, 2020'

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

setup(
    name='uchart',
    version=__version__,
    license='MIT',
    description="Command line application for managing JRC JAN-7201/9201 user maps.",
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges',
                   re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    long_description_content_type="text/markdown",
    author="Vasil Atanasov",
    author_email="vas.atanasov@gmail.com",
    url='https://github.com/VasAtanasov/uchart-cli.git',
    keywords='userchart furuno jrc converter cli',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    entry_points={
        'console_scripts': [
            'uchart=uchart.app:main'
        ]
    },
    install_requires=[
        "colorlog",
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Utilities',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
