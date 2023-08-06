from setuptools import setup
import re

# get setup.py long_description for pypi
with open("DESCRIPTION.md", "r", encoding="utf-8") as file:
    long_description = file.read().splitlines()
    
# get requirements
with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = file.read()
    
# get property from __init__.py file (like __version__)
# Kudos to https://stackoverflow.com/a/41110107/8082249
# for making this simple. I hate creating regex expresions...
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

# get properties from __init__.py
# check there for the value to these properties
project_dir = "feathery"
__name__ = get_property("__name__", project_dir)
__version__ = get_property("__version__", project_dir)
__author__ = get_property("__author__", project_dir)
__url__ = get_property("__url__", project_dir)
__description__ = get_property("__description__", project_dir)

# setup method call
setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    author=__author__,
    url=__url__,
    packages=['feathery'],
    include_package_data=True,
)