from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='groundplane',
    version='0.0.1',
    author='MakUrSpace',
    author_email='hello@makurspace.com',
    description='MakerModule Automation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.makurspace.com',
    packages=["groundplane"],
    install_requires=["requests", "pywemo"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
