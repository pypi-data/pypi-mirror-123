# Changelog

This file contains the changes made between released versions.

The format is based on [Keep a changelog](https://keepachangelog.com/) and the versioning tries to follow
[Semantic Versioning](https://semver.org).

## 0.2.0
### Added
- Indexer that applies rules to the fulltext of a document to extract meta data
- OCR support
- YAML style metadata files are supported
- Indexer addons

### Changed
- API for `Indexer` changed slightly
- `stores.get`, `stores.get_for_collection` accept byte streams, too

### Removed
- `add`, `remove`, and `edit` commandline parameters are gone. Use
  metaindexmanager for these functions instead


## 0.1.0
- Initial release

