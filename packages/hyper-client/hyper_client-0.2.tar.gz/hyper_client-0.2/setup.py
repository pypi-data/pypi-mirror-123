import os
import sys
from setuptools import find_packages, setup

project = "hyper_client"

number_of_arguments = len(sys.argv)
version_parameter = sys.argv[-1]
version = version_parameter.split("=")[1]
sys.argv = sys.argv[0 : number_of_arguments - 1]

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, "requirements.txt")) as f:
    requirements = f.readlines()

setup(
    name=project,
    version=version,
    description="Snark Hyper Client",
    author="Activeloop",
    author_email="support@activeloop.ai",
    url="https://github.com/activeloopai/hyper",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords="activeloop-hyper",
    python_requires=">=3",
    install_requires=[],
    setup_requires=[],
    dependency_links=[],
    tests_require=[
        "pytest",
        "mock>=1.0.1",
    ],
)
