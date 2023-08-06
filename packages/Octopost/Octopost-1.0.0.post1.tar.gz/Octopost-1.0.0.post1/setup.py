from setuptools import setup
from src.__init__ import __version__

DESCRIPTION = 'Octopost contains a pool of python3 tools for post-processing data obtained with the TDDFT code OCTOPUS.'

with open('README.rst', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='Octopost',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/ckern/octopost',
    author='Christian Kern, MSc.',
    author_email='christian.kern@uni-graz.at',
    package_dir={'': 'src'},
    packages=[''],
    python_requires='>=3.8',
    install_requires=['numpy>=1.20', 'scipy>=1.5', 'vtk>=9.0',
                      'matplotlib>=3.3', 'h5py>=3.0'],
    extras_require={
        'docs': ['sphinx==4.1.2', 'sphinx-rtd-theme==0.5.2'],
        'test': ['pytest==6.2.5', 'flake8==3.9.2'],
        'dev': ['sphinx==4.1.2', 'check-manifest==0.46',
                       'twine==3.4.2', 'sphinx-rtd-theme==0.5.2']},
    classifiers=['Topic :: Documentation :: Sphinx',
                 'Natural Language :: English',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.8',
                 'Topic :: Communications :: Email',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Topic :: Software Development :: Version Control :: Git',
                 'Topic :: Text Processing :: Markup :: reStructuredText',
                 'License :: OSI Approved :: MIT License'
                 ]
)
