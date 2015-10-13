# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]
- No notable updates

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

[unreleased]: https://github.com/sparkpost/python-sparkpost/compare/1.0.0.dev2...HEAD
[1.0.0.dev2]: https://github.com/sparkpost/python-sparkpost/compare/1.0.0.dev1...1.0.0.dev2
[coveralls]: https://coveralls.io/github/SparkPost/python-sparkpost


Added for new features.
Changed for changes in existing functionality.
Deprecated for once-stable features removed in upcoming releases.
Removed for deprecated features removed in this release.
Fixed for any bug fixes.
Security
