import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='xcomposite',
    version='2.0.1',
    author='Mike Malinowski',
    author_email='mike@twisted.space',
    description='A python package exposing the class composition design pattern',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/xcomposite',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        '': ['examples/game/data/*.json'],
    },
    keywords="xcomposite composite composition inheritence side combine",
)
