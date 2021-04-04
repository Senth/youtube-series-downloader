from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="youtube-series-downloader",
    use_scm_version=True,
    url="https://github.com/Senth/youtube-series-downloader",
    license="MIT",
    author="Matteus Magnusson",
    author_email="senth.wallace@gmail.com",
    description="Downloads YouTube series and optionally speeds them up to be watched on TVs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["youtube_series_downloader"],
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
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
)
