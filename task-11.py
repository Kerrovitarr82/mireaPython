from struct import *

FMT = dict(
    char='>c',
    int8='>b',
    uint8='>B',
    int16='>h',
    uint16='>H',
    int32='>i',
    uint32='>I',
    int64='>q',
    uint64='>Q',
    float='>f',
    double='>d',
)


def parse(buf, offs, ty):
    data = unpack_from(FMT[ty], buf, offs)
    data = data[0]
    of = offs + calcsize(FMT[ty])
    return data, of


def parse_a(buf, offs):
    a1, offs = parse_b(buf, offs)
    a2, offs = parse(buf, offs, 'uint64')
    a3, offs = parse(buf, offs, 'int32')
    a4, offs = parse(buf, offs, 'double')
    return dict(A1=a1, A2=a2, A3=a3, A4=a4), offs


def parse_b(buf, offs):
    b1, offs = parse(buf, offs, 'int32')
    b2_size, offs = parse(buf, offs, 'uint32')
    b2_offs, offs = parse(buf, offs, 'uint32')
    b2 = []
    for _ in range(b2_size):
        val, b2_offs = parse_c(buf, b2_offs)
        b2.append(val)
    b3, offs = parse(buf, offs, 'int8')
    b4, offs = parse_d(buf, offs)
    b5, offs = parse(buf, offs, 'uint32')
    return dict(B1=b1, B2=b2, B3=b3, B4=b4, B5=b5), offs


def parse_c(buf, offs):
    c1, offs = parse(buf, offs, 'int32')
    c2, offs = parse(buf, offs, 'uint64')
    c3_size, offs = parse(buf, offs, 'uint32')
    c3_offs, offs = parse(buf, offs, 'uint16')
    c3 = []
    for _ in range(c3_size):
        val, c3_offs = parse(buf, c3_offs, 'uint8')
        c3.append(val)
    return dict(C1=c1, C2=c2, C3=c3), offs


def parse_d(buf, offs):
    d1, offs = parse(buf, offs, 'int64')
    d2, offs = parse(buf, offs, 'uint32')
    d3, offs = parse(buf, offs, 'uint8')
    d4, offs = parse(buf, offs, 'int64')
    d5 = []
    for _ in range(8):
        val, offs = parse(buf, offs, 'uint8')
        d5.append(val)
    d6 = []
    for _ in range(4):
        val, offs = parse(buf, offs, 'int32')
        d6.append(val)
    return dict(D1=d1, D2=d2, D3=d3, D4=d4, D5=d5, D6=d6), offs


def main(buf):
    return parse_a(buf, 4)[0]


print(main(b'\xb8XUK\x8c\xd1;\x85\x00\x00\x00\x03\x00\x00\x00^\xfb\xd6\xb2>\xde\xe0o\x18'
           b'\x10O\x9c\x05\xb0a\x10\xe7\xf6&\x8ck\xc3\xdb\x9cs\xd13\x0b"\xfaK\xf5\x91'
           b'7\xe40\x97\x95\xf2\x05Bz\x88\x10\x96$#\xa9\xf5X5\xdeox\x87\x97\x97!:\xe4\x8a'
           b'\x00\xc5?\xe5\xde`\x8d\xf5\xac*n\xc0\xa8\x07\xb2J\xb0\xb2\xba\xc6\x11%/\xda'
           b'Z?\x16\xcd7\xf7\x00\x00\x00\x02\x00V\x0b\x15\x0cR\xc1yK\xe7B!-S'
           b'\x00\x00\x00\x04\x00XR("\x9fy\xda\xf5?\x02U\xe9o\x00\x00\x00\x02\x00\\'))
