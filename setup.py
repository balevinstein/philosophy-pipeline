#!/usr/bin/env python3
"""
Setup script for Philosophy Pipeline

This setup.py provides backward compatibility for development installations.
For production use, prefer installing via pip with pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
def read_requirements(filename):
    with open(this_directory / "requirements" / filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#") and not line.startswith("-r")]

setup(
    name="philosophy-pipeline",
    version="1.0.0",
    description="AI-Driven Philosophy Paper Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Philosophy Pipeline Team",
    author_email="team@philosophy-pipeline.org",
    url="https://github.com/balevinstein/philosophy-pipeline",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=read_requirements("base.txt"),
    extras_require={
        "dev": read_requirements("dev.txt"),
        "test": read_requirements("test.txt"),
    },
    entry_points={
        "console_scripts": [
            "philosophy-pipeline=src.pipeline.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Education",
    ],
    keywords="philosophy, ai, paper-generation, academic, research",
    include_package_data=True,
    zip_safe=False,
)
