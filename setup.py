#!/usr/bin/env python3
"""
Setup script for HealthFirst - Health Guidance System
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "HealthFirst - Hệ Thống Hướng Dẫn Y Tế Tại Nhà"

# Read requirements
def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

setup(
    name="healthfirst",
    version="1.0.0",
    author="HealthFirst Team",
    author_email="admin@healthfirst.com",
    description="Hệ thống hướng dẫn y tế tại nhà thông minh",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/healthfirst/healthfirst-web",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "production": [
            "gunicorn>=20.0",
            "gevent>=21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "healthfirst=run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.html", "*.css", "*.js"],
    },
    keywords="health, medical, triage, symptoms, assessment, vietnam, vietnamese",
    project_urls={
        "Bug Reports": "https://github.com/healthfirst/healthfirst-web/issues",
        "Source": "https://github.com/healthfirst/healthfirst-web",
        "Documentation": "https://healthfirst.readthedocs.io/",
    },
)
