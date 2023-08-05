"""Setup.py for DB2 custom Airflow provider package."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow_provider_db2 setup."""
setup(
    name='airflow_provider_db2',
    version="0.0.2",
    description='A provider package built by AIOPS IBM team',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
    "apache_airflow_provider": [
        "provider_info=airflow_provider_db2.__init__:get_provider_info"
          ]
      },
    license='Apache License 2.0',
    packages=['airflow_provider_db2', 'airflow_provider_db2.hooks'],
    install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='Fernanda Milagres',
    author_email='fernandamilagres@gmail.com',
    python_requires='~=3.7',
)