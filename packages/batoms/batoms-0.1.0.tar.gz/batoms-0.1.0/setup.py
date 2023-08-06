import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="batoms",
    version="0.1.0",
    description="Drawing and rendering beautiful atoms, molecules using Blender.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/superstar54/batoms",
    author="Xing Wang",
    author_email="xingwang1991@gmail.com",
    license="GPL",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3.9",
    ],
    packages=["batoms"],
    entry_points={'console_scripts': ['batoms=batoms.cli.main:main']},
    install_requires=["ase", "numpy", "scipy", "scikit-image"],
    python_requires='>=3.9',
)
