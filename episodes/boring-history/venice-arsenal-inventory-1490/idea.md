---
channel: boring-history
status: scripting
created: 2026-04-11
updated: 2026-04-11
tags: [venice, arsenal, inventory, weapons, shipbuilding, 15th-century, bureaucracy, maritime]
---

# Venice Arsenale Inventory, 1490

## Angle / Hook
> The Arsenale di Venezia was the largest industrial complex in the world in 1490 — a walled city within a city, employing three thousand workers, producing a warship every few days. Twice a year, the Provveditori all'Arsenal dispatched a team of scribes to count everything: every cannon by calibre and founder, every coil of rope by weight, every oar in every rack, every barrel of pitch, every hull in the covered sheds, in varying states of repair. In November 1490, you are the junior scribe assigned to the winter inventory. This is the register you compiled over eleven days.

## Target Audience
- People who want: sleep, slow narration, the meditative rhythm of lists and numbers
- Mood target: deep relaxation, second-person immersion into clerical routine, the sensation of being buried in columns of inventory figures that do not add up

---

## Outline

| # | Section | Duration | Chunks | Description |
|---|---------|----------|--------|-------------|
| 0 | Intro | ~5 min | 2 | November 4, 1490. Water gate of Arsenale Vecchio at dawn. Letter of appointment presented. Last spring's register received. Eleven-day task briefed. |
| 1 | The Cannon Hall | ~30 min | 9 | Days 1–2. Ordnance hall. bombardelle, passavolante, colubrina, falconetto, petriera — by calibre, founder, condition. 12 with no founder mark. 7 unserviceable. The 1487 discrepancy introduced. |
| 2 | Rope, Sail, and Timber | ~27 min | 8 | Days 3–4. The Tana, 316 metres long. Hemp rope by thickness, tarred cable, running rigging. Timber yard — oak, larch, elm at varying seasoning. Dalmatian timber storage dispute unresolved. |
| 3 | The Galley Shed Assessment | ~27 min | 8 | Days 5–8. 38 hulls. navigabile / da raddobbo / da disarmare. The condemned hull accounting question. The 1471 galea grossa listed da raddobbo since 1483, repair estimate risen from 300 to 740 ducati. |
| 4 | Oars, Anchors, and the Cyprus Loan | ~23 min | 7 | Days 9–10. Oar racks, 22,411 oars in seven lengths. Rack 17 — Cyprus-stamped oars, the 1487 loan, Cyprus annexed 1489. Anchor inventory by weight class. The Bucintoro entry. |
| 5 | Arms, Armour, and Final Certification | ~17 min | 5 | Day 11. Crossbows, bolts, pavises, plate armour, mail coats, helmets. Old numbering format pre-1465. Total 3,214 serviceable vs stated wartime requirement 6,000. Register signed. |
| 6 | Outro | ~5 min | 2 | Register submitted November 14. Three Provveditori queries in December. Responses not found. Register survives in Archivio di Stato di Venezia. That is all. |

---

## Recurring Motifs (unresolved throughout)
1. **The 1487 cannon discrepancy** — two petriere whose bore measurements do not match the 1487 register entry; master responsible no longer employed; query to Provveditori unanswered since March 1490
2. **The Cyprus oar loan** — 1,200 oars dispatched to Famagusta in June 1487 under Council of Ten authorisation; Cyprus annexed by Ottomans 1489; oars absent from rack seventeen but remain on the register as "on loan"
3. **The condemned hulls** — 13 hulls da disarmare; whether to retain at salvage value or strike from register entirely has been under review since 1488; no Senate resolution passed

---

## Script Notes

- **POV:** Second-person (`you`). You are a junior scribe (scrivan) assigned by the Provveditori's office.
- **Tone:** Flat logistical register. No commentary on Venice's power or geopolitical position.
- **Pacing:** Very slow. Catalogue entries are substance, not filler — read each one fully.
- **Avoid:** "The most powerful navy…", anything about the Ottoman threat, "Venice was known for…", exclamation marks, "fascinating", rhetorical questions, cliffhangers.
- **Language:** English

---

## Asset Requirements

### Voice (TTS)
- Voice: Charon (Gemini TTS — deep, authoritative)
- Provider: Gemini (`gemini-2.5-flash-preview-tts`)
- Speed: 0.95 (FFmpeg atempo — slightly slow)
- Gen script: `tools/gen_audio.py`

### Music nền
- Mood: subliminal static drone, almost no melody, something like a large stone building with water nearby
- BPM range: 50–60
- Avoid: anything nautical or dramatic, no drums, no lute or Renaissance feel

### Thumbnail
- Subject: A Venetian scribe in dark robes standing in the cannon storage hall, dwarfed by rows of bronze cannon on trestles, holding an open register
- Mood / color palette: cool grey stone, amber bronze, deep shadow, flat November light

**Prompt 1** — *hook: the lone scribe among the cannon*
```
A Venetian government scribe in dark wool robes standing alone in a vast stone storage hall, rows of large bronze cannon on wooden trestles receding into shadow on both sides, holding an open parchment register, flat grey November light entering from high arched windows, dust motes visible in the beam, classical oil painting style, cool grey and amber bronze palette, cinematic atmosphere, one line of bold serif title text centered near the bottom: large gold letters #D4A017 "HISTORY FOR SLEEP", heavy drop shadow, no other text in image, 16:9
```

**Prompt 2** — *hook: the Tana scale*
```
Interior of an extremely long Renaissance-era rope factory, a vast stone-vaulted hall receding into near-darkness, great coils of hemp rope hanging from ceiling hooks at intervals, stone floor dusted with pale hemp fibre, two small figures of clerks visible in the far distance, a single lantern casting warm light in the mid-ground, classical oil painting style, cool stone grey and warm amber lamplight, cinematic scale composition, one line of bold serif title text centered near the bottom: large gold letters #D4A017 "HISTORY FOR SLEEP", heavy drop shadow, no other text in image, 16:9
```

**Prompt 3** — *hook: galley shed scale*
```
Interior of a Renaissance Venetian galley shed, a large weathered wooden galley hull resting on support blocks dominating the centre, massive timber roof trusses arching overhead, water visible through a half-open gate at the far end, a lone figure of a scribe walking alongside the hull as a small silhouette, cold grey winter light, classical oil painting style, desaturated palette with cool blue-grey and dark brown, one line of bold serif title text centered near the bottom: large gold letters #D4A017 "BORING HISTORY FOR SLEEP", heavy drop shadow, no other text in image, 16:9
```

---

## YouTube Description

```
Venice Arsenale Inventory Records, 1490

In November of fourteen hundred and ninety, a scribe from the office of the Provveditori all'Arsenal was assigned to conduct the winter inventory of the Venetian Arsenal — at that time the largest industrial facility in Europe.

This recording covers the eleven-day inventory as documented: the ordnance register of the cannon hall, the rope and timber assessment of the Tana and the wood stores, the condition survey of thirty-eight galley hulls in the covered sheds, the oar and anchor count, and the armoury assessment. Three administrative questions raised during the inventory remained unresolved at the time the register was certified.

Duration: approximately 1 hour 45 minutes. Narrated at a slow pace. Ambient drone at low volume.

---

00:00 Intro — Arsenale, November 4, 1490
XX:XX Part 1 — The Cannon Hall
XX:XX Part 2 — Rope, Sail, and Timber
XX:XX Part 3 — The Galley Shed Assessment
XX:XX Part 4 — Oars, Anchors, and the Cyprus Loan
XX:XX Part 5 — Arms, Armour, and Final Certification
XX:XX Outro

#SleepStories #BoringHistory #Venice
```

---

## Production Checklist

- [x] `idea.md` hoàn chỉnh
- [x] `script.md` (index) tạo xong
- [x] `script/00-intro.md` viết xong
- [x] `script/01-cannon-hall.md` viết xong
- [x] `script/02-tana-timber.md` viết xong
- [x] `script/03-galley-sheds.md` viết xong
- [x] `script/04-oars-anchors.md` viết xong
- [x] `script/05-armoury.md` viết xong
- [x] `script/06-outro.md` viết xong
- [ ] `script/image-prompts.md` hoàn chỉnh
- [ ] `script/audio-image-map.md` hoàn chỉnh
- [ ] TTS generated → `assets/audio/`
- [ ] Images generated → `assets/images/`
- [ ] Music chọn xong → `assets/music/`
- [ ] Video assembled
- [ ] Thumbnail created → `exports/thumbnail.png`
- [ ] Export final → `exports/final.mp4`
- [ ] Uploaded YouTube
