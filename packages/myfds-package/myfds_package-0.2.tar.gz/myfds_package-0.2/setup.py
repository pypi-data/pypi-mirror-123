from setuptools import setup

setup(
    name='myfds_package',  # package name
    version='0.2',  # version
    description='My first package',  # short description
    url='https://github.com/Ditmarscehen/myfds_package',  # package URL
    install_requires=['pandas'],  # list of packages this package depends
    # on.
    packages=['myfds_package'],  # List of module names that installing
    # this package will provide.
)
