from setuptools import setup, find_packages

setup(
    name="travelplanner",
    version="0.0.0",
    author="Mubarak Youssouf",
    install_requires=['numpy', 'matplotlib', 'pytest'],
    packages=find_packages(exclude=['*test']),
    entry_points={
        'console_scripts': [
         'bussimula = travelplanner.command:main'
        ]
    }


)
