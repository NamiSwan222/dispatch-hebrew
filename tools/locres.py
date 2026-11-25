"""Read and write Unreal .locres files (versions 0-3, as written by UE 4.x).

    from locres import read, write
    entries = read(path)          # [(namespace, key, source_hash, text)]
    write(path, entries, version) # strings are de-duplicated again

Version 3 ("Optimized_CityHash64_UTF16") stores a hash of every namespace and key; we keep the ones read,
so nothing has to be re-hashed as long as the namespaces and keys stay the same.
"""
import struct

MAGIC = bytes.fromhex('0e14747567 4a03fc 4a15909d c3377f1b'.replace(' ', ''))


class Reader:
    def __init__(self, data):
        self.d, self.o = data, 0

    def u8(self):
        self.o += 1
        return self.d[self.o - 1]

    def i32(self):
        self.o += 4
        return struct.unpack_from('<i', self.d, self.o - 4)[0]

    def u32(self):
        self.o += 4
        return struct.unpack_from('<I', self.d, self.o - 4)[0]

    def i64(self):
        self.o += 8
        return struct.unpack_from('<q', self.d, self.o - 8)[0]

    def fstr(self):
        n = self.i32()
        if n == 0:
            return ''
        if n > 0:
            s = self.d[self.o:self.o + n - 1].decode('latin-1')
            self.o += n
            return s
        s = self.d[self.o:self.o - 2 * n - 2].decode('utf-16-le')
        self.o += -2 * n
        return s


def fstr(s):
    if s == '':
        return struct.pack('<i', 0)
    try:
        b = s.encode('ascii')
        return struct.pack('<i', len(b) + 1) + b + b'\0'
    except UnicodeEncodeError:
        b = s.encode('utf-16-le')
        return struct.pack('<i', -(len(b) // 2 + 1)) + b + b'\0\0'


def read(path):
    """Returns (version, entries); entries = [(ns, ns_hash, key, key_hash, source_hash, text)]."""
    r = Reader(open(path, 'rb').read())
    version = 0
    if r.d[:16] == MAGIC:
        r.o = 16
        version = r.u8()
    strings = None
    if version >= 1:
        off = r.i64()
        save = r.o
        r.o = off
        strings = []
        for _ in range(r.i32()):
            s = r.fstr()
            if version >= 2:
                r.i32()  # ref count
            strings.append(s)
        r.o = save
    if version >= 2:
        r.u32()  # entries count
    out = []
    for _ in range(r.u32()):
        nsh = r.u32() if version >= 2 else 0
        ns = r.fstr()
        for _ in range(r.u32()):
            kh = r.u32() if version >= 2 else 0
            key = r.fstr()
            sh = r.u32()
            text = strings[r.i32()] if version >= 1 else r.fstr()
            out.append((ns, nsh, key, kh, sh, text))
    return version, out


def write(path, version, entries):
    if version < 2:
        raise ValueError('only locres v2/v3 can be written')
    table, refs, index = [], [], {}
    body = bytearray()
    groups = {}
    for ns, nsh, key, kh, sh, text in entries:
        groups.setdefault((ns, nsh), []).append((key, kh, sh, text))
    body += struct.pack('<I', len(entries))
    body += struct.pack('<I', len(groups))
    for (ns, nsh), items in groups.items():
        body += struct.pack('<I', nsh) + fstr(ns) + struct.pack('<I', len(items))
        for key, kh, sh, text in items:
            if text not in index:
                index[text] = len(table)
                table.append(text)
                refs.append(0)
            refs[index[text]] += 1
            body += struct.pack('<I', kh) + fstr(key) + struct.pack('<Ii', sh, index[text])
    head = MAGIC + bytes([version])
    off = len(head) + 8 + len(body)
    tail = struct.pack('<i', len(table)) + b''.join(fstr(s) + struct.pack('<i', n) for s, n in zip(table, refs))
    with open(path, 'wb') as f:
        f.write(head + struct.pack('<q', off) + body + tail)
