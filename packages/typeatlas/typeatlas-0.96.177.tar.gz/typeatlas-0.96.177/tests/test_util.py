# -*- coding: utf-8 -*-
#
#    TypeAtlas Unit Tests for Some Utility Function and Classes
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

from nose.tools import assert_equal, assert_not_equal, assert_raises
from nose.tools import assert_sequence_equal, assert_set_equal
from nose.tools import assert_less_equal, assert_greater_equal
from nose.tools import assert_set_equal, assert_in, assert_not_in
from typeatlas.util import ManagedIter


class TestManagedIter:

    def test_iter(self):
        it = ManagedIter(list(range(300)))
        assert_equal(next(it), 0)
        assert_equal(next(it), 1)
        assert_equal(next(it), 2)
        assert_equal(next(it), 3)
        assert_equal(list(it), list(range(4, 300)))
        assert_raises(StopIteration, next, it)
        assert_equal(next(it, 616), 616)

    def test_sentinel(self):
        L = list(reversed(range(4, 30)))
        it = ManagedIter(lambda: L.pop() if L else -1, -1)
        assert_equal(next(it), 4)
        assert_equal(next(it), 5)
        assert_equal(next(it), 6)
        assert_equal(next(it), 7)
        assert_equal(list(it), list(range(8, 30)))
        assert_raises(StopIteration, next, it)
        assert_equal(next(it, 616), 616)

    def test_lookahead(self):
        it = ManagedIter(list(range(300)))
        assert_equal(next(it), 0)
        assert_equal(next(it), 1)
        assert_equal(it.peek(), 2)
        assert_equal(it.empty(), False)
        assert_equal(next(it), 2)
        assert_equal(next(it), 3)
        assert_equal(it.lookahead(6), 10)
        assert_equal(it.lookahead(5), 9)
        assert_equal(it.lookahead(4), 8)
        assert_equal(it.lookahead(3), 7)
        assert_equal(it.lookahead(2), 6)
        assert_equal(it.lookahead(1), 5)
        assert_equal(it.lookahead(0), 4)
        assert_equal(it.peek(), 4)
        assert_equal(it.lookahead(6), 10)
        assert_equal(next(it), 4)
        assert_equal(next(it), 5)
        assert_equal(next(it), 6)
        assert_equal(next(it), 7)
        assert_equal(next(it), 8)
        assert_equal(next(it), 9)
        assert_equal(next(it), 10)
        assert_equal(next(it), 11)
        assert_equal(next(it), 12)
        assert_equal(it.lookahead(0), 13)
        assert_equal(it.lookahead(1), 14)
        assert_equal(it.lookahead(2), 15)
        assert_equal(it.lookahead(3), 16)

        assert_equal(list(it), list(range(13, 300)))
        assert_equal(it.empty(), True)
        assert_raises(StopIteration, next, it)
        assert_raises(StopIteration, it.peek)
        assert_raises(StopIteration, it.lookahead)
        assert_equal(it.empty(), True)
        assert_equal(next(it, 616), 616)
        assert_equal(it.empty(), True)

        assert_equal(next(it, None), None)
        assert_equal(it.peek(None), None)
        assert_equal(it.lookahead(0, None), None)
        assert_equal(it.lookahead(10000000, None), None)

        L = list(reversed(range(4, 30)))
        it = ManagedIter(lambda: L.pop() if L else -1, -1)

        assert_raises(StopIteration, it.lookahead, 400)

        assert_equal(it.peek(), 4)
        assert_equal(it.lookahead(25), 29)
        assert_raises(StopIteration, it.lookahead, 26)
        assert_equal(next(it), 4)
        assert_equal(next(it), 5)
        assert_equal(next(it), 6)
        assert_equal(next(it), 7)
        assert_equal(list(it), list(range(8, 30)))
        assert_raises(StopIteration, next, it)
        assert_equal(next(it, 616), 616)
        assert_equal(it.peek(616), 616)
        assert_equal(it.lookahead(0, 616), 616)
        assert_equal(it.lookahead(101, 616), 616)

    def test_appendleft(self):
        L = list(reversed(range(4, 30)))
        it = ManagedIter(lambda: L.pop() if L else -1, -1)

        assert_raises(StopIteration, it.lookahead, 400)

        assert_equal(it.peek(), 4)
        assert_equal(it.lookahead(25), 29)
        assert_raises(StopIteration, it.lookahead, 26)

        it.appendleft(3)
        assert_equal(it.peek(), 3)
        assert_equal(it.lookahead(26), 29)
        assert_raises(StopIteration, it.lookahead, 27)

        assert_equal(next(it), 3)
        assert_equal(next(it), 4)
        assert_equal(next(it), 5)
        assert_equal(next(it), 6)
        assert_equal(next(it), 7)
        assert_equal(list(it), list(range(8, 30)))
        assert_raises(StopIteration, next, it)
        assert_equal(it.peek(616), 616)
        assert_equal(next(it, 616), 616)

        L = list(reversed(range(4, 30)))
        it = ManagedIter(lambda: L.pop() if L else -1, -1)
        it.extendleft(reversed([0,1,2,3]))

        assert_equal(list(it), list(range(0, 30)))
        assert_raises(StopIteration, next, it)
        assert_equal(next(it, 616), 616)
        assert_equal(it.peek(616), 616)

    def test_extend_head(self):
        it = ManagedIter(range(30))
        it.extend(range(30, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter(range(30))
        assert_equal(list(it.head(15)), list(range(0, 15)))
        it.extend(range(30, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter(range(30))
        assert_equal(list(it.head(30)), list(range(0, 30)))
        it.extend(range(30, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter(range(30))
        assert_equal(list(it.head(60)), list(range(0, 30)))
        it.extend(range(30, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter(range(30))
        assert_equal(list(it.head(60)), list(range(0, 30)))
        it.extend(range(30, 60))
        assert_equal(list(it.head(60)), list(range(0, 60)))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter([])
        it.extend(range(0, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

        it = ManagedIter([])
        assert_raises(StopIteration, next, it)
        it.extend(range(0, 60))
        assert_equal(list(it), list(range(0, 60)))
        assert_raises(StopIteration, next, it)
        assert_equal(list(it.head(100)), [])

    def test_append(self):
        it1 = ManagedIter(range(3))
        it1.append(4)

        it2 = ManagedIter(range(3))
        it2.extend([4])

        assert_equal(list(it1), list(it2))
        assert_raises(StopIteration, next, it1)
        assert_raises(StopIteration, next, it2)

        it = ManagedIter(range(3))
        it.append(3)
        it.append(4)
        it.append(5)
        it.append(6)
        it.append(7)

        assert_equal(list(it), list(range(0, 8)))
        assert_raises(StopIteration, next, it)

        it = ManagedIter(range(3))
        assert_equal(list(it), list(range(0, 3)))
        it.append(3)
        it.append(4)
        it.append(5)
        it.append(6)
        it.append(7)

        assert_equal(list(it), list(range(3, 8)))
        assert_raises(StopIteration, next, it)

        it = ManagedIter(range(3))
        assert_equal(next(it), 0)
        assert_equal(next(it), 1)
        assert_equal(next(it), 2)
        it.append(3)
        it.append(4)
        it.append(5)
        it.append(6)
        it.append(7)

        assert_equal(list(it), list(range(3, 8)))
        assert_raises(StopIteration, next, it)
        assert_raises(StopIteration, it.peek)
        assert_equal(it.peek(-1), -1)
        assert_equal(it.lookahead(100, -1), -1)

    def test_head(self):
        it = ManagedIter(range(3))
        assert_equal(list(it.head(6)), list(range(3)))
        it.append(3)
        it.append(4)
        it.append(5)
        it.append(6)
        it.append(7)

        assert_equal(list(it), list(range(0, 8)))
        assert_raises(StopIteration, next, it)

        it = ManagedIter(range(3))
        it.append(3)
        it.append(4)
        assert_equal(list(it.head(6)), list(range(5)))
        it.append(5)
        it.append(6)
        it.append(7)

        assert_equal(list(it), list(range(0, 8)))
        assert_raises(StopIteration, next, it)

        it = ManagedIter(range(3))
        it.append(3)
        it.append(4)
        it.append(5)
        it.append(6)
        assert_equal(list(it.head(6)), list(range(6)))
        it.append(7)

        assert_equal(list(it), list(range(0, 8)))
        assert_raises(StopIteration, next, it)
