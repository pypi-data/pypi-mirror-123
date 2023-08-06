from setuptools import setup

VERSION = '1.0.2'

setup(
    name='rsa_crypto',
    version=VERSION,

    description='Encrypt and decrypt data using RSA certificates.',
    url='https://github.com/Christophe-Gauge/rsa_crypto',

    author='Christophe Gauge',
    author_email='chris@videre.us',

    packages=['rsa_crypto'],

    install_requires=['pycryptodome'],

    entry_points={
        'console_scripts': [
            'rsa_crypto = rsa_crypto.__main__:main'
        ]
    },

)
