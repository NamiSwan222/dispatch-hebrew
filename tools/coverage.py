"""Coverage check: every English string needs Hebrew with the same markup.

    python tools/coverage.py                 report; exit 1 if anything is missing or broken
    python tools/coverage.py --batch 300     also write what's missing to work/todo/batch-NNN.json

Markup that must survive: the set of {Placeholders}, every <Style> tag and </>, and the number of ^
(highlight markers). Strings without letters (numbers, symbols, placeholders only) count as done.
translation/keep.json can list ids that may stay as they are (names written in Latin on purpose).
"""
import argparse, collections, os, re, sys
from common import ROOT, WORK, english, hebrew, load_json, save_json

PH = re.compile(r'\{\w+\}')
TAG = re.compile(r'<[A-Za-z_]+>|</>')
HEB = re.compile(r'[֐-׿]')


def markup_ok(en, he):
    return (set(PH.findall(en)) == set(PH.findall(he))
            and collections.Counter(TAG.findall(en)) == collections.Counter(TAG.findall(he))
            and en.count('^') == he.count('^'))


def check():
    keep = set(load_json(os.path.join(ROOT, 'translation', 'keep.json')).get('ids', []))
    en, he = english(), hebrew()
    total = done = 0
    missing, broken = [], []
    for t, rows in en.items():
        for r in rows:
            total += 1
            src = r['en']
            plain = TAG.sub('', PH.sub('', src))
            if not re.search(r'[A-Za-z]{2}', plain) or r['id'] in keep:
                done += 1
                continue
            h = he[t].get(r['id'])
            if not h:
                missing.append((t, r))
            elif not markup_ok(src, h):
                broken.append((t, r, h, 'markup'))
            elif not HEB.search(h):
                broken.append((t, r, h, 'no Hebrew'))
            else:
                done += 1
    return total, done, missing, broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', type=int)
    a = ap.parse_args()
    total, done, missing, broken = check()
    for t, r, h, why in broken:
        print(f'BROKEN ({why}) {t} {r["id"]}\n  en: {r["en"]!r}\n  he: {h!r}')
    print(f'coverage: {done}/{total} = {100 * done / total:.2f}%  missing {len(missing)}  broken {len(broken)}')
    if a.batch:
        todo = os.path.join(WORK, 'todo')
        os.makedirs(todo, exist_ok=True)
        for f in os.listdir(todo):
            os.remove(os.path.join(todo, f))
        items = missing + [(t, r) for t, r, _, _ in broken]
        for i in range(0, len(items), a.batch):
            b = {}
            for t, r in items[i:i + a.batch]:
                b.setdefault(t, []).append({'id': r['id'], 'speaker': r['speaker'], 'en': r['en']})
            save_json(os.path.join(todo, f'batch-{i // a.batch:03d}.json'), b)
        print(f'{(len(items) + a.batch - 1) // a.batch} batches in work/todo')
    sys.exit(0 if not missing and not broken else 1)


if __name__ == '__main__':
    main()
