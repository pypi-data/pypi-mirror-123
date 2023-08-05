from pathlib import Path
from setuptools import setup

__version__ = None
with open('yandeley/version.py') as f:
    exec(f.read())

setup(
    name='yandeley',
    version=__version__,
    packages=['yandeley', 'yandeley.models', 'yandeley.resources'],
    url='https://github.com/shuichiro-makigaki/yandeley-python-sdk',
    license='Apache',
    author='Shuichiro MAKIGAKI',
    author_email='shuichiro.makigaki@gmail.com',
    description='(Yet Another) Python SDK for the Mendeley API',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',

    install_requires=[
        'arrow==0.5.0',
        'future==0.14.3',
        'memoized-property==1.0.2',
        'requests==2.5.1',
        'requests-oauthlib==0.4.2',
        'oauthlib==0.7.2'
    ],

    tests_require=[
        'pytest==2.6.4',
        'vcrpy==1.2.0'
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
