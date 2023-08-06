import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='auth3',
    packages=find_packages(),
    version='1.0.1',
    description='Official SDK to use the Auth3.dev Identity Platform API',
    url="https://auth3.dev/",
    project_urls={
        "Bug Tracker": "https://github.com/auth3-dev/python-sdk/issues",
    },
    long_description=README,
    long_description_content_type="text/markdown",
    author='Auth3.dev',
    license='Apache-2.0',
    include_package_data=True,
    install_requires = [
        "grpcio>=1.37.1",
        "protobuf",
    ]
)