# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Fixed

### Changed

### Removed

## [0.15.0] - 2025-07-11

### Changed
- The command `write-population-status` is responsible to post the file content and write to disk the response.
- Refactor `write-population-status` command to use HTTP POST with multipart/form-data, aligning with the updated API endpoint. Now sends the CSV as a file and receives JSON in response.

## [0.14.0] - 2025-01-15

### Added

- Add command,`write-population-status-from-mixed-methods`, for a entrypoint from `eradication_data_requirements` api.

## [0.13.0] - 2024-10-30

### Added

- Add command,`write-bootstrap-progress-intervals`, for a entrypoint from `eradication_data_requirements` api.

## [0.12.0] - 2024-09-23

### Added

- Add command,`write-aerial-monitoring`, for a entrypoint from `eradication_data_requirements` api.

## [0.11.0] - 2024-09-17

### Added

- Add command,`filter-by-method`, for a entrypoint from `eradication_data_requirements` api.

## [0.10.1] - 2024-09-17

### Fixed

- Fix command argument `bootstrapping-number` for `write-population-status`.

## [0.10.0] - 2024-09-13

### Added

- Add command,`write-population-status`, for a entrypoint from `eradication_data_requirements` api.

## [0.9.0] - 2024-07-27

### Added

- Add command,`plot-custom-cpue-vs-cum-captures`, for a entrypoint from `eradication_data_requirements` api.

## [0.8.0] - 2024-07-17

### Added

- Add command,`plot-cumulative-series-cpue-by-flight`, for a entrypoint from `eradication_data_requirements` api.

## [0.7.0] - 2023-10-12

### Added

- Add one command,`plot-comparative-catch-curves`, for one entrypoint from `eradication_data_requirements` api.

## [0.6.0] - 2023-10-10

### Added

- Add one command,`plot-cpue-vs-cum-captures`, for one entrypoint from `eradication_data_requirements` api.

## [0.5.0] - 2023-09-27

### Added

- Add two command,`write-csv-probability` `write-probability-progress-figure`, for two entrypoints from `eradication_data_requirements` api.

## [0.4.0] - 2023-08-31


[unreleased]: https://github.com/IslasGECI/api_caller/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/IslasGECI/api_caller/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/IslasGECI/api_caller/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/IslasGECI/api_caller/tag/v0.4.0
