from setuptools import setup

setup(
    name='STOSC UI',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
        'boto3',
        'requests',
        'color-it',
        'pandas',
        'mysql-connector-python'
    ],
    entry_points='''
        [console_scripts]
        ui=main:main
    ''',
)
