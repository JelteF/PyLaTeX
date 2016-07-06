try:
    from setuptools import setup
    from setuptools.command.install import install
    from setuptools.command.egg_info import egg_info
except ImportError:
    from distutils.core import setup
import sys
import os
import subprocess
import errno


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

PY2_CONVERTED = False


extras['all'] = list(set([req for reqs in extras.values() for req in reqs]))


# Automatically convert the source from Python 3 to Python 2 if we need to.
class CustomInstall(install):
    def run(self):
        convert_to_py2()
        install.run(self)


class CustomEggInfo(egg_info):
    def initialize_options(self):
        convert_to_py2()
        egg_info.initialize_options(self)


def convert_to_py2():
    if source_dir == 'python2_source' and not PY2_CONVERTED:
        try:
            # Check if 3to2 exists
            subprocess.check_output(['3to2', '--help'])
            subprocess.check_output(['pasteurize', '--help'])
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e
            if not os.path.exists(os.path.join(source_dir, 'pylatex')):
                raise ImportError('3to2 and future need to be installed '
                                  'before installing when PyLaTeX for Python '
                                  '2.7 when it is not installed using one of '
                                  'the pip releases.')
        else:
            converter = os.path.dirname(os.path.realpath(__file__)) \
                + '/convert_to_py2.sh'
            subprocess.check_call([converter])
            global PY2_CONVERTED
            PY2_CONVERTED = True


setup(name='PyLaTeX',
      version='1.0.3',
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
      cmdclass={
          'install': CustomInstall,
          'egg_info': CustomEggInfo,
      },
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
