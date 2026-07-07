# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-07-07

### Added

- Initial satellite package for Pumpwood RabbitMQ-backed simple task workers
  on Kubernetes.
- **`PumpWoodSimpleTasksMicroservice`**: renders per-image Secret and
  Deployment manifests for task containers without cloud storage access.
- **`PumpWoodSimpleTasksWithStorageMicroservice`**: same Kubernetes
  resources with storage env vars, volumes, and credential mounts for
  tasks that read project buckets.
- Kubernetes resource templates:
  - ``secrets.yml`` — per-task microservice credentials
  - ``deploy__task.yml`` — base task Deployment
  - ``deploy__task_storage.yml`` — storage-enabled task Deployment
- README with quick start, configuration reference, prerequisites, and
  deployment flow diagram.
- Project scaffolding: ``build.sh``, ``pyproject.toml``, generated API
  documentation under ``docs/``, and Google Style module docstrings.

### Changed

- No changes.

### Removed

- No removes.
