from setuptools import setup, find_packages

setup(
    name='pmux',
    version='0.1',
    packages=find_packages(),
    author='Travis Woodrow <travis.woodrow@latitudeengineering.com>, Chasen Johnson <chase.johnson@latitudeengineering.com>',
    description='An effort toward making distributed, cross-language programs easier to write.',
    install_requires=['nnpy', 'msgpack-python'],
    zip_safe=False,
)
