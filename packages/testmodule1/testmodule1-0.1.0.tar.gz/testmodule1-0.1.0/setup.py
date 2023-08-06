from setuptools import setup

setup(
    name='testmodule1',
    version='0.1.0',    
    description='A example Python package',
    author='Vladislav Gusev',
    author_email='vladislav.sg@yandex.ru',
    packages=['testmodule1'],
    install_requires=['numpy<1.20.1']
)
