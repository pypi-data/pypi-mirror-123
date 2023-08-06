import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-github-role",
    "version": "0.0.2",
    "description": "IAM Role that can be assumed by GitHub workflows",
    "license": "Apache-2.0",
    "url": "https://github.com:/dklabs/cdk-github-role.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com:/dklabs/cdk-github-role.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_github_role",
        "cdk_github_role._jsii"
    ],
    "package_data": {
        "cdk_github_role._jsii": [
            "cdk-github-role@0.0.2.jsii.tgz"
        ],
        "cdk_github_role": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.127.0, <2.0.0",
        "aws-cdk.core>=1.127.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.39.0, <2.0.0",
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
