from setuptools import setup, find_packages


setup(
    name='broker_clients',
    version='0.0.1',
    license='UNLICENSED',
    author="Oswaldo Cruz",
    author_email='oswaldo_cs_94@hotmail.com',
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    packages=['broker_clients'],
    package_data={
        '': [
            'alembic/*',
            'data/*',
            'alembic/versions/*',
            'emulator_proxy/*/*.py',
            'emulator_proxy/*.py',
            'quantfury_proxy/*/*.py',
            'quantfury_proxy/*.py',
            'binance_proxy/*/*.py',
            'binance_proxy/*.py'
        ],
    }
)