import setuptools
from pathlib import Path

def read(rel_path):
	path = Path(__file__).parent.resolve()
	return open(path.joinpath(rel_path)).read()

def get_version(rel_path):
	for line in read(rel_path).splitlines():
		if line.startswith('__version__'):
			delim = '"' if '"' in line else "'"
			return line.split(delim)[1]
	else:
		raise RuntimeError('Unable to find version string')

with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pgeng',
	version=get_version('pgeng/__init__.py'),
	author='Qamynn',
	description='Useful functions and classes for PyGame',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Qamynn/pgeng',
	license='MIT',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	packages=['pgeng', 'pgeng.vfx'],
	include_package_data=True,
	install_requires=['pygame>=2'],
	python_requires='>=3.6',
)
