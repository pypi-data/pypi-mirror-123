import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "flywaymigrationconstructmonocdk",
    "version": "0.0.2",
    "description": "flywaymigrationconstructmonocdk",
    "license": "Apache-2.0",
    "url": "https://github.com/180517/flywaymigrationconstruct-monocdk.git",
    "long_description_content_type": "text/markdown",
    "author": "APrzysiuda<180517@umons.ac.be>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/180517/flywaymigrationconstruct-monocdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "flywaymigrationconstructmonocdk",
        "flywaymigrationconstructmonocdk._jsii"
    ],
    "package_data": {
        "flywaymigrationconstructmonocdk._jsii": [
            "flywaymigrationconstructmonocdk@0.0.2.jsii.tgz"
        ],
        "flywaymigrationconstructmonocdk": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.36.0, <2.0.0",
        "monocdk>=1.126.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
