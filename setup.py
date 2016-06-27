try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
import os
import errno
import versioneer


if sys.version_info[:2] <= (2, 6):
    raise RuntimeError(
        "You're using Python <= 2.6, but this package requires either Python "
        "2.7, or 3.3 or above, so you can't use it unless you upgrade your "
        "Python version."
    )

dependencies = ['ordered-set']

extras = {
    'docs': ['sphinx'],
    'matrices': ['numpy'],
    'matplotlib': ['matplotlib'],
    'quantities': ['quantities', 'numpy'],
    'testing': ['flake8', 'pep8-naming', 'flake8_docstrings', 'nose'],
    'convert_to_py2': ['3to2', 'future>=0.15.2'],
}

if sys.version_info[0] == 3:
    source_dir = '.'
else:
    source_dir = 'python2_source'
    dependencies.append('future>=0.15.2')


extras['all'] = list(set([req for reqs in extras.values() for req in reqs]))


setup(name='PyLaTeX',
      version=versioneer.get_version(),
      author='Jelte Fennema',
      author_email='pylatex@jeltef.nl',
      description='A Python library for creating LaTeX files and snippets',
      long_description=open('README.rst').read(),
      package_dir={'': source_dir},
      packages=['pylatex', 'pylatex.base_classes'],
      url='https://github.com/JelteF/PyLaTeX',
      license='MIT',
      install_requires=dependencies,
      extras_require=extras,
      cmdclass=versioneer.get_cmdclass(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Text Processing :: Markup :: LaTeX',
      ]
      )
