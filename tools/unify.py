"""Make names and terms consistent across all translation files (re-runnable).

    python tools/unify.py

Each pair replaces a variant the batch translators used with the form chosen for glossary.md.
"""
import os
from common import HE_DIR, hebrew, save_json

REPLACE = [
    ("אינביזיכלבה", "אינביזיביץ'"),
    ("אינביזי-כלבה", "אינביזיביץ'"),
    ("המוקדנים", "המשגרים"), ("מוקדנים", "משגרים"), ("המוקדן", "המשגר"), ("מוקדן", "משגר"),
    ("טראק סטאר", "טרק סטאר"),
    ("ואנדרסטנק", "ונדרסטנק"), ("ואנדרסטינק", "ונדרסטינק"), ("ואנדקו", "ונדקו"),
    ("קריפטו נייט", "ליל הקריפטו"),
    ("אקווילבריום", "אקוויליבריום"),
    ("חטיבת האמיצים", "הבריגדה האמיצה"),
    ("פנומה-פאן", "פנומה-מעריץ"),
    ("אתה ועוד {Percentage}", "אתה ו-{Percentage}"),
    ("ימי חופש ", "ימי חופשה "),
    ("לייטנינגסטרק", "מוכה-ברק"), ("לייטנינגסטראק", "מוכה-ברק"),
    ("רד רינג", "הטבעת האדומה"),
    ("פרוטו-פאלס", "פרוטו-פולס"),
    ("ת'אנדרקאק", "קרנן-רעם"),
]
# whole-word replacements (regex), for short names that occur inside other words
import re
WORDS = [("מאל", "מל"), ("צ'אד(?= |$|[.,!?])(?=.*(כת|כנסיי|שד))", "צ'אאד")]


def main():
    he = hebrew()
    changed = 0
    for t, d in he.items():
        for k, v in d.items():
            n = v
            for a, b in REPLACE:
                n = n.replace(a, b)
            for a, b in WORDS:
                n = re.sub(r'(?<![א-ת])' + a + r'(?![א-ת])', b, n)
            if n != v:
                d[k] = n
                changed += 1
        save_json(os.path.join(HE_DIR, t + '.json'), dict(sorted(d.items())))
    print('changed', changed, 'strings')


if __name__ == '__main__':
    main()
