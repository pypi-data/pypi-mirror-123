from setuptools import setup, find_packages

setup(
    author="Barry Howard",
    author_email="barry.howard@ge.com",
    description="Python Library for communicating with vault server.",
    keywords=['vault', 'ge', 'cloudops'],
    long_description="Python Library for communicating with GE vault server.",
    name="gevault",
    scripts=['./gevault'],
    url="https://github.build.ge.com/Cloudpod/vault",
    version="1.2.1634196758",
    packages=find_packages(exclude=["build", "build/*"])
)
