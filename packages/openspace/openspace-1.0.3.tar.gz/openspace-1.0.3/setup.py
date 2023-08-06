#!/usr/bin/env python

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name="openspace",
	version="1.0.3",
	python_requires='>3.8.0',
	description="Public package for various space operations applications",
	long_description=long_description,
	author="Brandon Sexton",
	author_email="brandon.sexton.1@outlook.com",
	entry_points={'console_scripts': ['openspace=openspace.geoplanner:run',
	'reach_demo=openspace.reach_demo:run',
	'joystick=openspace.joystick:run',
	'sda_demo=openspace.sda_demo:run']},
	packages=find_packages(),
	include_package_data=True,
	install_requires=[]
	)
