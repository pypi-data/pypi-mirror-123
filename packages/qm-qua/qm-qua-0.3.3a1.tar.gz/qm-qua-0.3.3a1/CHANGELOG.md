# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- :guardswoman: Define an analog port with delay.
- New `set_dc_offset()` statement that can change the DC offset of element input in real time
- New input stream capabilities facilitating data transfer from job to QUA.
- Docs - Add information about demod on a tuple 
- Docs - Added best practice guide

## [0.3.2] - 2021-10-03
### Added
- :guardswoman: QuantumMachinesManager health check shows errors and warnings.
- :guardswoman: Fetching job results indicates if there were execution errors.
- :guardswoman: Define an element with multiple input ports.
- :guardswoman: Stream processing demod now supports named argument `integrate`. If `False` is provided
the demod will not sum the items, but only multiply by weights
### Changed
- Documentation structure and content

## [0.3.1] - 2021-09-13
### Fixed
- Fixed serialization of IO values.
- Support running `QuantumMachinesManager` inside ipython or jupyter notebook.
### Changed
- Removing deprecation notice from `with_timestamps` method on result streams.
- Setting `time_of_flight` or `smearing` are required if element has `outputs` and
must not appear if it does not.

## [0.3.0] - 2021-09-03
### Changed
- Support for result fetching of both versions of QM Server.
- Now the SDK supports all version of QM server.

## [0.2.1] - 2021-09-01
### Changed
- Default port when creating new `QuantumMachineManager` is now `80` and user 
config file is ignored.

## [0.2.0] - 2021-08-31
### Added
- The original QM SDK for QOP 2.

## [0.1.0] - 2021-08-31
### Added
- The original QM SDK for QOP 1.

[Unreleased]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/qm-labs/qm-qua-sdk/releases/tag/v0.1.0

## Legend 
* :guardswoman: Features that are server specific and depend on capabilities and version