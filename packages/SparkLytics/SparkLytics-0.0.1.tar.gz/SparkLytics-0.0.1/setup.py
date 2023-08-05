from setuptools import setup

VERSION = '0.0.1'

CLASSIFIERS = ['Intended Audience :: Science/Research',
			   'Intended Audience :: Developers',
			   'Programming Language :: Python :: 3',
			   'Topic :: Software Development',
			   'Topic :: Scientific/Engineering',
			   'Operating System :: Microsoft :: Windows',
			   'Operating System :: Unix',
			   'Operating System :: MacOS'
			   ]

setup(
	name='SparkLytics',
    version=VERSION,
	packages=['SparkLytics'],
    url='https://github.com/scottclay/SparkLytics',
	license='MIT',
    author='Scott Clay',
    author_email='scottclay8@gmail.com',
    description='A library of useful functions to help with ML analysis with PySpark and MLLib.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	install_requires=['numpy >= 1.14.3', 'matplotlib >= 3.0', 'seaborn >= 0.8.1', 'pandas >= 0.23.0',
					'scikit-learn >= 0.19.1'],
    zip_safe=False,
	classifiers = CLASSIFIERS
	)
