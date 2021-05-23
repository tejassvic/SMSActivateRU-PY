#!/usr/bin/env python
import setuptools

with open('requirements.txt') as f:
    dependencies = [l.strip() for l in f]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SMSActivateRU',
    version='0.1.0',
    description='sms-activate.ru Api Wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='#',
    author='WarHawk',
    author_email='WarHawk-Dcoderz@protonmail.com',
    url='git@github.com:WarHawk-Dcoderz/SMSActivateRU-PY.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Typing :: Typed'
    ],
    install_requires=dependencies,
    python_requires='>=3.6'
)