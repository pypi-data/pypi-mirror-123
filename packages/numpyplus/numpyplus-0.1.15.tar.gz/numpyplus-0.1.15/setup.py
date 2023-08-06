from setuptools import setup

setup(
    name='numpyplus',
    version='0.1.15',    
    description='An upgraded version of numpy',
    url='https://github.com/Shashulovskiy/numpyplus',
    author='Artem Shashulovskiy',
    author_email='shashulovskiy@gmail.com',
    license='BSD 2-clause',
    packages=['numpyplus'],
    install_requires=['numpy==1.7.0',
                     'tensorflow',
                     ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
