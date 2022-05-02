import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='videoall',
    version='0.0.6',
    author='C灵C',
    author_email='c0c@cocpy.com',
    description='All video download',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cocpy/VideoAll',
    packages=setuptools.find_packages(),
    install_requires=[

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)