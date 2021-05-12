
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hmrs_mission_control",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Gabriel Rodrigues",
    author_email="gabrielsr@gmail.com",
    description="Mission Control for Heterogeneous Multi-Robots Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielsr/hmrs_mission_control",
    packages=find_packages(
        include=['deeco', 'deeco.*', 'evaluation', 'evaluation.*',
                 'mission_control'] ,
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
