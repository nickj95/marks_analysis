from setuptools import setup, find_packages

setup(
    name='marks_analysis',
    version='0.1.0',
    author='Nicholas James',
    author_email='nicholas.james619@gmail.com',
    description='A package for analyzing exam marks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nickj95/marks_analysis',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)