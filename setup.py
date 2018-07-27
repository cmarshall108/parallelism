try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


long_description = """
A replacement for Python's threading module used in attempt to efficient achieve single-core threading parallelism.
"""

setup(name='parallelism',
    description='Parallelism - Efficient Single-Core Parallel Threading',
    long_description=long_description,
    license='BSD',
    version='0.1',
    author='Caleb Marshall',
    author_email='anythingtechpro@gmail.com',
    maintainer='Caleb Marshall',
    maintainer_email='anythingtechpro@gmail.com',
    url='https://github.com/AnythingTechPro/parallelism',
    packages=['parallelism'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ])
