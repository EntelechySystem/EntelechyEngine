from setuptools import setup, find_packages

setup(
    name='entelechy_engine',
    version='0.0.8_alpha',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'openpyxl',
        'matplotlib',
        'igraph',
        'torch',
        'jax',
        'numba',
        'scipy'
    ],
    author='Entelechy System Explorer',
    author_email='',
    description='A description of your package',
    url='https://github.com/EntelechySystem/EntelechyEngine',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.12.1',
)
