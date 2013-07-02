from setuptools import setup, find_packages


setup(
    name='django-dumper',
    version='0.0.0',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=find_packages(),
    url='https://www.github.com/saulshanabrook/django-dumper',
    license='LICENSE.txt',
    description='Django URL cache invalidation from model saves',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django>=1.3,<1.6",
        "six",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries",
    ],
)
