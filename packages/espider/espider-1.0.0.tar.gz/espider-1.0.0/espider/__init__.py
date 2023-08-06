# -*- coding: utf-8 -*-
"""Beautiful Soup bonus library: Unicode, Dammit

This library converts a bytestream to Unicode through any means
necessary. It is heavily based on code from Mark Pilgrim's Universal
Feed Parser. It works best on XML and HTML, but it does not rewrite the
XML or HTML to reflect a new encoding; that's the tree builder's job.
"""
# Use of this source code is governed by the MIT license.
__license__ = "MIT"

import codecs
import re
import logging
import typing
import sys
import os

# Import a library to autodetect character encodings.
chardet_type = None
try:
    # First try the fast C implementation.
    #  PyPI package: cchardet
    import cchardet


    def chardet_dammit(s):
        if isinstance(s, str):
            return None
        return cchardet.detect(s)['encoding']
except ImportError:
    try:
        # Fall back to the pure Python implementation
        #  Debian package: python-chardet
        #  PyPI package: chardet
        import chardet


        def chardet_dammit(s):
            if isinstance(s, str):
                return None
            return chardet.detect(s)['encoding']
        # import chardet.constants
        # chardet.constants._debug = 1
    except ImportError:
        # No chardet available.
        def chardet_dammit(s):
            return None

# Available from http://cjkpython.i18n.org/.
#
# TODO: This doesn't work anymore and the closest thing, iconv_codecs,
# is GPL-licensed. Check whether this is still necessary.
try:
    import iconv_codec
except ImportError:
    pass

# Build bytestring and Unicode versions of regular expressions for finding
# a declared encoding inside an XML or HTML document.
xml_encoding = '^\\s*<\\?.*encoding=[\'"](.*?)[\'"].*\\?>'
html_meta = '<\\s*meta[^>]+charset\\s*=\\s*["\']?([^>]*?)[ /;\'">]'
encoding_res = dict()
encoding_res[bytes] = {
    'html': re.compile(html_meta.encode("ascii"), re.I),
    'xml': re.compile(xml_encoding.encode("ascii"), re.I),
}
encoding_res[str] = {
    'html': re.compile(html_meta, re.I),
    'xml': re.compile(xml_encoding, re.I)
}


class EncodingDetector:
    """Suggests a number of possible encodings for a bytestring.

    Order of precedence:

    1. Encodings you specifically tell EncodingDetector to try first
    (the override_encodings argument to the constructor).

    2. An encoding declared within the bytestring itself, either in an
    XML declaration (if the bytestring is to be interpreted as an XML
    document), or in a <meta> tag (if the bytestring is to be
    interpreted as an HTML document.)

    3. An encoding detected through textual analysis by chardet,
    cchardet, or a similar external library.

    4. UTF-8.

    5. Windows-1252.
    """

    def __init__(self, markup, override_encodings=None, is_html=False,
                 exclude_encodings=None):
        """Constructor.

        :param markup: Some markup in an unknown encoding.
        :param override_encodings: These encodings will be tried first.
        :param is_html: If True, this markup is considered to be HTML. Otherwise
            it's assumed to be XML.
        :param exclude_encodings: These encodings will not be tried, even
            if they otherwise would be.
        """
        self.override_encodings = override_encodings or []
        exclude_encodings = exclude_encodings or []
        self.exclude_encodings = set([x.lower() for x in exclude_encodings])
        self.chardet_encoding = None
        self.is_html = is_html
        self.declared_encoding = None

        # First order of business: strip a byte-order mark.
        self.markup, self.sniffed_encoding = self.strip_byte_order_mark(markup)

    def _usable(self, encoding, tried):
        """Should we even bother to try this encoding?

        :param encoding: Name of an encoding.
        :param tried: Encodings that have already been tried. This will be modified
            as a side effect.
        """
        if encoding is not None:
            encoding = encoding.lower()
            if encoding in self.exclude_encodings:
                return False
            if encoding not in tried:
                tried.add(encoding)
                return True
        return False

    @property
    def encodings(self):
        """Yield a number of encodings that might work for this markup.

        :yield: A sequence of strings.
        """
        tried = set()
        for e in self.override_encodings:
            if self._usable(e, tried):
                yield e

        # Did the document originally start with a byte-order mark
        # that indicated its encoding?
        if self._usable(self.sniffed_encoding, tried):
            yield self.sniffed_encoding

        # Look within the document for an XML or HTML encoding
        # declaration.
        if self.declared_encoding is None:
            self.declared_encoding = self.find_declared_encoding(
                self.markup, self.is_html)
        if self._usable(self.declared_encoding, tried):
            yield self.declared_encoding

        # Use third-party character set detection to guess at the
        # encoding.
        if self.chardet_encoding is None:
            self.chardet_encoding = chardet_dammit(self.markup)
        if self._usable(self.chardet_encoding, tried):
            yield self.chardet_encoding

        # As a last-ditch effort, try utf-8 and windows-1252.
        for e in ('utf-8', 'windows-1252'):
            if self._usable(e, tried):
                yield e

    @classmethod
    def strip_byte_order_mark(cls, data):
        """If a byte-order mark is present, strip it and return the encoding it implies.

        :param data: Some markup.
        :return: A 2-tuple (modified data, implied encoding)
        """
        encoding = None
        if isinstance(data, str):
            # Unicode data cannot have a byte-order mark.
            return data, encoding
        if (len(data) >= 4) and (data[:2] == b'\xfe\xff') \
                and (data[2:4] != '\x00\x00'):
            encoding = 'utf-16be'
            data = data[2:]
        elif (len(data) >= 4) and (data[:2] == b'\xff\xfe') \
                and (data[2:4] != '\x00\x00'):
            encoding = 'utf-16le'
            data = data[2:]
        elif data[:3] == b'\xef\xbb\xbf':
            encoding = 'utf-8'
            data = data[3:]
        elif data[:4] == b'\x00\x00\xfe\xff':
            encoding = 'utf-32be'
            data = data[4:]
        elif data[:4] == b'\xff\xfe\x00\x00':
            encoding = 'utf-32le'
            data = data[4:]
        return data, encoding

    @classmethod
    def find_declared_encoding(cls, markup, is_html=False, search_entire_document=False):
        """Given a document, tries to find its declared encoding.

        An XML encoding is declared at the beginning of the document.

        An HTML encoding is declared in a <meta> tag, hopefully near the
        beginning of the document.

        :param markup: Some markup.
        :param is_html: If True, this markup is considered to be HTML. Otherwise
            it's assumed to be XML.
        :param search_entire_document: Since an encoding is supposed to declared near the beginning
            of the document, most of the time it's only necessary to search a few kilobytes of data.
            Set this to True to force this method to search the entire document.
        """
        if search_entire_document:
            xml_endpos = html_endpos = len(markup)
        else:
            xml_endpos = 1024
            html_endpos = max(2048, int(len(markup) * 0.05))

        if isinstance(markup, bytes):
            res = encoding_res[bytes]
        else:
            res = encoding_res[str]

        xml_re = res['xml']
        html_re = res['html']
        declared_encoding = None
        declared_encoding_match = xml_re.search(markup, endpos=xml_endpos)
        if not declared_encoding_match and is_html:
            declared_encoding_match = html_re.search(markup, endpos=html_endpos)
        if declared_encoding_match is not None:
            declared_encoding = declared_encoding_match.groups()[0]
        if declared_encoding:
            if isinstance(declared_encoding, bytes):
                declared_encoding = declared_encoding.decode('ascii', 'replace')
            return declared_encoding.lower()
        return None


class UnicodeDammit:
    """A class for detecting the encoding of a *ML document and
    converting it to a Unicode string. If the source encoding is
    windows-1252, can replace MS smart quotes with their HTML or XML
    equivalents."""

    # This dictionary maps commonly seen values for "charset" in HTML
    # meta tags to the corresponding Python codec names. It only covers
    # values that aren't in Python's aliases and can't be determined
    # by the heuristics in find_codec.
    CHARSET_ALIASES = {"macintosh": "mac-roman",
                       "x-sjis": "shift-jis"}

    ENCODINGS_WITH_SMART_QUOTES = [
        "windows-1252",
        "iso-8859-1",
        "iso-8859-2",
    ]

    def __init__(self, markup, override_encodings=[],
                 smart_quotes_to=None, is_html=False, exclude_encodings=[]):
        """Constructor.

        :param markup: A bytestring representing markup in an unknown encoding.
        :param override_encodings: These encodings will be tried first,
           before any sniffing code is run.

        :param smart_quotes_to: By default, Microsoft smart quotes will, like all other characters, be converted
           to Unicode characters. Setting this to 'ascii' will convert them to ASCII quotes instead.
           Setting it to 'xml' will convert them to XML entity references, and setting it to 'html'
           will convert them to HTML entity references.
        :param is_html: If True, this markup is considered to be HTML. Otherwise
            it's assumed to be XML.
        :param exclude_encodings: These encodings will not be considered, even
            if the sniffing code thinks they might make sense.
        """
        self.smart_quotes_to = smart_quotes_to
        self.tried_encodings = []
        self.contains_replacement_characters = False
        self.is_html = is_html
        self.log = logging.getLogger(__name__)
        self.detector = EncodingDetector(
            markup, override_encodings, is_html, exclude_encodings)

        # Short-circuit if the data is in Unicode to begin with.
        if isinstance(markup, str) or markup == '':
            self.markup = markup
            self.unicode_markup = str(markup)
            self.original_encoding = None
            return

        # The encoding detector may have stripped a byte-order mark.
        # Use the stripped markup from this point on.
        self.markup = self.detector.markup

        u = None
        for encoding in self.detector.encodings:
            markup = self.detector.markup
            u = self._convert_from(encoding)
            if u is not None:
                break

        if not u:
            # None of the encodings worked. As an absolute last resort,
            # try them again with character replacement.

            for encoding in self.detector.encodings:
                if encoding != "ascii":
                    u = self._convert_from(encoding, "replace")
                if u is not None:
                    self.log.warning(
                        "Some characters could not be decoded, and were "
                        "replaced with REPLACEMENT CHARACTER."
                    )
                    self.contains_replacement_characters = True
                    break

        # If none of that worked, we could at this point force it to
        # ASCII, but that would destroy so much data that I think
        # giving up is better.
        self.unicode_markup = u
        if not u:
            self.original_encoding = None

    def _sub_ms_char(self, match):
        """Changes a MS smart quote character to an XML or HTML
        entity, or an ASCII character."""
        orig = match.group(1)
        if self.smart_quotes_to == 'ascii':
            sub = self.MS_CHARS_TO_ASCII.get(orig).encode()
        else:
            sub = self.MS_CHARS.get(orig)
            if type(sub) == tuple:
                if self.smart_quotes_to == 'xml':
                    sub = '&#x'.encode() + sub[1].encode() + ';'.encode()
                else:
                    sub = '&'.encode() + sub[0].encode() + ';'.encode()
            else:
                sub = sub.encode()
        return sub

    def _convert_from(self, proposed, errors="strict"):
        """Attempt to convert the markup to the proposed encoding.

        :param proposed: The name of a character encoding.
        """
        proposed = self.find_codec(proposed)
        if not proposed or (proposed, errors) in self.tried_encodings:
            return None
        self.tried_encodings.append((proposed, errors))
        markup = self.markup
        # Convert smart quotes to HTML if coming from an encoding
        # that might have them.
        if (self.smart_quotes_to is not None
                and proposed in self.ENCODINGS_WITH_SMART_QUOTES):
            smart_quotes_re = b"([\x80-\x9f])"
            smart_quotes_compiled = re.compile(smart_quotes_re)
            markup = smart_quotes_compiled.sub(self._sub_ms_char, markup)

        try:
            # print("Trying to convert document to %s (errors=%s)" % (
            #    proposed, errors))
            u = self._to_unicode(markup, proposed, errors)
            self.markup = u
            self.original_encoding = proposed
        except Exception as e:
            # print("That didn't work!")
            # print(e)
            return None
        # print("Correct encoding: %s" % proposed)
        return self.markup

    def _to_unicode(self, data, encoding, errors="strict"):
        """Given a string and its encoding, decodes the string into Unicode.

        :param encoding: The name of an encoding.
        """
        return str(data, encoding, errors)

    @property
    def declared_html_encoding(self):
        """If the markup is an HTML document, returns the encoding declared _within_
        the document.
        """
        if not self.is_html:
            return None
        return self.detector.declared_encoding

    def find_codec(self, charset):
        """Convert the name of a character set to a codec name.

        :param charset: The name of a character set.
        :return: The name of a codec.
        """
        value = (self._codec(self.CHARSET_ALIASES.get(charset, charset))
                 or (charset and self._codec(charset.replace("-", "")))
                 or (charset and self._codec(charset.replace("-", "_")))
                 or (charset and charset.lower())
                 or charset
                 )
        if value:
            return value.lower()
        return None

    def _codec(self, charset):
        if not charset:
            return charset
        codec = None
        try:
            codecs.lookup(charset)
            codec = charset
        except (LookupError, ValueError):
            pass
        return codec

    # A partial mapping of ISO-Latin-1 to HTML entities/XML numeric entities.
    MS_CHARS = {b'\x80': ('euro', '20AC'),
                b'\x81': ' ',
                b'\x82': ('sbquo', '201A'),
                b'\x83': ('fnof', '192'),
                b'\x84': ('bdquo', '201E'),
                b'\x85': ('hellip', '2026'),
                b'\x86': ('dagger', '2020'),
                b'\x87': ('Dagger', '2021'),
                b'\x88': ('circ', '2C6'),
                b'\x89': ('permil', '2030'),
                b'\x8A': ('Scaron', '160'),
                b'\x8B': ('lsaquo', '2039'),
                b'\x8C': ('OElig', '152'),
                b'\x8D': '?',
                b'\x8E': ('#x17D', '17D'),
                b'\x8F': '?',
                b'\x90': '?',
                b'\x91': ('lsquo', '2018'),
                b'\x92': ('rsquo', '2019'),
                b'\x93': ('ldquo', '201C'),
                b'\x94': ('rdquo', '201D'),
                b'\x95': ('bull', '2022'),
                b'\x96': ('ndash', '2013'),
                b'\x97': ('mdash', '2014'),
                b'\x98': ('tilde', '2DC'),
                b'\x99': ('trade', '2122'),
                b'\x9a': ('scaron', '161'),
                b'\x9b': ('rsaquo', '203A'),
                b'\x9c': ('oelig', '153'),
                b'\x9d': '?',
                b'\x9e': ('#x17E', '17E'),
                b'\x9f': ('Yuml', ''), }

    # A parochial partial mapping of ISO-Latin-1 to ASCII. Contains
    # horrors like stripping diacritical marks to turn á into a, but also
    # contains non-horrors like turning “ into ".
    MS_CHARS_TO_ASCII = {
        b'\x80': 'EUR',
        b'\x81': ' ',
        b'\x82': ',',
        b'\x83': 'f',
        b'\x84': ',,',
        b'\x85': '...',
        b'\x86': '+',
        b'\x87': '++',
        b'\x88': '^',
        b'\x89': '%',
        b'\x8a': 'S',
        b'\x8b': '<',
        b'\x8c': 'OE',
        b'\x8d': '?',
        b'\x8e': 'Z',
        b'\x8f': '?',
        b'\x90': '?',
        b'\x91': "'",
        b'\x92': "'",
        b'\x93': '"',
        b'\x94': '"',
        b'\x95': '*',
        b'\x96': '-',
        b'\x97': '--',
        b'\x98': '~',
        b'\x99': '(TM)',
        b'\x9a': 's',
        b'\x9b': '>',
        b'\x9c': 'oe',
        b'\x9d': '?',
        b'\x9e': 'z',
        b'\x9f': 'Y',
        b'\xa0': ' ',
        b'\xa1': '!',
        b'\xa2': 'c',
        b'\xa3': 'GBP',
        b'\xa4': '$',  # This approximation is especially parochial--this is the
        # generic currency symbol.
        b'\xa5': 'YEN',
        b'\xa6': '|',
        b'\xa7': 'S',
        b'\xa8': '..',
        b'\xa9': '',
        b'\xaa': '(th)',
        b'\xab': '<<',
        b'\xac': '!',
        b'\xad': ' ',
        b'\xae': '(R)',
        b'\xaf': '-',
        b'\xb0': 'o',
        b'\xb1': '+-',
        b'\xb2': '2',
        b'\xb3': '3',
        b'\xb4': ("'", 'acute'),
        b'\xb5': 'u',
        b'\xb6': 'P',
        b'\xb7': '*',
        b'\xb8': ',',
        b'\xb9': '1',
        b'\xba': '(th)',
        b'\xbb': '>>',
        b'\xbc': '1/4',
        b'\xbd': '1/2',
        b'\xbe': '3/4',
        b'\xbf': '?',
        b'\xc0': 'A',
        b'\xc1': 'A',
        b'\xc2': 'A',
        b'\xc3': 'A',
        b'\xc4': 'A',
        b'\xc5': 'A',
        b'\xc6': 'AE',
        b'\xc7': 'C',
        b'\xc8': 'E',
        b'\xc9': 'E',
        b'\xca': 'E',
        b'\xcb': 'E',
        b'\xcc': 'I',
        b'\xcd': 'I',
        b'\xce': 'I',
        b'\xcf': 'I',
        b'\xd0': 'D',
        b'\xd1': 'N',
        b'\xd2': 'O',
        b'\xd3': 'O',
        b'\xd4': 'O',
        b'\xd5': 'O',
        b'\xd6': 'O',
        b'\xd7': '*',
        b'\xd8': 'O',
        b'\xd9': 'U',
        b'\xda': 'U',
        b'\xdb': 'U',
        b'\xdc': 'U',
        b'\xdd': 'Y',
        b'\xde': 'b',
        b'\xdf': 'B',
        b'\xe0': 'a',
        b'\xe1': 'a',
        b'\xe2': 'a',
        b'\xe3': 'a',
        b'\xe4': 'a',
        b'\xe5': 'a',
        b'\xe6': 'ae',
        b'\xe7': 'c',
        b'\xe8': 'e',
        b'\xe9': 'e',
        b'\xea': 'e',
        b'\xeb': 'e',
        b'\xec': 'i',
        b'\xed': 'i',
        b'\xee': 'i',
        b'\xef': 'i',
        b'\xf0': 'o',
        b'\xf1': 'n',
        b'\xf2': 'o',
        b'\xf3': 'o',
        b'\xf4': 'o',
        b'\xf5': 'o',
        b'\xf6': 'o',
        b'\xf7': '/',
        b'\xf8': 'o',
        b'\xf9': 'u',
        b'\xfa': 'u',
        b'\xfb': 'u',
        b'\xfc': 'u',
        b'\xfd': 'y',
        b'\xfe': 'b',
        b'\xff': 'y',
    }

    # A map used when removing rogue Windows-1252/ISO-8859-1
    # characters in otherwise UTF-8 documents.
    #
    # Note that \x81, \x8d, \x8f, \x90, and \x9d are undefined in
    # Windows-1252.
    WINDOWS_1252_TO_UTF8 = {
        0x80: b'\xe2\x82\xac',  # €
        0x82: b'\xe2\x80\x9a',  # ‚
        0x83: b'\xc6\x92',  # ƒ
        0x84: b'\xe2\x80\x9e',  # „
        0x85: b'\xe2\x80\xa6',  # …
        0x86: b'\xe2\x80\xa0',  # †
        0x87: b'\xe2\x80\xa1',  # ‡
        0x88: b'\xcb\x86',  # ˆ
        0x89: b'\xe2\x80\xb0',  # ‰
        0x8a: b'\xc5\xa0',  # Š
        0x8b: b'\xe2\x80\xb9',  # ‹
        0x8c: b'\xc5\x92',  # Œ
        0x8e: b'\xc5\xbd',  # Ž
        0x91: b'\xe2\x80\x98',  # ‘
        0x92: b'\xe2\x80\x99',  # ’
        0x93: b'\xe2\x80\x9c',  # “
        0x94: b'\xe2\x80\x9d',  # ”
        0x95: b'\xe2\x80\xa2',  # •
        0x96: b'\xe2\x80\x93',  # –
        0x97: b'\xe2\x80\x94',  # —
        0x98: b'\xcb\x9c',  # ˜
        0x99: b'\xe2\x84\xa2',  # ™
        0x9a: b'\xc5\xa1',  # š
        0x9b: b'\xe2\x80\xba',  # ›
        0x9c: b'\xc5\x93',  # œ
        0x9e: b'\xc5\xbe',  # ž
        0x9f: b'\xc5\xb8',  # Ÿ
        0xa0: b'\xc2\xa0',  #  
        0xa1: b'\xc2\xa1',  # ¡
        0xa2: b'\xc2\xa2',  # ¢
        0xa3: b'\xc2\xa3',  # £
        0xa4: b'\xc2\xa4',  # ¤
        0xa5: b'\xc2\xa5',  # ¥
        0xa6: b'\xc2\xa6',  # ¦
        0xa7: b'\xc2\xa7',  # §
        0xa8: b'\xc2\xa8',  # ¨
        0xa9: b'\xc2\xa9',  # ©
        0xaa: b'\xc2\xaa',  # ª
        0xab: b'\xc2\xab',  # «
        0xac: b'\xc2\xac',  # ¬
        0xad: b'\xc2\xad',  # ­
        0xae: b'\xc2\xae',  # ®
        0xaf: b'\xc2\xaf',  # ¯
        0xb0: b'\xc2\xb0',  # °
        0xb1: b'\xc2\xb1',  # ±
        0xb2: b'\xc2\xb2',  # ²
        0xb3: b'\xc2\xb3',  # ³
        0xb4: b'\xc2\xb4',  # ´
        0xb5: b'\xc2\xb5',  # µ
        0xb6: b'\xc2\xb6',  # ¶
        0xb7: b'\xc2\xb7',  # ·
        0xb8: b'\xc2\xb8',  # ¸
        0xb9: b'\xc2\xb9',  # ¹
        0xba: b'\xc2\xba',  # º
        0xbb: b'\xc2\xbb',  # »
        0xbc: b'\xc2\xbc',  # ¼
        0xbd: b'\xc2\xbd',  # ½
        0xbe: b'\xc2\xbe',  # ¾
        0xbf: b'\xc2\xbf',  # ¿
        0xc0: b'\xc3\x80',  # À
        0xc1: b'\xc3\x81',  # Á
        0xc2: b'\xc3\x82',  # Â
        0xc3: b'\xc3\x83',  # Ã
        0xc4: b'\xc3\x84',  # Ä
        0xc5: b'\xc3\x85',  # Å
        0xc6: b'\xc3\x86',  # Æ
        0xc7: b'\xc3\x87',  # Ç
        0xc8: b'\xc3\x88',  # È
        0xc9: b'\xc3\x89',  # É
        0xca: b'\xc3\x8a',  # Ê
        0xcb: b'\xc3\x8b',  # Ë
        0xcc: b'\xc3\x8c',  # Ì
        0xcd: b'\xc3\x8d',  # Í
        0xce: b'\xc3\x8e',  # Î
        0xcf: b'\xc3\x8f',  # Ï
        0xd0: b'\xc3\x90',  # Ð
        0xd1: b'\xc3\x91',  # Ñ
        0xd2: b'\xc3\x92',  # Ò
        0xd3: b'\xc3\x93',  # Ó
        0xd4: b'\xc3\x94',  # Ô
        0xd5: b'\xc3\x95',  # Õ
        0xd6: b'\xc3\x96',  # Ö
        0xd7: b'\xc3\x97',  # ×
        0xd8: b'\xc3\x98',  # Ø
        0xd9: b'\xc3\x99',  # Ù
        0xda: b'\xc3\x9a',  # Ú
        0xdb: b'\xc3\x9b',  # Û
        0xdc: b'\xc3\x9c',  # Ü
        0xdd: b'\xc3\x9d',  # Ý
        0xde: b'\xc3\x9e',  # Þ
        0xdf: b'\xc3\x9f',  # ß
        0xe0: b'\xc3\xa0',  # à
        0xe1: b'\xa1',  # á
        0xe2: b'\xc3\xa2',  # â
        0xe3: b'\xc3\xa3',  # ã
        0xe4: b'\xc3\xa4',  # ä
        0xe5: b'\xc3\xa5',  # å
        0xe6: b'\xc3\xa6',  # æ
        0xe7: b'\xc3\xa7',  # ç
        0xe8: b'\xc3\xa8',  # è
        0xe9: b'\xc3\xa9',  # é
        0xea: b'\xc3\xaa',  # ê
        0xeb: b'\xc3\xab',  # ë
        0xec: b'\xc3\xac',  # ì
        0xed: b'\xc3\xad',  # í
        0xee: b'\xc3\xae',  # î
        0xef: b'\xc3\xaf',  # ï
        0xf0: b'\xc3\xb0',  # ð
        0xf1: b'\xc3\xb1',  # ñ
        0xf2: b'\xc3\xb2',  # ò
        0xf3: b'\xc3\xb3',  # ó
        0xf4: b'\xc3\xb4',  # ô
        0xf5: b'\xc3\xb5',  # õ
        0xf6: b'\xc3\xb6',  # ö
        0xf7: b'\xc3\xb7',  # ÷
        0xf8: b'\xc3\xb8',  # ø
        0xf9: b'\xc3\xb9',  # ù
        0xfa: b'\xc3\xba',  # ú
        0xfb: b'\xc3\xbb',  # û
        0xfc: b'\xc3\xbc',  # ü
        0xfd: b'\xc3\xbd',  # ý
        0xfe: b'\xc3\xbe',  # þ
    }

    MULTIBYTE_MARKERS_AND_SIZES = [
        (0xc2, 0xdf, 2),  # 2-byte characters start with a byte C2-DF
        (0xe0, 0xef, 3),  # 3-byte characters start with E0-EF
        (0xf0, 0xf4, 4),  # 4-byte characters start with F0-F4
    ]

    FIRST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[0][0]
    LAST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[-1][1]

    @classmethod
    def detwingle(cls, in_bytes, main_encoding="utf8",
                  embedded_encoding="windows-1252"):
        """Fix characters from one encoding embedded in some other encoding.

        Currently the only situation supported is Windows-1252 (or its
        subset ISO-8859-1), embedded in UTF-8.

        :param in_bytes: A bytestring that you suspect contains
            characters from multiple encodings. Note that this _must_
            be a bytestring. If you've already converted the document
            to Unicode, you're too late.
        :param main_encoding: The primary encoding of `in_bytes`.
        :param embedded_encoding: The encoding that was used to embed characters
            in the main document.
        :return: A bytestring in which `embedded_encoding`
          characters have been converted to their `main_encoding`
          equivalents.
        """
        if embedded_encoding.replace('_', '-').lower() not in (
                'windows-1252', 'windows_1252'):
            raise NotImplementedError(
                "Windows-1252 and ISO-8859-1 are the only currently supported "
                "embedded encodings.")

        if main_encoding.lower() not in ('utf8', 'utf-8'):
            raise NotImplementedError(
                "UTF-8 is the only currently supported main encoding.")

        byte_chunks = []

        chunk_start = 0
        pos = 0
        while pos < len(in_bytes):
            byte = in_bytes[pos]
            if not isinstance(byte, int):
                # Python 2.x
                byte = ord(byte)
            if (byte >= cls.FIRST_MULTIBYTE_MARKER
                    and byte <= cls.LAST_MULTIBYTE_MARKER):
                # This is the start of a UTF-8 multibyte character. Skip
                # to the end.
                for start, end, size in cls.MULTIBYTE_MARKERS_AND_SIZES:
                    if byte >= start and byte <= end:
                        pos += size
                        break
            elif byte >= 0x80 and byte in cls.WINDOWS_1252_TO_UTF8:
                # We found a Windows-1252 character!
                # Save the string up to this point as a chunk.
                byte_chunks.append(in_bytes[chunk_start:pos])

                # Now translate the Windows-1252 character into UTF-8
                # and add it as another, one-byte chunk.
                byte_chunks.append(cls.WINDOWS_1252_TO_UTF8[byte])
                pos += 1
                chunk_start = pos
            else:
                # Go on to the next character.
                pos += 1
        if chunk_start == 0:
            # The string is unchanged.
            return in_bytes
        else:
            # Store the final chunk.
            byte_chunks.append(in_bytes[chunk_start:])
        return b''.join(byte_chunks)


# Type aliases used in function signatures.
EscapeCodes = typing.Mapping[str, str]
LogColors = typing.Mapping[str, str]
SecondaryLogColors = typing.Mapping[str, LogColors]

# The default colors to use for the debug levels
default_log_colors = {
    "DEBUG": "white",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

# The default format to use for each style
default_formats = {
    "%": "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    "{": "{log_color}{levelname}:{name}:{message}",
    "$": "${log_color}${levelname}:${name}:${message}",
}


# Returns escape codes from format codes
def esc(*codes: int) -> str:
    return "\033[" + ";".join(str(code) for code in codes) + "m"


escape_codes = {
    "reset": esc(0),
    "bold": esc(1),
    "thin": esc(2),
}

escape_codes_foreground = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "purple": 35,
    "cyan": 36,
    "white": 37,
    "light_black": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_purple": 95,
    "light_cyan": 96,
    "light_white": 97,
}

escape_codes_background = {
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "purple": 45,
    "cyan": 46,
    "white": 47,
    "light_black": 100,
    "light_red": 101,
    "light_green": 102,
    "light_yellow": 103,
    "light_blue": 104,
    "light_purple": 105,
    "light_cyan": 106,
    "light_white": 107,
    # Bold background colors don't exist,
    # but we used to provide these names.
    "bold_black": 100,
    "bold_red": 101,
    "bold_green": 102,
    "bold_yellow": 103,
    "bold_blue": 104,
    "bold_purple": 105,
    "bold_cyan": 106,
    "bold_white": 107,
}

# Foreground without prefix
for name, code in escape_codes_foreground.items():
    escape_codes["%s" % name] = esc(code)
    escape_codes["bold_%s" % name] = esc(1, code)
    escape_codes["thin_%s" % name] = esc(2, code)

# Foreground with fg_ prefix
for name, code in escape_codes_foreground.items():
    escape_codes["fg_%s" % name] = esc(code)
    escape_codes["fg_bold_%s" % name] = esc(1, code)
    escape_codes["fg_thin_%s" % name] = esc(2, code)

# Background with bg_ prefix
for name, code in escape_codes_background.items():
    escape_codes["bg_%s" % name] = esc(code)

# 256 colour support
for code in range(256):
    escape_codes["fg_%d" % code] = esc(38, 5, code)
    escape_codes["bg_%d" % code] = esc(48, 5, code)


def parse_colors(string: str) -> str:
    """Return escape codes from a color sequence string."""
    return "".join(escape_codes[n] for n in string.split(",") if n)


class ColoredRecord:
    """
    Wraps a LogRecord, adding escape codes to the internal dict.

    The internal dict is used when formatting the message (by the PercentStyle,
    StrFormatStyle, and StringTemplateStyle classes).
    """

    def __init__(self, record: logging.LogRecord, escapes: EscapeCodes) -> None:
        self.__dict__.update(record.__dict__)
        self.__dict__.update(escapes)


class ColoredFormatter(logging.Formatter):
    """
    A formatter that allows colors to be placed in the format string.

    Intended to help in creating more readable logging output.
    """

    def __init__(
            self,
            fmt: typing.Optional[str] = None,
            datefmt: typing.Optional[str] = None,
            style: str = "%",
            log_colors: typing.Optional[LogColors] = None,
            reset: bool = True,
            secondary_log_colors: typing.Optional[SecondaryLogColors] = None,
            validate: bool = True,
            stream: typing.Optional[typing.IO] = None,
            no_color: bool = False,
    ) -> None:
        """
        Set the format and colors the ColoredFormatter will use.

        The ``fmt``, ``datefmt`` and ``style`` args are passed on to the
        ``logging.Formatter`` constructor.

        The ``secondary_log_colors`` argument can be used to create additional
        ``log_color`` attributes. Each key in the dictionary will set
        ``{key}_log_color``, using the value to select from a different
        ``log_colors`` set.

        :Parameters:
        - fmt (str): The format string to use.
        - datefmt (str): A format string for the date.
        - log_colors (dict):
            A mapping of log level names to color names.
        - reset (bool):
            Implicitly append a color reset to all records unless False.
        - style ('%' or '{' or '$'):
            The format style to use. (*No meaning prior to Python 3.2.*)
        - secondary_log_colors (dict):
            Map secondary ``log_color`` attributes. (*New in version 2.6.*)
        - validate (bool)
            Validate the format string.
        - stream (typing.IO)
            The stream formatted messages will be printed to. Used to toggle colour
            on non-TTY outputs. Optional.
        """

        # Select a default format if `fmt` is not provided.
        fmt = default_formats[style] if fmt is None else fmt

        if sys.version_info >= (3, 8):
            super().__init__(fmt, datefmt, style, validate)
        else:
            super().__init__(fmt, datefmt, style)

        self.log_colors = log_colors if log_colors is not None else default_log_colors
        self.secondary_log_colors = (
            secondary_log_colors if secondary_log_colors is not None else {}
        )
        self.reset = reset
        self.stream = stream
        self.no_color = no_color

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        escapes = self._escape_code_map(record.levelname)
        wrapper = ColoredRecord(record, escapes)
        message = super().formatMessage(wrapper)  # type: ignore
        message = self._append_reset(message, escapes)
        return message

    def _escape_code_map(self, item: str) -> EscapeCodes:
        """
        Build a map of keys to escape codes for use in message formatting.

        If _blank_escape_codes() returns True, all values will be an empty string.
        """
        codes = {**escape_codes}
        codes.setdefault("log_color", self._get_escape_code(self.log_colors, item))
        for name, colors in self.secondary_log_colors.items():
            codes.setdefault("%s_log_color" % name, self._get_escape_code(colors, item))
        if self._blank_escape_codes():
            codes = {key: "" for key in codes.keys()}
        return codes

    def _blank_escape_codes(self):
        """Return True if we should be prevented from printing escape codes."""
        if self.no_color:
            return True

        if "NO_COLOR" in os.environ:
            return True

        if self.stream is not None and not self.stream.isatty():
            return True

        return False

    @staticmethod
    def _get_escape_code(log_colors: LogColors, item: str) -> str:
        """Extract a color sequence from a mapping, and return escape codes."""
        return parse_colors(log_colors.get(item, ""))

    def _append_reset(self, message: str, escapes: EscapeCodes) -> str:
        """Add a reset code to the end of the message, if it's not already there."""
        reset_escape_code = escapes["reset"]

        if self.reset and not message.endswith(reset_escape_code):
            message += reset_escape_code

        return message


class Request:
    def __init__(self, **kwargs):
        self.url = None
        self.method = None
        self.data = None
        self.json = None
        self.headers = None
        self.cookies = None
        self.allow_redirects = None
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<espider.Request {}>'.format(self.url)


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"
]
