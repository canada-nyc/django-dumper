from setuptools import setup, find_packages


setup(
    name='django-dumper',
    version='0.0.1',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=find_packages(),
    url='https://www.github.com/saulshanabrook/django-dumper',
    license='LICENSE.txt',
    description='Django URL cache invalidate from model saves',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django>=1.3,<1.6",
    ],
)
