#! /usr/bin/env python3

from setuptools import setup


setup(
    name="uninews",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    install_requires=[
        "cmslib",
        "flask",
        "functoolsplus",
        "his",
        "hwdb",
        "mdb",
        "newslib",
        "previewlib",
        "wsgilib",
    ],
    packages=["uninews"],
    description="Multi-source news API.",
)
