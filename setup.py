from setuptools import setup

setup(
    name='PyTeX',
    version='0.0.1',    
    description='Python representation of LaTeX documents',
    url='https://github.com/davidnkraemer/pytex',
    author='David Kraemer',
    author_email='david.kraemer@stonybrook.edu',
    license='Creative Commons',
    packages=['pytex'],
    install_requires=['bibtexparser'],

    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)

