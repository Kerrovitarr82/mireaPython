from struct import unpack_from, calcsize
from typing import Any, Callable


class BinaryReader:
    def __init__(self, source, offset=0):
        self.offset = offset
        self.source = source

    def read_uint64(self):
        return self.read('Q')

    def read_int64(self):
        return self.read('q')

    def read_uint32(self):
        return self.read('I')

    def read_int32(self):
        return self.read('i')

    def read_uint16(self):
        return self.read('H')

    def read_int16(self):
        return self.read('h')

    def read_uint8(self):
        return self.read('B')

    def read_int8(self):
        return self.read('b')

    def read_float(self):
        return self.read('f')

    def read_char(self):
        return self.read('c')

    def read_double(self):
        return self.read('d')

    def read(self, pattern: str):
        size = calcsize(pattern)
        data = unpack_from(pattern, self.source, self.offset)
        self.offset += size
        return data[0]


def read_array(
    source: str,
    size: int,
    address: int,
    read: Callable[[BinaryReader], Any],
    structure_size: int = 1,
):
    reader = BinaryReader(source=source, offset=address)
    values = []
    while address + (size * structure_size) > reader.offset:
        values.append(read(reader))
    return values


def read_f(reader: BinaryReader):
    f1 = read_array(
        source=reader.source,
        size=8,
        address=0,
        read=lambda reader: reader.read_uint8()
    )
    f2 = reader.read_int16()
    f3 = reader.read_int64()
    return dict(F1=f1, F2=f2, F3=f3)


def read_e(reader: BinaryReader):
    e1 = read_array(
        source=reader.source,
        size=3,
        address=0,
        read=lambda reader: reader.read_uint8()
    )
    e2 = reader.read_uint64()
    e3 = reader.read_int16()
    e4 = reader.read_int16()
    return dict(E1=e1, E2=e2, E3=e3, E4=e4)


def read_d(reader: BinaryReader):
    d1 = reader.read_double()
    d2 = read_e(reader)
    d3 = read_array(
        source=reader.source,
        size=reader.read_uint32(),
        address=reader.read_uint32(),
        read=lambda reader: reader.read_uint16(),
    )
    return dict(D1=d1, D2=d2, D3=d3)


def read_c(reader: BinaryReader):
    c1 = reader.read_double()
    c2 = read_d(reader)
    return dict(C1=c1, C2=c2)


def read_b(reader: BinaryReader):
    b1 = reader.read_int32()
    b2 = read_array(
        source=reader.source,
        size=1,
        address=reader.read_uint32(),
        read=lambda reader: read_c(reader),
    )
    return dict(B1=b1, B2=b2)


def read_a(reader: BinaryReader):
    a1 = reader.read_int8()
    a2 = read_array(
        source=reader.source,
        size=1,
        address=reader.read_uint16(),
        read=lambda reader: read_b(reader)
    )
    a3 = read_b(reader)
    return dict(A1=a1, A2=a2, A3=a3)


def main(source):
    reader = BinaryReader(source)
    reader.read('ccccc')
    return read_a(reader)


print(main(b'OJGY\x16(C\x00\x02\x00\x00\x00o\x00\x00\x00\xd5\xdak:<\xd5\x8b\xf6\x9at4\xba'
           b'\x94\xc7\xcc\xc9"\x02\xee\xbf|\x01?\x19\x8e\xa5\xe8\xbf\xf1\x95\x85\xb2'
           b'\xb9FU`\xd6\x1av2\xf0,\xe2\x06\x00\x00\x00\x10\x00\x00\x00\x9c'
           b'\xe9\x15\xe4\x1c\x00\x00\x00\x8f\xe9/\xef\x16X\x02\x82\x81:\xcb\xa6\xc0'
           b"\xb1p.\xa6\x8d\xb5'\xbfiqE\xd6|[/d\xbe|O\xd5\xd5\xbd\x85K\x00\x00\x00]"
           b'\x00\x00\x00'))
