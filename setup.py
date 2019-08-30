"""Install pycql."""

from setuptools import find_packages, setup
import os
import os.path

# don't install dependencies when building win readthedocs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# get version number
# from https://github.com/mapbox/rasterio/blob/master/setup.py#L55
with open(os.path.join(__file__, 'pycql/__init__.py')) as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

# use README.md for project long_description
with open('README.md') as f:
    readme = f.read()


def parse_requirements(file):
    return sorted(set(
        line.partition('#')[0].strip()
        for line in open(os.path.join(os.path.dirname(__file__), file))
    ) - set(''))

setup(
    name='pycql',
    version=version,
    description='CQL parser for Python',
    long_description=readme,
    author='Fabian Schindler',
    author_email='fabian.schindler@gmail.com',
    url='https://github.com/constantinius/pycql',  # TODO
    license='MIT',
    packages=find_packages(),
    package_dir={'static': 'static'},
    package_data={'.static': ['*']}, # TODO
    install_requires=parse_requirements('requirements.txt') if not on_rtd else [],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=['pytest']
)
