"""Various indexers for common formats"""
import logging
import datetime
import io
import zipfile
import re

import multidict

try:
    import pyexiv2
except ImportError:
    pyexiv2 = None

try:
    import PIL
    import PIL.Image
except ImportError:
    PIL = None

try:
    import mutagen
except ImportError:
    mutagen = None

try:
    import pdfminer
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
except ImportError:
    pdfminer = None

from metaindex.indexer import registered_indexer, to_utf8, Indexer, Order
from metaindex.opf import parse_opf
from metaindex.ruleindexer import RuleIndexer


if pyexiv2 is not None:
    @registered_indexer
    class Exiv2Indexer(Indexer):
        NAME = 'exiv2'
        ACCEPT = ['image/', 'video/']

        def run(self, path, info):
            logging.debug(f"[image, exiv2] processing {path.name}")

            try:
                meta = pyexiv2.core.Image(str(path))
            except:
                return False, {}

            result = multidict.MultiDict()
            try:
                result.extend(meta.read_exif())
            except:
                pass

            try:
                result.extend(meta.read_iptc())
            except:
                pass

            try:
                result.extend(meta.read_xmp())
            except:
                pass

            meta.close()
            return True, result


if mutagen is not None:
    @registered_indexer
    class MutagenIndexer(Indexer):
        NAME = 'mutagen'
        ACCEPT = ['audio/', 'video/']

        def run(self, path, info):
            logging.debug(f"[mutagen] processing {path.name}")

            try:
                meta = mutagen.File(path, easy=True)
            except:
                return False, {}

            result = multidict.MultiDict()

            if meta is not None:
                for key in meta.keys():
                    result.extend([('id3.' + key, value) for value in meta[key]])
                if hasattr(meta, 'info') and hasattr(meta.info, 'length'):
                    result.add('length', meta.info.length)

            return True, result


if PIL is not None:
    @registered_indexer
    class PillowIndexer(Indexer):
        NAME = 'pillow'
        ACCEPT = ['image/']

        def run(self, path, info):
            logging.debug(f"[image, pillow] processing {path.name}")

            try:
                meta = PIL.Image.open(path)
            except:
                return False, {}

            result = {}
            if meta is not None:
                result = {'resolution': "{}x{}".format(*meta.size)}
                if self.should_ocr(path):
                    ocr = self.ocr.run(meta)
                    if ocr.success:
                        result['ocr.language'] = ocr.language
                        if self.should_fulltext(path):
                            result['ocr.fulltext'] = ocr.fulltext
                meta.close()

            return True, result


if pdfminer is not None:
    @registered_indexer
    class PdfMinerIndexer(Indexer):
        NAME = 'pdfminer'
        ACCEPT = ['application/pdf']

        PDF_METADATA = ('title', 'author', 'creator', 'producer', 'keywords',
                        'manager', 'status', 'category', 'moddate', 'creationdate',
                        'subject')

        def run(self, path, info):
            logging.debug(f"[pdf] processing {path.name}")

            try:
                fp = open(path, 'rb')
            except OSError:
                return False, {}

            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.converter import PDFConverter
            from pdfminer.pdfpage import PDFPage
            from pdfminer.layout import LTImage, LTPage, LTFigure

            run_ocr = self.ocr.run
            ocr_result = [False]

            class MyImageReader(PDFConverter):
                def __init__(self, output, rdmngr, **kwargs):
                    super().__init__(rdmngr, io.BytesIO(), **kwargs)
                    self.output = output
                    self.output.append(False)
                    self.output.append("")
                    self.output.append("")

                def receive_layout(self, ltpage):
                    if isinstance(ltpage, (LTFigure, LTPage)):
                        for obj in ltpage:
                            self.receive_layout(obj)
                    if isinstance(ltpage, LTImage):
                        try:
                            self.ocr_pdf_page(ltpage.stream)
                        except Exception as exc:
                            logging.error(f"[pdf] Could not run OCR on image from PDF: {exc}")

                def ocr_pdf_page(self, stream):
                    img_ = PIL.Image.open(io.BytesIO(stream.get_rawdata()))

                    result = run_ocr(img_)
                    if result.success:
                        self.output[0] = True
                        self.output[1] = result.language
                        self.output[2] += result.fulltext + "\n"

            # basic document info
            try:
                parser = PDFParser(fp)
                pdf = PDFDocument(parser)
            except:
                fp.close()
                return False, {}

            if self.should_ocr(path):
                # OCR every image
                rmngr = PDFResourceManager(caching=True)
                device = MyImageReader(ocr_result, rmngr)
                interpreter = PDFPageInterpreter(rmngr, device)
                try:
                    for page in PDFPage.get_pages(fp, set()):
                        interpreter.process_page(page)
                except Exception as exc:
                    logging.error(f"[pdf] OCR in PDF died: {exc}")

            result = multidict.MultiDict()

            if ocr_result[0]:
                result.add('ocr.language', ocr_result[1])
                if self.should_fulltext(path):
                    result.add('ocr.fulltext', ocr_result[2])

            if len(pdf.info) > 0:
                for field in pdf.info[0].keys():
                    if not isinstance(field, str):
                        logging.debug(f"PDF: Unexpected type for info field key: {type(field)}")
                        continue
                    if field.lower() not in self.PDF_METADATA:
                        logging.debug(f"PDF: Ignoring {field} key")
                        continue

                    raw = pdf.info[0][field]
                    value = None

                    if isinstance(raw, bytes):
                        value = to_utf8(raw)
                        if value is None:
                            continue
                    elif isinstance(raw, str) and len(raw.strip()) > 0:
                        value = raw.strip()
                    else:
                        continue

                    if field.endswith('Date') and value.startswith(':'):
                        try:
                            value = datetime.datetime.strptime(value[:15], ':%Y%m%d%H%M%S')
                        except ValueError:
                            continue

                    if value is not None:
                        result['pdf.' + field] = value

            fp.close()
            return True, result


@registered_indexer
class EpubIndexer(Indexer):
    NAME = 'epub'
    ACCEPT = ['application/epub+zip']

    def run(self, path, info):
        logging.debug(f"[epub] processing {path.name}")

        with zipfile.ZipFile(path) as fp:
            files = fp.namelist()
            if 'content.opf' in files:
                with fp.open('content.opf') as contentfp:
                    return True, parse_opf(contentfp.read(), '')
        return False, {}


@registered_indexer
class FileTagsIndexer(Indexer):
    NAME = 'filetags'
    ACCEPT = '*'

    TAG_MARKER = ' -- '
    DATE_PATTERN = (re.compile(r'^([0-9]+)-([01][0-9])-([0-3][0-9])'), 10)
    DATE2_PATTERN = (re.compile(r'^([0-9]+)([01][0-9])([0-3][0-9])'), 8)
    DATETIME_PATTERN = (re.compile(r'^([0-9]+)-([01][0-9])-([0-3][0-9])[T_]([0-2][0-9])[._-]([0-6][0-9])'), 16)
    DATETIME2_PATTERN = (re.compile(r'^([0-9]+)([01][0-9])([0-3][0-9])_([0-2][0-9])([0-6][0-9])'), 13)
    DATETIMESEC_PATTERN = (re.compile(r'^([0-9]+)-([01][0-9])-([0-3][0-9])[T_]([0-2][0-9])[._-]([0-6][0-9])[._-]([0-6][0-9])'), 19)
    DATETIMESEC2_PATTERN = (re.compile(r'^([0-9]+)([01][0-9])([0-3][0-9])_([0-2][0-9])([0-6][0-9])([0-6][0-9])'), 15)

    def run(self, path, info):
        logging.debug(f"[filetags] Running {path.stem}")
        result = set()
        counter = 0

        success, result = self.extract_metadata(path.stem)

        while path.parent != path:
            path = path.parent
            counter += 1

            if counter > 1:
                break

            success, tags = self.extract_metadata(path.stem)
            result |= {(tag, value) for tag, value in tags if tag in [self.NAME + '.date', self.NAME + '.tags']}

        return len(result) > 0, multidict.MultiDict(list(result))

    def extract_metadata(self, text):
        result = set()
        tags = None

        match, text = self.obtain_datetime(text)

        if match:
            result.add((self.NAME + '.date', match))

        if match and text.startswith('--'):
            _, text = self.obtain_datetime(text[2:])
            # TODO: do something useful with the end part of the range

        if self.TAG_MARKER in text:
            text, tags = text.split(self.TAG_MARKER, 1)
            result |= {(self.NAME + '.tags', tag) for tag in tags.split()}

        if tags is not None or match is not None:
            if text.startswith('-'):
                text = text[1:]
            result.add((self.NAME + '.title', text))

        return len(result) > 0, result

    def obtain_datetime(self, text):
        match = None
        patterns = [
            self.DATETIMESEC_PATTERN,
            self.DATETIMESEC2_PATTERN,
            self.DATETIME_PATTERN,
            self.DATE_PATTERN,
            self.DATE2_PATTERN,
        ]

        for pattern, length in patterns:
            if len(text) < length:
                continue

            match = pattern.match(text)
            if not match:
                continue

            try:
                match = datetime.datetime(*[int(value) for value in match.groups()])
                text = text[length:]
                break
            except ValueError:
                match = None
                continue

        return match, text

