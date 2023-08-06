# -*- coding: utf-8 -*-
#
#    TypeAtlas Archive Support Utilities
#    Copyright (C) 2021 Milko Krachounov
#
#    This file is part of TypeAtlas
#
#    TypeAtlas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TypeAtlas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TypeAtlas.  If not, see <http://www.gnu.org/licenses/>.
#
#                                 ***
#
#    Alternatively, you may use this file (part of TypeAtlas libraries)
#    under the terms of the X11/MIT license as follows:
#
#    Permission is hereby granted, free of charge, to any person
#    obtaining a copy of this software and associated documentation
#    files (the "Software"), to deal in the Software without
#    restriction, including without limitation the rights to use,
#    copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the
#    Software is furnished to do so, subject to the following
#    conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#    OTHER DEALINGS IN THE SOFTWARE.
#

"""This module provides in-memory extraction facilities for
archives."""

import os
import zipfile
import tarfile
import magic
import io
import re
from collections.abc import Iterator, Callable
from typeatlas.util import generic_type

SequenceOf = generic_type('Sequence')
Optional = generic_type('Optional')


extension_factories = {}
mimetype_factories = {}


def get_factory(filename: str=None, fileobj: io.BufferedIOBase=None, *,
                mimetype: str=None) -> type:

    """Return the archive factory for the given archive type."""

    if filename is None and (fileobj is None or mimetype is None):
        raise TypeError("filename or fileobject with mime required")

    if mimetype is None and filename is not None:
        if fileobj is None or os.access(filename, os.R_OK):
            mimetype = magic.from_file(filename, mime=True)

    if mimetype is not None:
        for factory in mimetype_factories.get(mimetype, ()):
            if (fileobj is not None or filename is None or
                factory.is_known_archive(filename)):
                    return factory

    if filename:
        match = re.search(r'\.([^\.]+(?:\.([^\.]+))?)$', filename)
        if match is not None:
            for ext in match.groups():
                if ext:
                    for factory in extension_factories.get(ext, ()):
                        return factory

    raise UnknownArchiveFormat("%r [%s] has unknown archive format"
                                    % (filename or fileobj, mimetype))


def is_known_archive(filename: str, *, mimetype: str=None) -> bool:
    """Return true if the file is a known archive."""
    if mimetype is None:
        mimetype = magic.from_file(filename, mime=True)

    for factory in mimetype_factories.get(mimetype, ()):
        if factory.is_known_archive(filename):
            return True

    if filename:
        for ext in re.search(r'\.([^\.]+(?:\.([^\.]+))?)$', filename).groups():
            if ext:
                for factory in extension_factories.get(ext, ()):
                    if factory.is_known_archive(filename):
                        return True

    return False


def get_archive(filename: str=None, fileobj: io.BufferedIOBase=None, *,
                mimetype: str=None) -> 'Archive':

    """Return the archive object that can iterate over the files
    archived inside the file."""

    factory = get_factory(filename, fileobj, mimetype=mimetype)
    return factory(filename, fileobj)


def archive_iterate(filename: str=None, fileobj: io.BufferedIOBase=None, *,
                    mimetype: str=None) -> Iterator:
    """Iterate over the provided archive filename or object."""
    return get_archive(filename, fileobj, mimetype=mimetype).iterate()


def register(extensions: SequenceOf[str]=(), mimetypes: SequenceOf[str]=(),
             compressions: SequenceOf[str]=()) -> Callable:
    """Return a decorator registering the given archive type for the
    given extensions and mime types."""

    def decorator(cls):
        for ext in extensions:
            extension_factories.setdefault(ext, []).append(cls)
        for mime in mimetypes:
            mimetype_factories.setdefault(mime, []).append(cls)
        for mime in compressions:
            mimetype_factories.setdefault(mime, []).append(cls)

        cls.extensions = tuple(extensions)
        cls.mimetypes = tuple(mimetypes)
        cls.compressions = tuple(compressions)

    return decorator


class Archive:

    extensions = ()
    mimetypes = ()
    compressions = ()

    def __init__(self, filename: str=None, fileobj: io.BufferedIOBase=None):
        self.filename = filename
        self.fileobj = fileobj

    @classmethod
    def is_known_archive(self, filename: str) -> bool:
        """Return True if we can read this file with this class."""
        return magic.from_file(filename, mime=True) in self.mimetypes

    def iterate(self) -> Iterator:
        raise NotImplementedError

    def __iter__(self):
        return self.iterate()

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__,
                               self.filename, self.fileobj)


class ArchiveMember:

    @property
    def name(self) -> str:
        """The name or path of the member."""
        raise NotImplementedError

    @property
    def size(self) -> Optional[int]:
        """The size in bytes of the member."""
        raise NotImplementedError

    def open(self) -> io.BytesIO:
        """Return a bytes file object for reading the archive member."""
        raise NotImplementedError

    def getdata(self, limit: Optional[int]=16777216) -> bytes:
        """Return the data as a bytes object. There is a default zip bomb
        limit in place."""
        if limit is None:
            return self.open().read()

        if self.size is not None:
            if self.size > limit:
                raise MemberTooBigError("%r is larger than zip bomb "
                                        "limit of %d" % (self, limit))

        fileob = self.open()
        result = fileob.read(limit)
        if len(result) >= limit:
            if len(result) > limit or fileob.read(1):
                raise MemberTooBigError("%r is larger than zip bomb "
                                        "limit of %d" % (self, limit))

        return result

    def isdir(self) -> bool:
        """Return True if this is a directory."""
        raise NotImplementedError

    def isfile(self) -> bool:
        """Return True if this is a regular file."""
        return not self.isdir()

    def isfifo(self) -> bool:
        """Return True if this is a named FIFO."""
        return False

    def isblk(self) -> bool:
        """Return True if this is a block device."""
        return False

    def ischr(self) -> bool:
        """Return True if this is a character device."""
        return False

    def islink(self) -> bool:
        """Return True if this is a symlink."""
        return False

    def issocket(self) -> bool:
        """Return True if this is a socket."""
        return False

    def ishardlink(self) -> bool:
        """Return True if this is a hard link."""
        return False

    def __repr__(self):
        typename = 'unknown'
        try:
            if self.isfile():
                typename = 'file'
            elif self.isdir():
                typename = 'dir'
            elif self.islink():
                typename = 'symlink'
            elif self.ishardlink():
                typename = 'hardlink'
            elif self.isfifo():
                typename = 'FIFO'
            elif self.isblk():
                typename = 'blockdev'
            elif self.ischr():
                typename = 'chardev'
            elif self.issocket():
                typename = 'socket'
        except Exception:
            typename = 'broken'

        size = self.size
        if size is None:
            size = '-'

        return '<%s %r (%s) [%s] at 0x%x>' % (type(self).__name__, self.name,
                                              typename, size, id(self))


class ZipMember(ArchiveMember):

    def __init__(self, archive: zipfile.ZipFile, member: zipfile.ZipInfo):
        self.archive = archive
        self.member = member

    @property
    def name(self) -> str:
        return self.member.filename

    @property
    def size(self) -> Optional[int]:
        return self.member.file_size

    def isdir(self) -> bool:
        return self.member.is_dir()

    def open(self) -> io.BytesIO:
        return self.archive.open(self.member)


class TarMember(ArchiveMember):

    def __init__(self, archive: tarfile.TarFile, member: tarfile.TarInfo):
        self.archive = archive
        self.member = member

    @property
    def name(self) -> str:
        return self.member.name

    @property
    def size(self) -> Optional[int]:
        return self.member.size

    def isdir(self) -> bool:
        return self.member.isdir()

    def isfile(self) -> bool:
        return self.member.isfile()

    def isfifo(self) -> bool:
        return self.member.isfifo()

    def isblk(self) -> bool:
        return self.member.isblk()

    def ischr(self) -> bool:
        return self.member.ischr()

    def islink(self) -> bool:
        return self.member.issym()

    def ishardlink(self) -> bool:
        return self.member.islnk()

    def open(self) -> io.BytesIO:
        return self.archive.extractfile(self.member)


@register(['zip'], ['application/zip'])
class ZipArchive(Archive):

    def iterate(self) -> Iterator:
        if self.fileobj is None:
            srcfile = self.filename
        else:
            srcfile = self.fileobj

        with zipfile.ZipFile(srcfile, 'r') as archive:
            for member in archive.infolist():
                yield ZipMember(archive, member)


@register(['tar', 'tar.gz', 'tar.bz2', 'tar.xz', 'tar.lzma'],
          ['application/x-tar'],
          ['application/gzip', 'application/x-gzip',
           'application/x-bzip2', 'application/x-xz',
           'application/x-lzma'])
class TarArchive(Archive):

    @classmethod
    def is_known_archive(self, filename: str) -> bool:
        return tarfile.is_tarfile(filename)

    def iterate(self) -> Iterator:
        if self.fileobj is None:
            mode = 'r:*'
        else:
            mode = 'r|*'

        with tarfile.open(self.filename, mode, self.fileobj) as archive:
            for member in archive:
                yield TarMember(archive, member)


class ArchiveError(OSError):
    """Base exception for archive errors."""


class UnknownArchiveFormat(ArchiveError):
    """Raised when the archive format is unknown."""


class MemberTooBigError(ArchiveError):
    """Raised when zip bomb limit was exceeeded."""


if __name__ == '__main__':
    import traceback, sys, hashlib
    for arg in sys.argv[1:]:
        try:
            for member in archive_iterate(arg):#, open(arg, 'rb'),
                                          #mimetype=magic.from_file(arg, mime=True)):
                print(member)
                if member.isfile():
                    print('  ', hashlib.md5(member.open().read()).hexdigest())
                    #print('  ', hashlib.md5(member.open().read()).hexdigest())
                    #f = member.open()
                    #print('  ', hashlib.md5(f.read()).hexdigest())
                    #f.seek(0)
                    #print('  ', hashlib.md5(f.read()).hexdigest())
        except Exception:
            traceback.print_exc()
