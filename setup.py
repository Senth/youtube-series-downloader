from setuptools import find_packages
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="youtube-series-downloader",
    version="1.0.0",
    url="https://github.com/Senth/youtube-series-downloader",
    license="MIT",
    author="Matteus Magnusson",
    author_email="senth.wallace@gmail.com",
    description="Downloads YouTube series and optionally speeds them up to be watched on TVs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "config")),
    entry_points={
        "console_scripts": [
            "youtube-series-downloader=youtube_series_downloader.__main__:__main__",
        ],
    },
    include_package_data=True,
    data_files=[
        ("config/youtube-series-downloader", ["config/config.example.py"]),
    ],
    install_requires=["requests", "apscheduler", "youtube-dl"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
