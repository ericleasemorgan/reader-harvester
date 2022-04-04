from setuptools import setup, find_packages

setup(
    name='reader-harvester',
    packages=find_packages(),
    include_package_data=True,
    entry_points={ 'console_scripts': [ 'hvr = hvr.hvr:hvr' ] }
)