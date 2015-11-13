from setuptools import setup, find_packages


setup(
    name='pmux',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1',

    description='Makes writing independent Python processes easy',

    # The project's main homepage.
    url='https://github.com/latitudeengineering/process_mux',

    # Author details
    author='Chase Johnson, Travis Woodrow',
    author_email='chase.johnson@latitudeengineering.com,travis.Woodrow@latitudeengineering.com',

    # Choose your license
    license='LGPLv3',


    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pyzmq'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
