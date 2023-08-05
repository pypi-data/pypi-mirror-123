from setuptools import find_packages, setup
setup(
    name = 'Listreqs',
    version = '0.0.2',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'listreqs = listreqs.__main__:main'
        ]
    })