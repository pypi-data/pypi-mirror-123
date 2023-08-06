from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Package for adding custom xmp to Image Carriers'

setup(
    name='sgsxmp',
    version='1.1.0',
    author='Andrew Neary',
    author_email='andrew.neary@sgsco.com',
    description='Add xmp to Image Carriers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='SGS',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['sgsxmp = sgsxmp.sgsxmp:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    keywords='sgsxmp',
    install_requires=requirements,
    zip_safe=False
)