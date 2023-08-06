from setuptools import setup, find_packages

with open("README.md","r") as f:
    README=f.read()# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links

with open("requirements.txt","r") as f:
    all_reqs = f.read().split('\n')
    install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]


setup (
    name = 'biblibrary',
    description = 'A simple command line tool for bibliography management',
    version = '1.0.1',
    packages = find_packages(), # list of all packages
    install_requires = install_requires,
    python_requires='>=3', # any python greater than 2.7
    entry_points='''
        [console_scripts]
        biblib=biblib:main
    ''',
    author="Jago Strong-Wright",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/jagoosw/biblibrary',
    download_url='https://github.com/jagoosw/biblibrary/archive/1.0.0.tar.gz',
    author_email='jagoosw@protonmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)