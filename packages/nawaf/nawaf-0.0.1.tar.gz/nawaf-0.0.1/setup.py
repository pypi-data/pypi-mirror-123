from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='nawaf',
    version='0.0.1',
    description='My Name :)',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Nawaf Alqari',
    author_email='contact@nawaf.cf',
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    license='MIT',
    keywords=['nawaf'],
    classifiers=[
    'Programming Language :: Python :: 3.6',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
  ],
)

# python setup.py sdist
# twine upload dist/jsonwriter-[version].tar.gz