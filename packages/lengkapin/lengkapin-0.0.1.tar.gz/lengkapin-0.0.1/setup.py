from setuptools import setup, find_packages

setup(
    name='lengkapin',
    version='0.0.1',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description='wip',
    author='Agung Yuliyanto',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
