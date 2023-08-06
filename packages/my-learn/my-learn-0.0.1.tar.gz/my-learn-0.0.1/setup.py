from setuptools import setup, find_packages

setup(
    name='my-learn',
    version='0.0.1',
    packages=find_packages(include=['lengkapin']),
    package_dir={'': 'src'},
    description='wip',
    author='Agung Yuliyanto',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
