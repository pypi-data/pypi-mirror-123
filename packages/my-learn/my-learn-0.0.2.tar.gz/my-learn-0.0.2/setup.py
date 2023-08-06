from setuptools import setup, find_packages

setup(
    name='my-learn',
    version='0.0.2',
    packages=['lengkapin'],
    package_dir={'lengkapin': 'src/lengkapin'},
    description='wip',
    author='Agung Yuliyanto',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
