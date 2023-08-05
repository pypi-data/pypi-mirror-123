"""Setup package"""

from setuptools import setup, find_packages  # type: ignore

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="pescea",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="1.0.10",
    license="gpl-3.0",
    description="A python interface to the Escea fireplace controllers",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Laz Davila",
    author_email="laz.davila@gmail.com",
    url="https://github.com/lazdavila/pescea",
    download_url="https://github.com/lazdavila/pescea/archive/refs/tags/v1.0.10.tar.gz",
    keywords=[
        "Escea",
        "IoT",
    ],
    python_requires=">=3.7",
    tests_require=["pytest"],
    install_requires=[
        "asyncio",
        "async_timeout",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Home Automation",
        "Topic :: System :: Hardware",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: " "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
