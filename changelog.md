# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-07-06

### Added

- Initial satellite package for Pumpwood static page containers on
  Kubernetes.
- ``PumpWoodStaticPagesMicroservice`` to render Deployment and Service
  manifests for one static page image per instance.
- YAML template ``deploy__app.yml`` with ClusterIP Service on port 80.
- README with quick start, configuration reference, and prerequisites.

### Changed

- Package metadata aligned to ``pumpwood-deploy-static-pages`` and module
  ``pumpwood_deploy_static_pages`` (replacing incorrect datalake
  scaffolding from the repository bootstrap).

### Fixed

- Service ``targetPort`` aligned with container port 80.
- Broken ``deploy.py`` syntax and datalake-only manifest logic removed.

### Removed

- Datalake worker, secrets, and database deployment references from the
  package API.
