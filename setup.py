import contexttimer

from os.path import join, dirname

from setuptools import setup

setup(
    name="contexttimer",
    version=contexttimer.__version__,
    license="GPLv3",
    description='A timer context manager measuring the clock wall time of the code block it contains.',
    author="Balthazar Rouberol",
    author_email='brouberol@imap.cc',
    url='https://github.com/brouberol/contexttimer',
    packages=['contexttimer'],
    keywords=['time', 'timer'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
)
