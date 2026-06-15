---
channel: boring-history
status: idea
created: 2026-04-17
updated: 2026-04-17
tags: [roman-empire, census, tax-records, provincial-administration, bureaucratic-history]
---

# Roman Provincial Census and Tax Records, 5 AD

## Angle / Hook
> You are a scriba officialis assigned to the governor's census office in a Roman provincial capital. It is the year five after the beginning of the common era. The census declarations have arrived from the districts. There are seven thousand four hundred and twelve of them. Each one must be checked. You begin.

## Target Audience
- Người xem muốn: content để nghe khi ngủ, không cần chú ý tích cực
- Mood target: flat, monotone, soothing bureaucratic narration

---

## Outline

| # | Section | Duration | Mô tả |
|---|---------|----------|-------|
| 0 | Intro | ~2:30 min | Ngày 1 — Bạn được phân công vào văn phòng census. Cửa sổ. Bụi. Ánh đèn dầu. |
| 1 | Part 1 | ~8 min | Ngày 1-3 — Kiểm tra declarations từ các districts. Tên, tài sản, familiae. |
| 2 | Part 2 | ~8 min | Ngày 4-6 — Cross-reference với census records từ năm ngoái. So sánh, đối chiếu. |
| 3 | Part 3 | ~8 min | Ngày 7-9 — Các discrepancies được tìm thấy. Hướng xử lý. |
| 4 | Outro | ~2:30 min | Ngày 10 — Báo cáo hoàn thành. Được gửi đến governor. |

---

## Script Notes

- **POV:** Second-person (`you`). Narrator dẫn dắt, người nghe là nhân vật trải nghiệm.
- **Tone:** Flat, bureaucratic, dry. Không có excitement.
- **Pacing:** Chậm. Mỗi ngày trong story = 2-3 chunks (~8-12 min audio). Tổng ~30 min.
- **Tránh:** Chiến tranh, bạo lực, dramatic confrontations, cliffhangers
- **Từ đặc trưng / style:**
  - Latin terms giữ nguyên: censitus, tributum, caput, familia, pagus, vicus, actum
  - Dùng passive voice + nominalization
  - Số cụ thể, số lẻ: "seven thousand four hundred and twelve" không "about seven thousand"
  - Second-person POV bắt buộc trong mọi chunk
  - Sensory details: mùi dầu, tiếng bút, texture giấy papyrus

---

## Sources / Research

- **Census records:** Caesar's Gallic census system, Augustus' revised census (4 BC / 5 AD / 14 AD)
- **Tax system:** tributum (direct tax), portorium (customs), scriptura (land tax)
- **Primary sources:** resettled residents records from Egypt (papyrus fragments), census declarations from Pompeii (tabulae)
- **Provincial structure:** Africa Proconsularis, Aegyptus, Galatia — pick one for consistency

---

## Asset Requirements

### Voice (TTS)
- Voice: Charon (onyx equivalent) — xem docs/gemini-voices.md
- Provider: Gemini (`gemini-2.5-flash-preview-tts`)
- API key env: `GEMINI_API_KEY`
- Gen script: `tools/gen_audio.py`
- Speed: 0.95 (slower than default for sleepy tone)
- Ghi chú đặc biệt: Flat delivery, no emphasis on numbers

### Visuals — ý tưởng sơ bộ

- **Intro:** Văn phòng census — bàn dài, papyrus rolls, oil lamp, dust motes
- **Part 1:** Declarations được mở ra — từng tờ papyrus, handwriting, seals
- **Part 2:** Cross-reference — hai bảng cạnh nhau, fingers tracing lines
- **Part 3:** Discrepancies — red ink marks, corrections, marginal notes
- **Outro:** Report được cuộn lại, sealed, prepared for dispatch

### Thumbnail

**Visual anchor cho toàn episode:**
`classical Roman fresco style, muted earth tones, warm amber candlelight, aged papyrus texture`

**Thumbnail prompt (A/B/C test):**
- Prompt 1: Wide shot — văn phòng census, một người clerk ngồi bên bàn dài
- Prompt 2: Close-up — hands đang cầm papyrus, seal visible
- Prompt 3: Mid-shot — người trong không gian với papyrus rolls xung quanh

---

## Episode Timeline Design

### Ngày 1 — Arrival
- Morning: Bạn được assign vào census office
- Afternoon: Nhận bàn giao — 7,412 declarations
- Evening: Sắp xếp workspace

### Ngày 2-3 — Declarations Check
- Mỗi declaration: tên head of household, familia count, property assessed
- Pattern: district by district (pagi)
- Tactile details: papyrus texture, ink smell, seal impressions

### Ngày 4-6 — Cross-Reference
- So sánh với records từ census trước (4 BC)
- Tracking changes: births, deaths, relocations
- Mỗi discrepancy được đánh dấu bằng red ink

### Ngày 7-9 — Discrepancy Investigation
- Các trường hợp không khớp
-实地调查 (on-site investigation) — nhưng ở đây chỉ là paperwork, không đi đâu
- Hướng xử lý: adjusted, confirmed, or referred

### Ngày 10 — Completion
- Final report được viết
- Summary statistics
- Report được sealed và gửi đến governor

---

## YouTube Description

```
Roman Provincial Census and Tax Records, 5 AD

You are a scriba officialis in a Roman provincial capital. The census
declarations have arrived. There are seven thousand four hundred and
twelve of them. Each one must be checked.

This recording covers the administrative process of a Roman provincial
census: declarations received, cross-referencing with prior records,
discrepancy investigation, and final reporting.

#SleepStories #BoringHistory #RomanHistory #AdministrativeHistory
```

---

## Production Checklist

- [ ] `idea.md` hoàn chỉnh
- [ ] `script.md` (index) tạo xong
- [ ] `script/00-intro.md` viết xong
- [ ] `script/01-*.md` viết xong
- [ ] `script/02-*.md` viết xong
- [ ] `script/03-*.md` viết xong
- [ ] `script/04-outro.md` viết xong
- [ ] `script/image-prompts.md` hoàn chỉnh
- [ ] `script/audio-image-map.md` hoàn chỉnh
- [ ] TTS generated → `assets/audio/`
- [ ] Images generated → `assets/images/`
- [ ] Music chọn xong → `assets/music/`
- [ ] Video assembled
- [ ] Thumbnail created → `exports/thumbnail.png`
- [ ] Export final → `exports/final.mp4`
- [ ] Uploaded YouTube

---

## Notes

Episode này tiếp nối tự nhiên sau Ottoman salt inventory — cùng bureaucratic style, khác empire và thời đại. Có thể tham chiếu crossing referencing giữa two census periods như một callback technique.

Target length: ~30 min final video (~20k words script + prompts)