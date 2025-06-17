"""PostGrid Python SDK setup configuration."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="postgrid-sdk",
    version="0.1.0",
    author="TechWithTy",
    author_email="techwithty@example.com",
    description="Async Python SDK for the PostGrid API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techwithty/postgrid-python-sdk",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=1.10.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "black>=22.3.0",
            "isort>=5.10.1",
            "mypy>=0.961",
            "pytest>=7.1.2",
            "pytest-asyncio>=0.19.0",
            "pytest-cov>=3.0.0",
            "ruff>=0.0.260",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Bug Reports": "https://github.com/techwithty/postgrid-python-sdk/issues",
        "Source": "https://github.com/techwithty/postgrid-python-sdk",
    },
)