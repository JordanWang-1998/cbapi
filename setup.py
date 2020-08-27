from setuptools import setup, find_packages

setup(
    name = "cbapi",
    packages=["cbapi"],
    version = "1.0.0",
    url = "https://github.com/JordanWang-1998/CrunchbaseAPI",
    author = "Jordan Wang",
    author_email = "Junhan.Wang@baruchmail.cuny.edu",
    packages = find_packages(),
    install_requires = ["pandas","requests"],
    description = "An API library to allow downloading / querying organization / people data from Crunchbase",
    long_description=open('README.md').read(),
)
