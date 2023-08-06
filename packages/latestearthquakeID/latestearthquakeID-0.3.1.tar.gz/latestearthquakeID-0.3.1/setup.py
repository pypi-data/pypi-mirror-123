"""
https://packaging.python.org/tutorials/packaging-projects/
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latestearthquakeID",
    version="0.3.1",
    author="Dinda Wahyu Candradewa",
    author_email="candradewa1981@gmail.com",
    description="this package will get the latest earthquake from BMKG | Meteorological, Climatological, and Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Candyy1st/latest-indonesia-earthquake",
    project_urls={
        "Bug Tracker": "https://github.com/Candyy1st/latest-indonesia-earthquake/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
