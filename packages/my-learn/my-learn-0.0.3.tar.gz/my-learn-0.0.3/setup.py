from setuptools import setup, find_packages

setup(
    name='my-learn',
    version='0.0.3',
    packages=find_packages(exclude=['tests']),
    package_dir={'lengkapin': 'src/lengkapin'},
    description='wip',
    author='Agung Yuliyanto',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
