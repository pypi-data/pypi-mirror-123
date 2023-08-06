from setuptools import setup


setup(
    author='me me me',
    author_email='wooooah@gmail.com',
    name='package_lab2',                    # package name
    version='0.5',                          # version
    description='Package for Lab 2...',      # short description
    url='http://example.com',               # package URL
    install_requires=['matplotlib<1.2'],                    # list of packages this package depends
                                            # on.
    packages=['package_lab2'],              # List of module names that installing
                                            # this package will provide.
)
