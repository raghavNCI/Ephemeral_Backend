from setuptools import setup, find_packages

setup(
    name='Ephemeral_Hasher',
    version='0.1',
    packages=find_packages(),
    description='A simple Django utility for hashing strings with HMAC and SHA-256.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Praneeth Raghava',
    author_email='x23211946@student.ncirl.ie',
    install_requires=[
        'Django>=3.0',  # Specify Django as a dependency if needed
    ],
)
