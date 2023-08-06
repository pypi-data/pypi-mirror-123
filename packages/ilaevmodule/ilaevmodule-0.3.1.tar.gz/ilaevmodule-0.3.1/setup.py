from setuptools import setup

setup(
    name='ilaevmodule',
    version='0.3.1',
    description='A example Python package',
    url='https://github.com/nilaev',
    author='Nikita Ilaev',
    author_email='nik.ilaev@mail.ru',
    license='BSD 2-clause',
    packages=['my_module'],
    install_requires=[
        'numpy<1.17',
    ],
)