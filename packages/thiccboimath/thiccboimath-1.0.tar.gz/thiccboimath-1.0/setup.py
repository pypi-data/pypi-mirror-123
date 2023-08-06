import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # should match the package folder
    name='thiccboimath',
    # should match the package folder
    packages=['thiccboimath'],
    version='1.0',                                  # important for updates
    # should match your chosen license
    license='GNU GENERAL PUBLIC LICENSE',
    description='A simple python math function package.',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='ThickduckPlayz',
    author_email='iamhackerboi8@gmail.com',
    url='https://github.com/Thickduck/pymath/tree/main/Python%20maths%20project/Math%20operators',
    # list all packages that your package uses
    install_requires=['requests'],
    keywords=["pypi", "thiccboimath", "math"],  # descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/Thickduck/pymath/archive/refs/tags/1.0.tar.gz",
)
