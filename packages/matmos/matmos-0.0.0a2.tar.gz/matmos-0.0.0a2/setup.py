import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matmos",
    version="0.0.0.a2",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Library of atmospheric models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonlopezr/matmos",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "Python-Alexandria>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
