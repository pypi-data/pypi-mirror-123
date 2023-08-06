from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-url-parser',
    version='0.1.3',
    description='The purpose of this plugin is to parse URL and return it.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='',
    author_email='',
    packages=['tracardi_url_parser'],
    install_requires=[
        'tracardi_plugin_sdk>=0.6.18',
        'tracardi_dot_notation'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
