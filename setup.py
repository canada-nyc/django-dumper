from setuptools import setup, find_packages


setup(
    name='django-dumper',
    version='0.2.3',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=find_packages(),
    url='https://www.github.com/saulshanabrook/django-dumper',
    license='LICENSE.txt',
    description='Django URL cache invalidation from model saves',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django>=1.4,<1.7",
        "six",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries",
    ],
)
