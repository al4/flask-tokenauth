"""
Flask-TokenAuth
--------------

Token-based authentication for Flask routes
"""
from setuptools import setup


setup(
    name='Flask-TokenAuth',
    version='0.1.0',
    url='http://github.com/al4/flask-tokenauth/',
    license='MIT',
    author='Alex Forbes',
    author_email='alexforbes@gmail.com',
    description='Token-based authentication for Flask routes',
    long_description=__doc__,
    py_modules=['flask_tokenauth'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    test_suite="test_tokenauth",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
