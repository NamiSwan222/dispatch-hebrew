"""Extract Dispatch's English text into work/en (needs UnrealPak from an Unreal Engine install).

    python tools/extract.py [--game "<install folder>"]

The paks are AES-encrypted; the key is found in the game's own exe (find_aes_key.py) and only used
locally. For every localization target it writes work/en/<target>.locres (the original, kept for the
build: hashes and order come from it) and work/en/<target>.json: [{id, en, speaker, sort}] in
conversation order, with the speaker and order taken from the .po file next to the .locres.
"""
import argparse, base64, glob, json, os, re, shutil, subprocess, tempfile
from common import DEFAULT_GAME, EN_DIR, EXE, PAKS, TARGETS, UNREALPAK, save_json, uid
from find_aes_key import find_key
import locres


def parse_po(path):
    """{ "ns,key": (speaker, sort) }"""
    out, speaker, sort = {}, '', ''
    for line in open(path, encoding='utf-8-sig'):
        if line.startswith('#. Speaker:'):
            speaker = line.split(':', 1)[1].strip()
        elif line.startswith('#. SortingString:'):
            sort = line.split(':', 1)[1].strip()
        elif line.startswith('msgctxt '):
            ctx = json.loads(line[8:].strip())
            out[ctx] = (speaker, sort)
            speaker, sort = '', ''
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default=DEFAULT_GAME)
    a = ap.parse_args()
    paks = sorted(glob.glob(os.path.join(a.game, PAKS, '*.pak')))
    key = find_key(os.path.join(a.game, EXE), paks[0])
    tmp = tempfile.mkdtemp()
    keys = os.path.join(tmp, 'keys.json')
    json.dump({'EncryptionKey': {'Name': 'game', 'Guid': '00000000-0000-0000-0000-000000000000',
                                 'Key': base64.b64encode(key).decode()}}, open(keys, 'w'))
    out = os.path.join(tmp, 'x')
    for p in paks:
        subprocess.run([UNREALPAK, p, '-Extract', out, '-Filter=*Localization*/en/*', f'-cryptokeys={keys}'],
                       capture_output=True)
    os.makedirs(EN_DIR, exist_ok=True)
    found = {os.path.basename(f): f for f in glob.glob(os.path.join(out, '**', 'en', '*.*'), recursive=True)}
    for t in TARGETS:
        src = found[t + '.locres']
        shutil.copy(src, os.path.join(EN_DIR, t + '.locres'))
        po = parse_po(found[t + '.po']) if t + '.po' in found else {}
        _, entries = locres.read(src)
        rows = []
        for i, (ns, _, k, _, _, text) in enumerate(entries):
            sp, so = po.get(f'{ns},{k}', ('', ''))
            rows.append({'id': uid(ns, k), 'en': text, 'speaker': sp, 'sort': so or f'~{i:06d}'})
        rows.sort(key=lambda r: r['sort'])
        save_json(os.path.join(EN_DIR, t + '.json'), rows)
        print(t, len(rows), 'strings')
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
