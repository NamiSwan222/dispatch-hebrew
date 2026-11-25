"""Shared paths and helpers for the Dispatch tools."""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work')
EN_DIR = os.path.join(WORK, 'en')       # the game's English tables as JSON (extracted, never committed)
HE_DIR = os.environ.get('TIRGUMIM_HE_DIR') or os.path.join(ROOT, 'translation', 'he')  # override: test builds
DEFAULT_GAME = r'D:\SteamLibrary\steamapps\common\Dispatch'
EXE = r'Dispatch\Binaries\Win64\Dispatch-Win64-Shipping.exe'
PAKS = r'Dispatch\Content\Paks'
UNREALPAK = os.environ.get('UNREALPAK', r'D:\UE\UE_5.8\Engine\Binaries\Win64\UnrealPak.exe')
PAK_NAME = 'zzz_tirgumim_he_P.pak'
# localization target -> its English .locres inside the paks (game-root relative)
TARGETS = {t: f'Dispatch/Content/Localization/{t}/en/{t}.locres'
           for t in ['101', '102', '103', '104', '105', '106', '107', '108', 'Shared', 'OtherContent']}


def load_json(path):
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')


def uid(ns, key):
    return f'{ns}|{key}'


def english():
    """{target: [{id, en, speaker, sort}]} in conversation order."""
    return {t: load_json(os.path.join(EN_DIR, t + '.json')) for t in TARGETS}


def hebrew():
    return {t: load_json(os.path.join(HE_DIR, t + '.json')) for t in TARGETS}
