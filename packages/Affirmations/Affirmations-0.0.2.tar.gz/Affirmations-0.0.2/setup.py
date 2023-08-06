from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Affirmations', 
    version='0.0.2',
    description='Randomly adds affirming print statements to functions.',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/TimNicholsonShaw/affirmation',  
    author='Tim Nicholson-Shaw',
    author_email='timnicholsonshaw@gmail.com',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='Self Care',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[],

    project_urls={ 
        'GitHub': 'https://github.com/TimNicholsonShaw/affirmation',

    },
)