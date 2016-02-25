# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]
- No notable updates

## [1.0.1] - 2016-02-25
### Fixed
- Subpackages now get included properly
- Updated examples to use plural `transmissions`

## [1.0.0] - 2015-11-06
### Added
- Django email backend
- Support for scheduled sending via the `start_time` parameter in `Transmissions`
- Support for marking messages as transactional or non-transactional via the `transactional` parameter in `Transmissions`
- Support for skipping suppression (SparkPost Elite only) via the `skip_suppression` parameter in `Transmissions`

## [1.0.0.dev2] - 2015-09-01
### Added
- Code coverage via [coveralls]
- CONTRIBUTING file for notes on how to contribute
- `Templates` class to manage templates
- `RecipientLists` class to manage recipients we want to send to
- `SuppressionLists` class to manage recipients that are suppressed

### Changed
- Renamed `Transmission` class to `Transmissions` (backwards compatible)

### Removed
- Tox file for running tests in favor of `make test` and Travis CI

### Fixed
- Engagement tracking no longer automatically enabled for all transmissions
- Documentation generation issues

## 1.0.0.dev1 - 2014-02-09
### Added
- Base SparkPost class
- `Transmission` class for sending messages
- Examples for Transmission usage
- Metrics class for getting a list of campaigns and domains
- Docs on readthedocs.org

[unreleased]: https://github.com/sparkpost/python-sparkpost/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/sparkpost/python-sparkpost/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/sparkpost/python-sparkpost/compare/1.0.0.dev2...v1.0.0
[1.0.0.dev2]: https://github.com/sparkpost/python-sparkpost/compare/1.0.0.dev1...1.0.0.dev2
[coveralls]: https://coveralls.io/github/SparkPost/python-sparkpost
