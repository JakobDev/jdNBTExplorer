#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as f:
    description = f.read()

setup(name="jdNBTExplorer",
    version="1.0",
    description="A Editor for Minecraft NBT files",
    long_description=description,
    long_description_content_type="text/markdown",
    author="JakobDev",
    author_email="jakobdev@gmx.de",
    url="https://gitlab.com/JakobDev/jdNBTExplorer",
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        "jdTranslationHelper",
        "PyQt6",
        "nbt"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["jdNBTExplorer = jdNBTExplorer.jdNBTExplorer:main"]
    },
    license="GPL v3",
    keywords=["JakobDev","PyQt","PyQt6","Minecraft","NBT","English","German"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Other Environment",
        "Environment :: X11 Applications :: Qt",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Natural Language :: German",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
 )

