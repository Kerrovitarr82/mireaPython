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
    f1 = []
    for _ in range(8):
        val = reader.read_uint8()
        f1.append(val)
    f2 = reader.read_int16()
    f3 = reader.read_int64()
    return dict(F1=f1, F2=f2, F3=f3)


def read_d(reader: BinaryReader):
    d1 = reader.read_float()
    d2 = reader.read_double()
    d3 = read_array(
        source=reader.source,
        size=reader.read_uint32(),
        address=reader.read_uint32(),
        read=lambda reader: reader.read_uint32(),
        structure_size=4
    )
    d4 = reader.read_double()
    d5 = reader.read_double()
    d6 = []
    for _ in range(4):
        val = reader.read_int16()
        d6.append(val)
    d7 = reader.read_int64()
    d8 = reader.read_int32()
    return dict(D1=d1, D2=d2, D3=d3, D4=d4, D5=d5, D6=d6, D7=d7, D8=d8)


def read_c(reader: BinaryReader):
    c1 = reader.read_uint16()
    c2 = read_array(
        source=reader.source,
        size=reader.read_uint16(),
        address=reader.read_uint16(),
        read=lambda reader: reader.read_float(),
        structure_size=4
    )
    return dict(C1=c1, C2=c2)


def read_b(reader: BinaryReader):
    b1 = reader.read_int64()
    b2 = reader.read_uint64()
    b3 = reader.read_int32()
    b4 = []
    for _ in range(2):
        val = read_array(
            source=reader.source,
            size=1,
            address=reader.read_uint32(),
            read=lambda reader: read_c(reader),
        )
        b4.append(val)
    b4 = b4[0] + b4[1]
    b5 = reader.read_int8()
    b6 = read_array(
        source=reader.source,
        size=reader.read_uint32(),
        address=reader.read_uint16(),
        read=lambda reader: reader.read_uint32(),
        structure_size=4
    )
    b7 = reader.read_uint64()
    return dict(B1=b1, B2=b2, B3=b3, B4=b4, B5=b5, B6=b6, B7=b7)


def read_a(reader: BinaryReader):
    a1 = read_array(
        source=reader.source,
        size=1,
        address=reader.read_uint32(),
        read=lambda reader: read_b(reader),
    )
    a1 = a1[0]
    a2 = reader.read_int64()
    a3 = reader.read_int32()
    a4 = read_array(
        source=reader.source,
        size=1,
        address=reader.read_uint32(),
        read=lambda reader: read_d(reader),
    )
    a4 = a4[0]
    return dict(A1=a1, A2=a2, A3=a3, A4=a4)


def main(source):
    reader = BinaryReader(source)
    reader.read('ccccc')
    return read_a(reader)


print(main(b'YUTZ\xaaU\x00\x00\x00\x13\xe7\xd2\xfb\x99\x99\xbaJ\x91ly\\\x88\x00\x00'
           b'\x00y\x1d&?ll\x7f?\xa5Z\xe8\xbd\x81\xbe\x03\x00\x19\x00\x19n\x11\xbf]'
           b'\xc3\x14?K\xb6\xb2>\xcaf#\xbf\xba\xc6\x97\xbex\x80\x05\x00+\x00^\xad\xf1'
           b'kKX\xebj\xa4\xd3L\xed\xde\x1dE1\x91\xbd\x96\xa7\xd2\xf7r\x13\x12\x17\x92'
           b'\xfe\xb5\x84\x8b,(\xf0\x84\xa0%\x00\x00\x00?\x00\x00\x00\xa6\x04\x00'
           b'\x00\x00E\x00\xa5e\xec@\x83\xee>i\x14\xab\x1f0\xa1M*\xa5\x8e?\xcb\xbd'
           b'\x1cth\xc1(\x05\xea?\x02\x00\x00\x00\x80\x00\x00\x00\x00 \xf1\x86'
           b'Z\x87\x97\xbf`VS\x02\x1b*\xce\xbf\xf6\x06\x05G#\x19sf\x82\x00b\xe8X\xden\xd1'
           b'\x1c\xa0\x17N'))
