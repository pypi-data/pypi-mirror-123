from distutils.core import setup
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lietorch",
    author="B.M.N. Smets et.al",
    author_email="b.m.n.smets@tue.nl",
    description="Geometric ML and Lie analysis package for PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=setuptools.find_packages(),
    package_data={'lietorch' : ['lib/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
)
