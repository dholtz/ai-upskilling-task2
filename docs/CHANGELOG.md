# Changelog

All notable changes to this template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial Flask application template
- Docker setup with corporate certificate support
- Makefile with common commands
- Project structure (routes, models, utils)
- Security best practices (.gitignore, SECURITY.md)
- Health check endpoints
- Environment variable configuration
- Comprehensive documentation (README, LOCAL_SETUP, TEMPLATE_USAGE)
- Setup script for new projects with environment variable support
  - Supports command-line arguments, environment variables, or .setup.env file
  - Automatically updates app.py and README.md with project details
  - Cross-platform compatible (macOS and Linux)
- Pre-commit security checks

### Features
- Flask 3.1+ with blueprint architecture
- Gunicorn for production deployment
- Python-decouple for environment variables
- Dockerized with Python 3.9
- Corporate certificate handling (Zscaler)
- Health check endpoints
- Example API endpoints
- Security scanning tools

### Documentation
- README.md - Main project documentation
- docs/LOCAL_SETUP.md - Local development guide
- docs/SECURITY.md - Security best practices
- docs/TEMPLATE_USAGE.md - How to use this template
- docs/CHANGELOG.md - This file

---

## Template Version History

### Version 1.0.0
Initial release of the AI upskilling program template.

**For course participants**: This is the baseline template. Use it as a starting point for your projects.

**For instructors**: This template can be updated and versioned. Tag releases when making improvements.

