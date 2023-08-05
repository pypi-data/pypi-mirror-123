from setuptools import setup, find_packages

__version__ = '0.1.1'

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='techharper',
    author="Alex Elia",
    author_email="alex.elia42+pip@gmail.com",
    packages=find_packages(),
    version=__version__,
    description='Tool to fetch the latest updates for technologies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests==2.25.1',
    ],
    url='https://github.com/BoredTweak/techharper',
    python_requires='>=3.7',
    zip_safe=False,
    license='GPL-3',
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)