"""Build the Hebrew pack files from translation/he/*.json.

    python tools/build.py [--allow-missing]

Needs work/en (tools/extract.py) and the proxy DLL (tools/proxy/build.cmd xinput1_3 <repo>/work/proxy-target).
Writes work/pack/files/, laid out like the game folder:
  Dispatch/Binaries/Win64/xinput1_3.dll                      launcher-only proxy (inert without -tirgumim_he)
  Dispatch/Binaries/Win64/tirgumim/he/zzz_tirgumim_he_P.pak   Hebrew .locres files + fonts
  Dispatch/Binaries/Win64/tirgumim/he/redirect.cfg           shows that pak in Content/Paks to the game
The Hebrew goes into the English slot (culture "en"), so the game must be set to English.
"""
import argparse, os, shutil, subprocess, sys
from common import ROOT, WORK, TARGETS, PAK_NAME, hebrew, uid
import locres, pak, build_fonts

WIN64 = 'Dispatch/Binaries/Win64'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--allow-missing', action='store_true')
    a = ap.parse_args()
    if not a.allow_missing and subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'coverage.py')]).returncode:
        sys.exit('coverage is not 100%: not building (use --allow-missing for a test build)')
    stage = os.path.join(WORK, 'build', 'pak')
    shutil.rmtree(stage, ignore_errors=True)
    he = hebrew()
    for t, path in TARGETS.items():
        version, entries = locres.read(os.path.join(WORK, 'en', t + '.locres'))
        out = [(ns, nsh, k, kh, sh, he[t].get(uid(ns, k)) or text) for ns, nsh, k, kh, sh, text in entries]
        dst = os.path.join(stage, path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        locres.write(dst, version, out)
    build_fonts.main(os.path.join(ROOT, 'fonts', 'src'), stage)
    shutil.rmtree(os.path.join(stage, '_work'))
    files = os.path.join(WORK, 'pack', 'files')
    shutil.rmtree(files, ignore_errors=True)
    data = os.path.join(files, WIN64, 'tirgumim', 'he')
    os.makedirs(data)
    pak.build(stage, os.path.join(data, PAK_NAME))
    with open(os.path.join(data, 'redirect.cfg'), 'w', newline='\r\n') as f:
        f.write('root=..\\..\\..\nadd=Dispatch\\Content\\Paks\\' + PAK_NAME + '\n')
    dll = os.path.join(WORK, 'proxy-target', 'release', 'tirgumim_proxy.dll')
    if not os.path.exists(dll):
        sys.exit(r'build the proxy first: tools\proxy\build.cmd xinput1_3 <repo>\work\proxy-target')
    shutil.copy(dll, os.path.join(files, WIN64, 'xinput1_3.dll'))
    print('pack files in', files)


if __name__ == '__main__':
    main()
