from setuptools import setup

__project__ = 'chessvalidator'
__version__ = '0.0.5'
__description__ = 'validates a chess board using the correct datatype'
__packages__ = ['chessvalidator']
__author__ = '6mm3z7ms'
__author_email__ = '6mm3z7ms@anonaddy.me'
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
setup(
        name = __project__,
        version = __version__,
        description = __description__,
        packages = __packages__,
        author = __author__,
        author_email = __author_email__,
        classifiers = __classifiers__,
)
