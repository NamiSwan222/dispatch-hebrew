# Dispatch: Hebrew translation (fan project)

A full Hebrew translation of **Dispatch** (AdHoc Studio, 2025; Steam app 2592160): all eight episodes' dialogue and
subtitles, Robert's choices, shift calls and outcomes, hacking screens, story notifications, choice statistics,
menus and settings. About 12,500 strings / 86,000 English words, translated by us (no fan translation existed).

Unofficial fan project, for personal use. Not affiliated with AdHoc Studio. This repository holds only our tools,
our Hebrew text and OFL fonts. No game files and no English text.

## How it works

- The game's text is standard Unreal localization: `Dispatch/Content/Localization/<target>/en/<target>.locres` for
  the targets 101–108 (one per episode), `Shared` (UI) and `OtherContent`.
- `tools/extract.py` reads them from your install with UnrealPak. The paks are AES-encrypted; the key is found in
  the game's own exe at run time (`tools/find_aes_key.py`) and never stored. The speaker of each line and the
  conversation order come from the `.po` files next to the `.locres`.
- `tools/build.py` writes Hebrew `.locres` files (`tools/locres.py`, same namespaces, keys and hashes) and
  replacement fonts into a small unencrypted pak, `zzz_tirgumim_he_P.pak` (`tools/pak.py`). Unreal mounts `_P`
  paks above the game's own. The Hebrew sits in the English slot, so the launcher starts the game with
  `-culture=en`.
- Fonts: every Latin font slot (Aktiv Grotesk, Tomorrow, Montserrat, Noto Sans, Orbitron, Rajdhani, Barlow,
  Roboto, the mono fonts, SCHABO) gets Noto Sans + Noto Sans Hebrew merged at the slot's weight, narrower for
  the condensed families (`tools/build_fonts.py`; sources and licences in `fonts/src`, SIL OFL 1.1).
- Right-to-left: Unreal lays out Hebrew right-to-left by itself, so the text is stored in logical order.

### Hebrew only from the launcher

Same design as our Avatar pack: `Dispatch\Binaries\Win64\xinput1_3.dll` is a proxy (source `tools/proxy`) that
forwards XInput to System32 and does nothing unless the game was started with `-tirgumim_he`. With the flag it
makes `Content\Paks` *appear* to contain our pak, which really lives in `Dispatch\Binaries\Win64\tirgumim\he\`.
Nothing is written to the game folder, so a Steam launch is always the original English game. The launcher
starts it through Steam (the exe restarts itself through Steam, which drops environment variables).

## Build

Python 3.11+ with `fonttools` and `cryptography`, Rust + Visual Studio Build Tools, and an Unreal Engine install
for `UnrealPak.exe` (`UNREALPAK` env var; default UE 5.8).

```
python tools/extract.py --game "<install>"          # -> work/en (not committed)
python tools/coverage.py                             # must say 100%
tools\proxy\build.cmd xinput1_3 %CD%\work\proxy-target
python tools/build.py                                # -> work/pack/files
tools\make-pack.cmd 1.0.0                            # the launcher's make-pack -> work/out
```

## Translating

- `translation/he/<target>.json`: `{"<namespace>|<key>": "Hebrew"}`, logical order.
- `glossary.md`: characters, world terms, UI terms, tone and markup rules.
- `python tools/coverage.py --batch 300` lists what's missing or has broken markup (`{Name}`, `<Tag>`…`</>`, `^`)
  and writes batches with speakers to `work/todo/`; `tools/merge.py` merges translated batches back.
