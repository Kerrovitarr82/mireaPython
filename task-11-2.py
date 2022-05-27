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
)


def parse(buf, offs, ty):
    data = unpack_from(FMT[ty], buf, offs)
    data = data[0]
    of = offs + calcsize(FMT[ty])
    return data, of


def parse_a(buf, offs):
    a1, offs = parse(buf, offs, 'float')
    a2, offs = parse(buf, offs, 'uint64')
    a3, offs = parse_b(buf, offs)
    a4_size, offs = parse(buf, offs, 'uint32')
    a4_offs, offs = parse(buf, offs, 'uint16')
    a4 = []
    for _ in range(a4_size):
        val, a4_offs = parse(buf, a4_offs, 'char')
        a4.append(val.decode())
    a5, offs = parse_e(buf, offs)
    return dict(A1=a1, A2=a2, A3=a3, A4=''.join(a4), A5=a5), offs


def parse_b(buf, offs):
    b1_size, offs = parse(buf, offs, 'uint16')
    b1_offs, offs = parse(buf, offs, 'uint32')
    b1 = []
    for _ in range(b1_size):
        val, b1_offs = parse_c(buf, b1_offs)
        b1.append(val)
    b2, offs = parse_d(buf, offs)
    b3, offs = parse(buf, offs, 'int8')
    return dict(B1=b1, B2=b2, B3=b3), offs


def parse_c(buf, offs):
    c1, offs = parse(buf, offs, 'uint64')
    c2, offs = parse(buf, offs, 'uint32')
    c3, offs = parse(buf, offs, 'int16')
    c4 = []
    for _ in range(2):
        val, offs = parse(buf, offs, 'uint16')
        c4.append(val)
    return dict(C1=c1, C2=c2, C3=c3, C4=c4), offs


def parse_d(buf, offs):
    d1, offs = parse(buf, offs, 'uint16')
    d2, offs = parse(buf, offs, 'int32')
    d3, offs = parse(buf, offs, 'uint64')
    return dict(D1=d1, D2=d2, D3=d3), offs


def parse_e(buf, offs):
    e1, offs = parse(buf, offs, 'uint32')
    e2, offs = parse(buf, offs, 'int16')
    e3, offs = parse(buf, offs, 'int64')
    e4, offs = parse(buf, offs, 'uint32')
    e5_size, offs = parse(buf, offs, 'uint32')
    e5_offs, offs = parse(buf, offs, 'uint16')
    e5 = []
    for _ in range(e5_size):
        val, e5_offs = parse(buf, e5_offs, 'uint8')
        e5.append(val)
    e6, offs = parse(buf, offs, 'int16')
    return dict(E1=e1, E2=e2, E3=e3, E4=e4, E5=e5, E6=e6), offs


def main(buf):
    return parse_a(buf, 4)[0]


print(main(b'\xf8UQJ>S4\xbf\nK*\x7fB\x8b/\xc8\x04\x00E\x00\x00\x00\xc1c\xb54\x03K'
           b'\x84K\xec\x7f\x15\x8d\xd2l\x9e\x03\x00\x00\x00\x8d\x00x\xc0\x9a\xfe@'
           b'{\x1c\x83\x84\x85\x14<\x1e\xe4.\xd3\xeb\x19\x03\x00\x00\x00\x90\x00\xa5'
           b'\xf8\xbb$\x9f\r\xa4\xc6\xa8H\xe2C\x16w\x00\xd6\x11\xc2\x0b\xf0H\xe2\xaa\x1an'
           b'\xca&\x99j\x98f\xe2H\x93L.iA\xa8\x18\x13\xe4sM\x9f\xc7\xa9\xd2J\xd1a\xd7V'
           b'\\\xf5\x08\xffs\xd4\xbb\xb1\x84\xfd\xcdG\xc3\xa8\xc8):\xcf\x03\x0f\xd5xno'
           b'x\xd4\xb9'))
