from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in techno/__init__.py
from techno import __version__ as version

setup(
	name="techno",
	version=version,
	description="Techno",
	author="Ahmed Emam",
	author_email="ahmedemamhatem@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
