from setuptools import setup, find_packages

setup(
    name="project-rigor-punchcard",
    version="0.1",
    packages=find_packages(),
    install_requires=["project-rigor"],
    author="jarvick257",
    description="A Punchcard module for Project RIGOR",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jarvick257/rigor-punchcard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
