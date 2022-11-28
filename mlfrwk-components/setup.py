from struct  import pack
from setuptools import setup


setup(
    name='mlfrwk-components',
    version='1.1.3',
    description="Building blocks for carrying EDA in a Data Science Project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Alejandro Giraldo Henao",
    author_email="algiraldohe@gmail.com",
    license_files=['LICENSE'],
    packages=['components'],
    install_requires=['numpy>=1.19','pandas>=1.5.1','scikit-learn>=1.1.3','SQLAlchemy>=1.4.41','matplotlib>=3.6.2','seaborn>=0.12.1'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ]
)