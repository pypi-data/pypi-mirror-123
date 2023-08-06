import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='pythief-dj',
    version='0.3.2',
    description='A CLI for "borrowing" music from YouTube. DJ use only, and also, you know the deal, DJs, right?',
    author='Ben Stein',
    author_email='ben.s.stein@gmail.com',
    url='https://github.com/jammerware/pythief-dj',
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'Click',
        'flask',
        'flask-restful',
        'pydub',
        'pymitter',
        'python-dotenv',
        'pytube',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'pythief-dj = commands.cli:cli',
        ],
    },
)
