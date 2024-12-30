import os
from setuptools import setup, find_packages
 
about = {}
 
here = os.path.abspath(os.path.dirname(__file__))
 
with open(os.path.join(here, "pyavrio_scheduler", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)
 
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    readme = f.read()
 
 
setup(
    name=about["__title__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    version=about["__version__"],
    url=about["__url__"],
    packages=find_packages(),
    package_data={"": ["LICENSE", "README.md"]},
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",  
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)