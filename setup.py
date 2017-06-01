
from setuptools import setup

setup(
    name='horrible',
    version='0.0.0',
    long_description=__doc__,
    packages=['horrible'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-socketio',
        'gevent'
    ]
)
