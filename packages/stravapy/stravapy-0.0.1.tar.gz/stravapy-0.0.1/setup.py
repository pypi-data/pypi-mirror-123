from setuptools import find_packages, setup

setup(
    name='stravapy',
    packages=find_packages(include=['stravapy']),
    version='0.0.1',
    description='Basic Strava GPX Reader',
    author='DWin',
    url = 'https://github.com/user/reponame',
    license='MIT',
    install_requires=['lxml']
)