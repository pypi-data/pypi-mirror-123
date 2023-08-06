from setuptools import setup

setup(
    name='thingbits_ha',
    version='0.1.0',
    description='ThingBits HomeAssistant Integration',
    url='https://github.com/thingbits',
    author='ThingBits',
    author_email='dev@thingbits.com',
    packages=['thingbits_ha'],
    install_requires=['paho-mqtt==1.5.1'],

    classifiers=[
        'Operating System :: POSIX :: Linux',        
    ],
)

