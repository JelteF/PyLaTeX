# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased][unreleased]
This realease will bring some great changes. The whole package has been
refactored and actual documentation has been added. Because of this, things have
been moved an renamed.

### Changed
- The base_classes submodule has been split into multiple sub-submodules.
- The old baseclasses have been renamed as well. They now have easier names that
    better show their purpose.
- The command and parameters submodules have been merged into one command
    submodule in the base_classes submodule.
- The numpy classes have been moved to the math submodule.
- For all of the previous changes the old submodules and names should still work
    during the transition period, but they will be removed before the final
    release.

- The `Plt` class has been renamed to `MatplotlibFigure`. Its `add_plot` method
    also doesn't take a plt argument anymore. The plt module is now imported
    when a `MatplotlibFigure` figure is instantiated.

### Added
- Lots of documentation!!!!!
- A float environment base class.
- An unfinished Quantity class that can be used in conjunction with the
    quantitities package. https://pythonhosted.org/quantities/

## [0.8.0] - 23-05-2015
### Added
- List classes (enumerate, itemize, description)
- Arguments for plt.savefig
- SubFigure class for use with subcaption package
- Command line argument for ./testall.sh to supply a custom python command
- The generate_tex method is now usable in every class, this makes making
    snippets even easier.
- MultiColumn and MultiRow classes for generalized table layouts.

### Changed
- BaseLaTeXNamedContainer now uses the name of the class as the default
    container_name
- The `Table` object is going to be deprecated in favor of the better named
    `Tabular` object. This will take a couple of releases.
- Allow the data keyword argument of containers to be a single item instead of a
    list. If this is the case it will be wrapped in a list on initialization.

### Fixed
- Propagate packages recursively add packages of sub containers
- Make cleanup of files Windows compatible
- Filenames can be paths (`foo/bar/my_pdf`).
- Replace `filename` by `filepath` in the names of the arguments.
- Matplotlib support now uses the tmpfile module, this fixes permission issues
    with the badly previously badly located tmp directory.
- The temp directory is only removed in generate_pdf when cleaning is
    enabled


## [0.7.1] - 21-03-2015
### Added
- Contributing guidelines.

### Changed
- The non keyword argument for filename is now called path instead of filename
    to show it can also be used with paths.
- Travis now checks for Flake8 errors.

### Fixed
- Fix a bug in Plt and one in fix_filename that caused an error when using them
    with some filenames (dots in directories and a file without an extension)


## [0.7.0] - 17-03-2015
### Added
- Matplotlib support
- Quite a bit of basic docstrings

### Changed
- Filenames should now be specified to the `generate_pdf`/`generate_tex`
  methods of document. If this is not done the `default_filename` attribute
  will be used.

### Fixed
- Fix a lot of bugs in the `escape_latex` function


## [0.6.1] - 11-01-2015
### Added
- Travis tests

### Fixed
- Bug in VectorName


## [0.6] - 07-01-2015
### Added
- Figure class
- Command and Parameter classes
- `with` statement support


## [0.5] - 02-06-2014
### Added
- Python 2.7 support


## [0.4.2] - 18-03-2014
### Added
- More table types


## [0.4.1] - 29-01-2014
### Added
- Partial experimental support for multicol/multirow

### Fixed
- Fix package delegation with duplicate packages


[unreleased]: https://github.com/JelteF/PyLaTeX/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/JelteF/PyLaTeX/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/JelteF/PyLaTeX/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/JelteF/PyLaTeX/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/JelteF/PyLaTeX/compare/v0.6...v0.6.1
[0.6]: https://github.com/JelteF/PyLaTeX/compare/v0.5...v0.6
[0.5]: https://github.com/JelteF/PyLaTeX/compare/v0.4.2...v0.5
[0.4.2]: https://github.com/JelteF/PyLaTeX/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/JelteF/PyLaTeX/compare/68ddef6bc43a5dff42105c3a38068d87d99d049f...v0.4.1
