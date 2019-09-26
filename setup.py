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
import versioneer

cmdclass = versioneer.get_cmdclass()
version = versioneer.get_version()

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
    'testing': ['flake8<3.0.0', 'pep8-naming==0.8.2',
                'flake8_docstrings==1.3.0', 'pycodestyle==2.0.0',
                'pydocstyle==3.0.0', 'pyflakes==1.2.3', 'nose', 'flake8-putty',
                'coverage'],
    'convert_to_py2': ['3to2', 'future>=0.15.2'],
}

if sys.version_info[0] == 3:
    source_dir = '.'
    if sys.version_info < (3, 4):
        del extras['docs']
        extras['matplotlib'] = ['matplotlib<2.0.0']
        extras['matrices'] = ['numpy<1.12.0']
        extras['quantities'][1] = 'numpy<1.12.0'
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
    global PY2_CONVERTED
    if source_dir == 'python2_source' and not PY2_CONVERTED:
        pylatex_exists = os.path.exists(os.path.join(source_dir, 'pylatex'))

        if '+' not in version and pylatex_exists:
            # This is an official release, just use the pre existing existing
            # python2_source dir
            return

        try:
            # Check if 3to2 exists
            subprocess.check_output(['3to2', '--help'])
            subprocess.check_output(['pasteurize', '--help'])
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            if not pylatex_exists:
                raise ImportError('3to2 and future need to be installed '
                                  'before installing when PyLaTeX for Python '
                                  '2.7 when it is not installed using one of '
                                  'the pip releases.')
        else:
            converter = os.path.dirname(os.path.realpath(__file__)) \
                + '/convert_to_py2.sh'
            subprocess.check_call([converter])
            PY2_CONVERTED = True


cmdclass['install'] = CustomInstall
cmdclass['egg_info'] = CustomEggInfo

setup(name='PyLaTeX',
      version=version,
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
      cmdclass=cmdclass,
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
