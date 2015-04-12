# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]
### Added
- List classes (enumerate, itemize, description)
- The list of packages for the constructor of the Document class.

## [0.7.1]
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


## [0.6.0] - 07-01-2015
### Added
- Figure class
- Command and Parameter classes
- `with` statement support


## [0.5.0] - 02-06-2014
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

[unreleased]: https://github.com/JelteF/PyLaTeX/compare/v0.7.1...HEAD
[0.7.1]: https://github.com/JelteF/PyLaTeX/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/JelteF/PyLaTeX/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/JelteF/PyLaTeX/compare/v0.6...v0.6.1
[0.6]: https://github.com/JelteF/PyLaTeX/compare/v0.5...v0.6
[0.5]: https://github.com/JelteF/PyLaTeX/compare/v0.4.2...v0.5
[0.4.2]: https://github.com/JelteF/PyLaTeX/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/JelteF/PyLaTeX/compare/68ddef6bc43a5dff42105c3a38068d87d99d049f...v0.4.1
