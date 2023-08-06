from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='tns-piler', 
    version='0.0.4',
    description='Tool for finding cumulative pileups',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/TimNicholsonShaw/piler',  
    author='Tim Nicholson-Shaw',
    author_email='timnicholsonshaw@gmail.com',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='Sequencing, Bioinformatics',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=['pysam', 'gffutils',],

    entry_points={
        'console_scripts': [
            'Piler=Piler.Piler:main',
        ],
    },

    project_urls={ 
        'Lab Website': 'https://labs.biology.ucsd.edu/lykkeandersen/index.html',

    },
)