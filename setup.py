from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

module_name = "youtube_series_downloader"
project_slug = "youtube-series-downloader"

setup(
    name=project_slug,
    use_scm_version=True,
    url="https://github.com/Senth/youtube-series-downloader",
    license="MIT",
    author="Matteus Magnusson",
    author_email="senth.wallace@gmail.com",
    description="Downloads YouTube series and optionally speeds them up to be watched on TVs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            f"{project_slug}={module_name}.__main__:main",
        ],
    },
    include_package_data=True,
    data_files=[
        ("config", [f"config/{project_slug}-example.cfg"]),
    ],
    install_requires=[
        "apscheduler==3.7.0",
        "blulib==0.1.0",
        "requests==2.22.0",
        "tealprint==0.1.0",
        "youtube-dl",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
)
