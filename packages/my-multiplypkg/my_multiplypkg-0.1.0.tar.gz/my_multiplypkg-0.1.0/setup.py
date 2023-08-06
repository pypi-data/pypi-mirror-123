from setuptools import setup, find_packages

setup(
    name='my_multiplypkg',
    version='0.1.0',
    description='My first Python library for multiplication',
    author='Me',
    license='MIT',
    packages=["my_multiplypkg"],
    include_package_data=True,
    install_requires=[],
)