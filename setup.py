from setuptools import find_packages, setup

setup(
    name="Psychic Spoon",
    version="0.1.0",
    description="A framework for managing cache keys in a convenient way.",
    author="Stephen Ling",
    author_email="lingfromsh@163.com",
    packages=find_packages(include=["psychic_spoon"]),
    python_requires=">=3.8",
    install_requires=[
        "orjson >= 3.6.6",
        "redis >= 4.1.3",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
