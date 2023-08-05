from setuptools import find_packages, setup

setup(
    name='geopt',
    version='0.0.2',
    description='',
    long_description='',
    url='https://github.com/DavidePellis/geopt',
    author='Davide Pellis',
    download_url='https://github.com/DavidePellis/geopt/archive/0.0.2.tar.gz',
    author_email='davidepellis@gmail.com',
    packages=find_packages(),
    package_data={'': ['icons/*.png', '*.obj']},
    classifiers=['Development Status :: 1 - Planning'],
    license='MIT',
)
