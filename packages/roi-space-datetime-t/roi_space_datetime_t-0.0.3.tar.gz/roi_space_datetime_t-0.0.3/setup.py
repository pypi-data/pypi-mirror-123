import setuptools
from setuptools import setup, find_packages

# 版本信息
version = '0.0.3'

# 描述信息
long_description = ""
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()
# setup
setup(
    name="roi_space_datetime_t",
    version=version,
    description="roi_space_datetime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['roi_space_datetime'],
    license='MIT',
    python_requires='>=3.5',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
