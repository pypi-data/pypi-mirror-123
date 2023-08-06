from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'A proprietary open source fintech python package with a plethora of features for building equity and cryptocurrency trading algorithms.'
LONG_DESCRIPTION = 'Please visit the github for a longer disc.'

# Setting up
setup(
    # the name must match the folder name containing the package files
    name="ProfiTrade",
    version=VERSION,
    author="Harriharan Sivakumar",
    author_email="<harrishiv6@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'lxml', 'csv'],
    url='https://github.com/harrisiva/ProfiTrade-Package',

    keywords=['python', 'trading', 'stock',
              'crypto', 'profiTrade', 'profit trade'],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
