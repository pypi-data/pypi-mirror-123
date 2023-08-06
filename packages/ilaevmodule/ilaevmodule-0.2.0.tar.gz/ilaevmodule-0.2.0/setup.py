from setuptools import setup

setup(
    name='ilaevmodule',
    version='0.2.0',
    description='A example Python package',
    url='https://github.com/nilaev',
    author='Nikita Ilaev',
    author_email='nik.ilaev@mail.ru',
    license='BSD 2-clause',
    packages=['my_module'],
    install_requires=[
        'pandas<1.0',
    ],
)