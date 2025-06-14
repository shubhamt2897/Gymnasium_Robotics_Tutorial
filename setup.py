#!/usr/bin/env python3

"""
Setup script for the MaMuJoCo_Tutorial package.
"""

from setuptools import setup, find_packages

setup(
    name="mamujoco_tutorial",
    version="0.1.0",
    description="A comprehensive tutorial and toolkit for MuJoCo with Gymnasium",
    author="MaMuJoCo_Tutorial Contributors",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/MaMuJoCo_Tutorial",
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.28.1",
        "mujoco>=2.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
)
