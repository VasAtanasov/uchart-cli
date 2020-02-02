from os.path import abspath, dirname, join

from setuptools import setup, find_packages

from uchart import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='uchart',
    version=__version__,
    license='MIT',
    py_module=['uchart'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'uchart=uchart.core:main'
        ]
    },
    install_requires=[
        "colorlog",
    ],
    description="Command line application for mapping JRC JAN-7201/9201 user map to Furuno user map.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vasil Atanasov",
    author_email="vas.atanasov@gmail.com",
    keywords='userchart furuno jrc converter cli',
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
)