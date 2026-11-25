# Glossary: Dispatch (Hebrew)

Dispatch is an adult workplace comedy about superheroes: Robert Robertson (ex-hero Mecha Man) works as a
dispatcher at SDN, sending a team of misfit ex-villains to emergencies. Tone: sharp, sarcastic, modern
spoken Hebrew, like a good Israeli subtitle track for an adult animated series. Swearing stays swearing
(fuck = זין / לעזאזל / מזדיין, depending on the line; shit = חרא; asshole = מניאק / אידיוט), but keep it
natural, not heavier than the English. Short lines stay short.

## Characters (transliterated, as Hebrew fans would write them)

| English | Hebrew | gender |
|---|---|---|
| Robert (Robertson) | רוברט (רוברטסון) | m |
| Mecha Man | מכה-מן | m |
| Blonde Blazer / Mandy | בלונד בלייזר / מנדי | f |
| Invisigal | אינביזיגל | f |
| Flambae | פלאמביי | m |
| Punch Up | פאנץ' אפ | m |
| Prism | פריזם | f |
| Sonar | סונאר | m |
| Malevola | מלבולה | f |
| Coupé | קופה | f |
| Golem | גולם | m |
| Waterboy | ווטרבוי | m |
| Phenomaman | פנומנמן | m |
| Chase | צ'ייס | m |
| Royd | רויד | m |
| Shroud | שראוד | m |
| Toxic | טוקסיק | m |
| Galen | גיילן | m |
| Z-Team | צוות Z | |
| Other hero/villain names | transliterate by sound; translate only if the name is a plain English word joke that would be lost (decide once, keep it) | |

## Names decided during translation

| English | Hebrew |
|---|---|
| Invisibitch | אינביזיביץ' |
| Track Star | טרק סטאר |
| Starblazer | סטארבלייזר |
| Vanderstenk (Willem) / Vanderstink / VANDCO | (וילם) ונדרסטנק / ונדרסטינק / ונדקו |
| Lightningstruck | מוכה-ברק |
| Crypto Night | ליל הקריפטו |
| Equilibrium / Sweetalker / Pom Pom / Brickhouse / Brainbook | אקוויליבריום / סוויטוקר / פום פום / בריקהאוס / בריינבוק |
| Brave Brigade | הבריגדה האמיצה |
| Phoenix Program / Astral Pulse / Proto Pulse | תוכנית הפניקס / הפולס האסטרלי / פרוטו-פולס |
| Red Ring / The Sardine / Mole People | הטבעת האדומה / הסרדין / אנשי החפרפרת |
| Torrance / TPD | טורנס / משטרת טורנס |
| Phenoma-Fan | פנומה-מעריץ |
| Coop / Visi / Mal / Robbie / Bobby | קופ / ויזי / מל / רובי / בובי |
| Beef (Robert's dog) | ביף |
| Stats: Combat / Mobility / Charisma / Intellect / Vigor | קרב / ניידות / כריזמה / תבונה / חיוניות |
| "^You and {Percentage}^ of players ..." | "^אתה ו-{Percentage}^ מהשחקנים ..." (plural verb) |
| social handles (@TorrancePD...) | Hebrew handles with underscores (@משטרת_טורנס) |

## World

| English | Hebrew |
|---|---|
| SDN (Superhero Dispatch Network) | SDN (רשת השיגור לגיבורי-על) |
| dispatch / dispatcher | שיגור / משגר (ranks: משגר מתלמד / זוטר / שותף / עוזר) |
| shift | משמרת |
| hero / superhero | גיבור / גיבור-על |
| villain / supervillain | נבל / נבל-על |
| call / emergency | קריאה / מקרה חירום |
| assign / recall | שבץ / החזר |
| success / failure | הצלחה / כישלון |
| power | כוח |
| hacking | פריצה |
| Los Angeles | לוס אנג'לס |
| episode | פרק |

## UI

| English | Hebrew |
|---|---|
| Continue / New Game / Load / Save | המשך / משחק חדש / טעינה / שמירה |
| Settings / Audio / Video / Controls / Accessibility | הגדרות / שמע / תצוגה / שליטה / נגישות |
| Subtitles | כתוביות |
| Back / Confirm / Cancel / Apply | חזרה / אישור / ביטול / החל |
| Quit | יציאה |
| Choice / Timer | בחירה / טיימר |

## Rules for translators

- Keep markup exactly: `{Name}` placeholders (same names), `<Italic>`…`</>` and other `<Tag>`…`</>` (wrap the
  matching Hebrew words), and every `^` (highlight markers; same count, around the matching Hebrew words).
- `{X}|plural(one=..., other=...)` / `|ordinal(...)`: keep the structure, put Hebrew forms inside
  (e.g. `{NumMinutes} {NumMinutes}|plural(one=דקה, other=דקות)`); for ordinal use `other=` only.
- `[Choice]` labels in square brackets: translate inside the brackets, keep the brackets.
- Speaker and gender: lines carry the speaker. Use the speaker's gender for first person and the
  listener's for second person; Robert is male, the player-choice lines (no speaker / NodeTitle) are
  Robert's. When the listener's gender is unknown, prefer phrasing that avoids it.
- Hacking/terminal texts (ALL CAPS, `// >>` prefixes): keep the symbols, translate the words.
- Write Hebrew in logical order; the engine lays it out right-to-left. No niqqud.
