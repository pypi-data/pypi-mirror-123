from os import chdir, pardir
from os.path import join, exists, dirname, normpath, abspath
from setuptools import find_packages, setup

reqs_default = join(dirname(__file__), "requirements.txt")
required = []

if exists(reqs_default):
    with open(reqs_default) as f:
        required += f.read().splitlines()

with open(join(dirname(__file__), "README.md")) as f:
    long_desc = f.read()

# Allow setup.py to be run from any path
chdir(normpath(join(abspath(__file__), pardir)))

setup(
    name="iot-ccm-config-builder",
    version="1.0.0",
    description="A tool to build config files for the IOT CCM SDK project",
    long_description=long_desc,
    author="NIST IT Lab",
    author_email="itl_inquiries@nist.gov",
    url="https://gitlab.com/prometheuscomputing/nist-ssd-iot-testbed/iot-ccm-config-builder",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
)
