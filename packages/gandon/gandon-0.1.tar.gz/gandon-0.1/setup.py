from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='gandon',
    version='0.1',
    description='A package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tanglespace/gandon',
    author='Jackson Storm',
    author_email='c6lculus8ntr0py@gmail.com',
    license="Apache 2",
    project_urls={
        'Documentation': 'https://github.com/tanglespace/gandon',
        'Source': 'https://github.com/tanglespace/gandon',
        'Tracker': 'https://github.com/tanglespace/gandon/issues',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'hydralit>=1.0.10',
    ],
    python_requires='>=3.6',
    keywords=[
        'GAN',
        'Generative',
        'Machine Learning',
        'Data Modelling',
        'Presentation',
    ],
)
