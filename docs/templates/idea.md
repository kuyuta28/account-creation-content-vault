---
channel: CHANNEL_ID              # channel id — xem README.md
status: idea                     # idea | scripting | recorded | editing | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
---

# [WORKING TITLE]

## Angle / Hook
> Một câu: tại sao video này đáng bật lên rồi ngủ quên

## Target Audience
- Người xem muốn:
- Mood target:

---

## Outline

> Điền ngắn gọn — mỗi phần chỉ cần tên + thời lượng + 1 câu mô tả
> Script chi tiết sẽ viết trong script.md

| # | Section | Duration | Mô tả |
|---|---------|----------|-------|
| 0 | Intro | ~2 min | |
| 1 | Part 1: [tên] | ~8 min | |
| 2 | Part 2: [tên] | ~8 min | |
| 3 | Part 3: [tên] | ~8 min | |
| 4 | Outro | ~2 min | |

---

## Script Notes

- **POV:** Second-person (`you`). Narrator dẫn dắt, người nghe là nhân vật trải nghiệm.
- **Tone:**
- **Pacing:**
- **Tránh:**
- **Từ đặc trưng / style:**

---

## Sources / Research

- 
- 

---

## Asset Requirements

### Voice (TTS)
- Voice: [voiceId] — xem docs/inworld-voices.md
- Provider: Inworld AI (`inworld-tts-1.5-max`)
- Speed: [0.5–1.5]
- Temperature: [0.7–1.2]
- API key env: `INWORLD_API_KEY`
- Gen script: `tools/gen_audio.py`
- Ghi chú đặc biệt:

### Visuals — ý tưởng sơ bộ
<!-- Liệt kê loại ảnh cần theo từng phần — không cần prompt chi tiết ở đây, chi tiết sẽ trong script.md -->
- Intro:
- Part 1:
- Part 2:
- Part 3:

### Thumbnail
- Subject (central image):
- Text overlay: [TOP TEXT] (top, bold, gold) + [BOTTOM TEXT] (bottom, smaller, gold)
- Mood / color palette:


**Lưu ý:** Luôn tạo 3 prompt thumbnail khác nhau để chọn. Viết thẳng toàn bộ yêu cầu vào từng prompt — KHÔNG dùng Canva/Photoshop.

**Prompt 1:**
```
[SUBJECT], photorealistic, cinematic lighting, ultra detailed, dramatic chiaroscuro, 16:9, bold serif title text "[TOP TEXT]" at the top center in large gold letters #D4A017 with drop shadow, smaller serif text "[BOTTOM TEXT]" at the bottom center in gold #D4A017
```
**Prompt 2:**
```
[SUBJECT] viewed from a low angle looking up, [SETTING], dramatic top-down raking light, deep shadows, muted [COLOR] tones, photorealistic, cinematic, ultra detailed, 16:9, bold serif title text "[TOP TEXT]" at the top center in large gold letters #D4A017 with drop shadow, smaller serif text "[BOTTOM TEXT]" at the bottom center in gold #D4A017
```
**Prompt 3:**
```
Wide atmospheric shot of [SETTING], [SUBJECT] as a small silhouette in the foreground, volumetric haze, [LIGHTING] casting long shadows, painterly realism, muted desaturated palette with warm [COLOR] accent, 16:9, bold serif title text "[TOP TEXT]" at the top center in large gold letters #D4A017 with drop shadow, smaller serif text "[BOTTOM TEXT]" at the bottom center in gold #D4A017
```


---

## YouTube Description

```
[TITLE]

[1–2 câu đặt bối cảnh. Flat, không hype. Không câu hỏi tu từ.]

This recording covers [chủ đề] — [liệt kê ngắn các phần nội dung].

Duration: approximately X hours Y minutes. Narrated at a slow pace. No background music.

---

00:00 Intro
XX:XX Part 1 — [title]
XX:XX Part 2 — [title]
XX:XX Part 3 — [title]
XX:XX Outro
```

<!-- Điền timestamp thực sau khi video assembled -->

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
- [ ] TTS generated → `assets/audio/` (file đặt tên `audio-{section}-{chunk}.mp3`)
- [ ] Images generated → `assets/images/`
- [ ] Music chọn xong → `assets/music/`
- [ ] Video assembled
- [ ] Thumbnail created → `exports/thumbnail.png`
- [ ] Export final → `exports/final.mp4`
- [ ] Uploaded YouTube

---

## Notes

<!-- Ghi chú thêm, ý tưởng phát sinh, vấn đề gặp phải -->
