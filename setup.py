from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in lens/__init__.py
from lens import __version__ as version

setup(
	name="lens",
	version=version,
	description="LMNAs ExperieNce Suite",
	author="LMNAs Cloud Solutions LLP",
	author_email="hello@lmnas.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
