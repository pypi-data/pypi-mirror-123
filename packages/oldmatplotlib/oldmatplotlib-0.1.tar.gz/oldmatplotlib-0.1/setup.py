from setuptools import setup


setup(
    author='me me me',
    author_email='wooooah@gmail.com',
    name='oldmatplotlib',                    # package name
    version='0.1',                          # version
    description='Package for Lab 2...',      # short description
    url='http://example.com',               # package URL
    install_requires=['matplotlib<3.0'],                    # list of packages this package depends
                                            # on.
    packages=['oldmatplotlib'],              # List of module names that installing
                                            # this package will provide.
)
