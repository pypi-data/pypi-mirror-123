from setuptools import setup

setup(
    name='ilaevmodule',
    version='0.1.0',
    description='A example Python package',
    url='',
    author='Nikita Ilaev',
    packages=['my_module'],
    install_requires=[
        'pandas<1.0',
    ],
)