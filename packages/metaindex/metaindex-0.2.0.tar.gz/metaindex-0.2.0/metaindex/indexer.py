import codecs
import datetime
import pathlib
import mimetypes
import multiprocessing
import logging
import zipfile

import multidict

from metaindex import ocr
from metaindex import configuration


_registered_indexers = {}
_indexer_by_suffix = {}
_indexer_by_mimetype = {}
_generic_indexers = []

ocr_facility = ocr.Dummy()
app_config = configuration.Configuration()


class Order:
    FIRST = 100
    EARLY = 250
    AVERAGE = 500
    LATE = 750
    LAST = 1000


class Indexer:
    # specify what suffices or mimetypes are handled by this indexer, e.g.
    # ACCEPT = ['.rst', '.md', 'text/html', 'image/']
    # anything starting with a . is expected to be a suffix,
    # everything else is expected to be a mimetype.
    # If the mimetype ends with /, it is matched against the first part
    # of the file's mimetype
    # If your indexer should run for all files, use ACCEPT = '*'
    ACCEPT = []
    # When to execute this indexer in the order of indexers
    ORDER = Order.AVERAGE

    def __init__(self, ocr, fulltext, config):
        """Create a new indexer with this configuration

        ocr: the OCR facility to use (e.g. metaindex.ocr.Dummy)
        fulltext: whether or not to extract the fulltext
        """
        self.ocr = ocr
        self.fulltext = fulltext
        self.config = config

    def should_ocr(self, path):
        return self._check_match(self.ocr.accept_list, path)

    def should_fulltext(self, path):
        return self._check_match(self.fulltext, path)

    def _check_match(self, acceptor, path):
        if not isinstance(acceptor, list):
            return bool(acceptor)

        if self.NAME in acceptor:
            return True

        for item in acceptor:
            if item.startswith('.') and path.suffix.lower() == item.lower():
                return True
            if '/' in item:
                mimetype, _ = mimetypes.guess_type(path.name, strict=False)
                if mimetype.lower().startswith(item.lower()):
                    return True

        return False

    def __lt__(self, other):
        return self.ORDER < other.ORDER

    def run(self, path, info):
        """Execute this Indexer to run on the file at path.

        ``info`` is the previously collected metadata as a multidict this is
        purely informative and should not be returned.

        Return the tuple (success, metadata). success being True or False,
        metadata being a multidict.Multidict or a dict.

        path will be of type pathlib.Path.

        Be aware that each subprocess will create their own instance of the
        Indexer.
        """
        raise NotImplementedError()


def registered_indexer(cls):
    assert issubclass(cls, Indexer)
    
    global _registered_indexers
    global _indexer_by_suffix
    global _indexer_by_mimetype
    global _generic_indexers

    assert cls.NAME not in _registered_indexers
    _registered_indexers[cls.NAME] = cls

    if isinstance(cls.ACCEPT, str) and cls.ACCEPT == '*':
        _generic_indexers.append(cls.NAME)
    else:
        for pattern in cls.ACCEPT:
            pattern = pattern.lower()

            if pattern.startswith('.') and len(pattern) > 1:
                if pattern not in _indexer_by_suffix:
                    _indexer_by_suffix[pattern] = []
                _indexer_by_suffix[pattern].append(cls.NAME)

            elif len(pattern) > 0:
                if pattern.endswith('/') and len(pattern) > 1:
                    pattern = pattern[:-1]
                if pattern not in _indexer_by_mimetype:
                    _indexer_by_mimetype[pattern] = []
                _indexer_by_mimetype[pattern].append(cls.NAME)

    return cls


def remove_indexers(names):
    global _registered_indexers
    global _indexer_by_suffix
    global _indexer_by_mimetype
    global _generic_indexers

    if len(names) == 0:
        return

    for name in names:
        if name in _registered_indexers:
            del _registered_indexers[name]

    _indexer_by_suffix = dict([(key, [value for value in values if value not in names])
                               for key, values in _indexer_by_suffix.items()])
    _indexer_by_mimetype = dict([(key, [value for value in values if value not in names])
                                 for key, values in _indexer_by_mimetype.items()])
    _generic_indexers = [value for value in _generic_indexers if value not in names]


def to_utf8(raw):
    if isinstance(raw, str):
        return raw
    encoding = None
    skip = 1

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8'
    elif raw.startswith(codecs.BOM_UTF16_BE):
        encoding = 'utf-16-be'
    elif raw.startswith(codecs.BOM_UTF16_LE):
        encoding = 'utf-16-le'
    elif raw.startswith(codecs.BOM_UTF32_BE):
        encoding = 'utf-32-be'
    elif raw.startswith(codecs.BOM_UTF32_LE):
        encoding = 'utf-32-le'
    else:
        # just best efford
        encoding = 'utf-8'
        skip = 0

    try:
        text = str(raw, encoding=encoding).strip()
        return text[skip:]  # drop the BOM, if applicable
    except UnicodeError:
        pass
    return None


class IndexerCache:
    def __init__(self, ocr, fulltext, config):
        self.cached = {}
        self.ocr = ocr
        self.fulltext = fulltext
        self.config = config

    def get(self, name):
        if name not in self.cached:
            self.cached[name] = _registered_indexers[name](self.ocr, self.fulltext, self.config)
        return self.cached[name]


def get_metadata(filename, indexer_cache):
    """Extract metadata from the file at `filename`"""
    assert isinstance(filename, pathlib.Path)

    global ocr_facility
    global obtain_fulltext
    global app_config

    logging.error(f"Going for {filename}")

    if indexer_cache is None:
        indexer_cache = IndexerCache(ocr=ocr_facility,
                                     fulltext=obtain_fulltext,
                                     config=app_config)

    stat = filename.stat()
    suffix = filename.suffix[1:]
    mimetype, _ = mimetypes.guess_type(filename, strict=False)
    info = multidict.MultiDict({'size': stat.st_size,
                                'filename': filename.name,
                                'last_accessed': datetime.datetime.fromtimestamp(stat.st_atime),
                                'last_modified': datetime.datetime.fromtimestamp(stat.st_mtime)})

    if mimetype is None:
        logging.debug(f"Unknown mimetype for {suffix}")
        return False, info

    info['mimetype'] = mimetype
    applied_indexers = 0
    indexers = _generic_indexers[:] \
             + _indexer_by_suffix.get(filename.suffix.lower(), [])
    for mtype in [mimetype, mimetype.split('/', 1)[0]]:
        indexers += _indexer_by_mimetype.get(mtype, [])

    for handler in sorted([indexer_cache.get(indexer) for indexer in indexers]):
        logging.error(f"... running {handler}")
        success, extra = handler.run(filename, info.copy())
        if success:
            applied_indexers += 1
            info.extend(extra)

    success = applied_indexers > 0
    return success, info


def indexer(filenames):
    """Takes a list of filenames and tries to extract the metadata for all
    
    Returns a dictionary mapping filename to a dictionary with the metadata.
    """
    global ocr_facility
    global obtain_fulltext
    global app_config

    indexer_cache = IndexerCache(ocr_facility, obtain_fulltext, app_config)
    for name in _registered_indexers.keys():
        # pre-load all
        indexer_cache.get(name)

    result = []

    for filename in filenames:
        if not isinstance(filename, pathlib.Path):
            filename = pathlib.Path(filename)

        if not filename.is_file():
            continue

        success, info = get_metadata(filename, indexer_cache)

        result.append((filename, success, info))

    return result


def find_files(paths, recursive=True):
    """Find all files in these paths"""
    if not isinstance(paths, list):
        paths = [paths]

    pathqueue = list(paths)
    filenames = []

    while len(pathqueue) > 0:
        path = pathqueue.pop(0)

        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)

        if not path.exists():
            continue

        for item in path.iterdir():
            if item.is_dir() and recursive:
                pathqueue.append(item)
                continue

            if item.is_file():
                filenames.append(item)

    return filenames


def tuplice(item):
    success, info = get_metadata(item, None)
    return item, success, info


def index_files(files, processes=None, ocr=None, fulltext=False, config=None):
    """Run indexer on all files"""
    global ocr_facility
    global obtain_fulltext
    global app_config

    if ocr is not None:
        ocr_facility = ocr
    app_config = config or configuration.Configuration()
    obtain_fulltext = fulltext

    metadata = {}
    then = datetime.datetime.now()
    if processes == 1:
        index_result = indexer(files)
    else:
        with multiprocessing.Pool(processes) as pool:
            index_result = pool.map(tuplice, files)

    logging.info(f"Processed {len(metadata)} files in {datetime.datetime.now() - then}")

    return index_result


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG)

    index = index_files([pathlib.Path(i).expanduser() for i in sys.argv[1:]])

