import json

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("clio/version.json") as fp:
    _info = json.load(fp)

setup(
    name="syneto-clio",
    version=_info["version"],
    author="Alexandra Veres",
    author_email="alexandra.veres@syneto.eu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["clio", "clio.kube", "clio.prerequisites"],
    include_package_data=True,
    install_requires=["Click"],
    entry_points={"console_scripts": ["syneto-clio=clio.syneto_clio:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
