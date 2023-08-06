from setuptools import setup

setup(
    name='instail',
    version='0.1.0',
    description='A example Python package',
    author='Nikita Kozhukharov',
    author_email='n.korzhikov@gmail.com',
    license='MIT',
    packages=['instail'],
    install_requires=['numpy<1.16.5'],
)
