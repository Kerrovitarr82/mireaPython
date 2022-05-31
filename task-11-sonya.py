from struct import *

FMT = dict(
    char='c',
    int8='b',
    uint8='B',
    int16='h',
    uint16='H',
    int32='i',
    uint32='I',
    int64='q',
    uint64='Q',
    float='f',
    double='d',
)


def parse(buf, offs, ty):
    data = unpack_from(FMT[ty], buf, offs)
    data = data[0]
    of = offs + calcsize(FMT[ty])
    return data, of


def parse_a(buf, offs):
    a1, offs = parse(buf, offs, 'uint32')
    a2 = []
    for _ in range(2):
        val, offs = parse(buf, offs, 'int32')
        a2.append(val)
    a3, offs = parse_b(buf, offs)
    a4_size, offs = parse(buf, offs, 'uint16')
    a4_offs, offs = parse(buf, offs, 'uint32')
    a4 = []
    for _ in range(a4_size):
        val, a4_offs = parse(buf, a4_offs, 'uint32')
        a4.append(val)
    return dict(A1=a1, A2=a2, A3=a3, A4=a4), offs


def parse_b(buf, offs):
    b1, offs = parse(buf, offs, 'int64')
    b2_size, offs = parse(buf, offs, 'uint16')
    b2_offs, offs = parse(buf, offs, 'uint32')
    b2 = []
    for _ in range(b2_size):
        val, b2_offs = parse_c(buf, b2_offs)
        b2.append(val)
    b3, offs = parse_d(buf, offs)
    b4, offs = parse(buf, offs, 'int8')
    b5, offs = parse(buf, offs, 'double')
    return dict(B1=b1, B2=b2, B3=b3, B4=b4, B5=b5), offs


def parse_c(buf, offs):
    c1, offs = parse(buf, offs, 'float')
    c2, offs = parse(buf, offs, 'uint16')
    c3, offs = parse(buf, offs, 'uint16')
    c4, offs = parse(buf, offs, 'double')
    c5, offs = parse(buf, offs, 'int8')
    c6, offs = parse(buf, offs, 'uint8')
    return dict(C1=c1, C2=c2, C3=c3, C4=c4, C5=c5, C6=c6), offs


def parse_d(buf, offs):
    d1, offs = parse(buf, offs, 'int64')
    d2 = []
    for _ in range(4):
        val, offs = parse(buf, offs, 'double')
        d2.append(val)
    d3, offs = parse(buf, offs, 'uint16')
    return dict(D1=d1, D2=d2, D3=d3), offs


def main(buf):
    return parse_a(buf, 3)[0]


buf1 = b'SRI\xd7\xd1\xc4\x9a\xd5\xf5,\xa3\xdem\xa2\xb4\xcc9q]\xd7\xdf\x14\x8c\x03' \
       b'\x00V\x00\x00\x00\xf5\xf1\x82\xe7\xed\xf4r=0\xa19\xf9x\xaf\xc0\xbf\x88\x19k' \
       b'\x11\r\x13\xe0?`a\x90\xb2\xdd\x85\xdd?\xc0\x8a\x05\xa20Q\xa7?%\xd0\xc8' \
       b'h_\x1e;\x0c\xd2\xe9\xbf\x02\x00\x8c\x00\x00\x00&\x18[>\xc4Hf\x8b\x1e\xe5' \
       b'(\xca\xb4\x88\xeb\xbf\xa2\xb1\xa8nU?i\xda#\xb0\xd2\xf3$l\xa3.\xef\xbf' \
       b"\xe0N\x02{\x16\xbf\x8eZ\x94\x17\xc4J\x1a\x0f\xc2\xc1\xee?\x04'T~\xbf\xf5" \
       b'\xb3?~\xb5'

print(main(buf1))

print()
