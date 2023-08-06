import io
from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='Fifty-Docker',
    version='1.3',
    url='https://bitbucket.org/50onred/fifty-docker/overview',
    license='BSD',
    author='Steve Dorazio',
    author_email='sdorazio@50onred.com',
    description='Docker utilities.',
    long_description=readme,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Click',
        'Jinja2',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'j2=fifty_docker.main:render_template',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
