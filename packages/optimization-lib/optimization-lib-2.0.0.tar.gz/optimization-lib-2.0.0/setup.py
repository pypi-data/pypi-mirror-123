from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='optimization-lib',
    version='2.0.0',  # connect this to git tags version or release version
    author='Ty Crabtree',
    description='Measures program speed',
    long_description_content_type="text/markdown",
    long_description=long_description,
    scripts=[
        'optimization/optimization.py',
    ],
    python_requires='>=3.6',

)
