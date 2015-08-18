from setuptools import setup, find_packages

setup(
    name='PickPocket',
    version='0.1',
    description='Batch modify articles in your Pocket',
    url='https://github.com/garettmd/PickPocket',
    author='Garett Dunn',
    author_email='garettmd@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='pocket Pocket getpocket',
    packages=find_packages(),
    install_requires=['flask', 'flask-session', 'requests'],

)
