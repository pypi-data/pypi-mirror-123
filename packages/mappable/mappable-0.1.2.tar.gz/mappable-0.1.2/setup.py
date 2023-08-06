from setuptools import setup, find_packages


VERSION = {}
# version.py defines VERSION and VERSION_SHORT variables.
# We use exec here to read it so that we don't import mappable
# whilst setting up the package.
with open("mappable/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="mappable",
    version=VERSION["VERSION"],
    url="https://mappable.ai/",
    author="Mark Neumann",
    author_email="mark.neumann.1992@gmail.com",
    description="An interactive data annotation tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["annotation data text machine learning"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    license="Unlicensed",
    install_requires=[
        "pandas",
        "fastapi",
        "uvicorn",
        "aiofiles",
        "numpy",
        "typer",
        "sqlite-utils",
    ],
    entry_points={"console_scripts": ["mappable=mappable.__main__:cli"]},
    include_package_data=True,
    python_requires=">=3.6.0",
)
