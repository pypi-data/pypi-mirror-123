from setuptools import setup, find_packages

dependencies = [ "vcstools-latest" ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bughotspots",
    version="0.5",
    packages=find_packages(),
    install_requires=dependencies,
    author="Punit Goswami",
    description="A Python based implementation of the bug prediction algorithm proposed by Google",
    keywords="bughotspot bug spots bug prediction",
    long_description=long_description,
    url='https://github.com/pntgoswami18/python-bugspots',
    long_description_content_type="text/markdown",
    include_package_data=True,
    license="BSD",
    entry_points={
	'console_scripts' : [
		'bughotspots = bughotspots:main'
	]
    },

    classifiers=['Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Operating System :: Unix ']
)
