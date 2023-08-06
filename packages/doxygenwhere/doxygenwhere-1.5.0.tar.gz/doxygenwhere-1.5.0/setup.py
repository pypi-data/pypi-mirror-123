import setuptools
import doxygenwhere

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='doxygenwhere',
    version=doxygenwhere.__version__,
    description='Python interface to locate doxygen installation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bjoernrennfanz/pydoxygenwhere',
    author=doxygenwhere.__author__,
    author_email='bjoern@fam-rennfanz.de',
    license=doxygenwhere.__license__,
    packages=setuptools.find_packages(),
    package_data={"doxygenwhere": ["data/*.zip"]},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False)
