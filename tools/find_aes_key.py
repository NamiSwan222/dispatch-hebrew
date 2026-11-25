"""Find an Unreal pak AES-256 key inside the game executable.

    python find_aes_key.py <game.exe> <encrypted.pak>

Decrypts the first block of the pak index with each candidate and checks that it starts with a sane
mount-point FString ("../"). Candidates: keys built from runs of `mov dword ptr [..], imm32` in code
(how UE 4.2x embeds the key), then every 4-byte-aligned 32 bytes in the data sections.
"""
import os, re, struct, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def first_index_block(pak):
    sz = os.path.getsize(pak)
    with open(pak, 'rb') as f:
        f.seek(sz - 221)
        foot = f.read(221)
        off = struct.unpack_from('<q', foot, 17 + 8)[0]
        f.seek(off)
        return f.read(16)


def find_key(exe, pak):
    block = first_index_block(pak)

    def ok(key):
        d = Cipher(algorithms.AES(key), modes.ECB()).decryptor().update(block)
        n = struct.unpack_from('<i', d)[0]
        return 0 < n < 256 and d[4:7] == b'../'

    d = open(exe, 'rb').read()
    pe = struct.unpack_from('<I', d, 0x3c)[0]
    n = struct.unpack_from('<H', d, pe + 6)[0]
    osz = struct.unpack_from('<H', d, pe + 20)[0]
    secs = [struct.unpack_from('<8sIIII', d, pe + 24 + osz + i * 40) for i in range(n)]
    for name, vs, va, rs, ro in secs:
        if name.startswith(b'.text'):
            blob = d[ro:ro + rs]
            imms = [m.group(1) for m in re.finditer(rb'\xc7[\x40-\x47\x80-\x87\x44\x84].{1,5}?(.{4})', blob, re.S)]
            for i in range(len(imms) - 7):
                k = b''.join(imms[i:i + 8])
                if ok(k):
                    return k
    for name, vs, va, rs, ro in secs:
        if name.startswith((b'.rdata', b'.data')):
            blob = d[ro:ro + rs]
            for i in range(0, len(blob) - 32, 4):
                k = blob[i:i + 32]
                if k.count(0) <= 4 and ok(k):
                    return k
    raise SystemExit('AES key not found')


if __name__ == '__main__':
    print(find_key(sys.argv[1], sys.argv[2]).hex())
