from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='Finstein',
    packages=find_packages(include=['Finstein']),
    version='3.2',
    description='A library for finacial calculations',
    author='Abhiraj Mengade',
    license='MIT',
    install_requires=['scipy','numpy'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=[],
    tests_require=[],
    test_suite='Tests',
)