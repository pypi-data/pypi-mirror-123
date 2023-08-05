from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Auto data science '
LONG_DESCRIPTION = 'Auto Data science'

# Setting up
setup(
    # the name must match the folder name
    name="auto_ds",
    version=VERSION,
    author="Kaustuv.kunal@gmail.com",
    author_email="<kaustuv.kunal@amail.com>",
    description='Auto Data Science Toolkit',
    long_description='''
A Python tool that automatically creates and optimizes machine learning pipelines .
Contact
=============
If you have any questions or comments about AUTODS, please feel free to mail us at:
kaustuv.kunal@gmail.com
This project is hosted at https://github.com/Littilabs/auto_ds
''',
    packages=find_packages(),
    install_requires=['catboost>=0.25.1',
                      'pandas>=1.2.4',
                      'optuna>=2.9.1',
                      'scikit_learn>=1.0' ],
    extras_require={},

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7" ],
    keywords=['pipeline optimization', 'hyperparameter optimization', 'data science', 'machine learning',  'evolutionary computation'],
    )