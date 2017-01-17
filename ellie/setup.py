'''setup the app'''
from setuptools import setup

setup(
    name='ellie',
    packages=['ellie'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest_runner',
    ],
    test_require=[
        'pytest',
    ]
)