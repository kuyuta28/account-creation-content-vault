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


**Lưu ý — BẮT BUỘC để A/B test hiệu quả:**
- 3 prompt phải khác nhau về **composition** (close-up nhân vật / macro object / wide shot)
- 3 title phải khác nhau về **angle** (archival SEO / number hook / character hook) — KHÔNG chỉ đổi dấu ngăn cách
- 3 text overlay trên ảnh phải khác nhau (test copy song song với visual)
- Mục tiêu: sau khi upload, có thể swap thumbnail để test CTR — 3 cái giống nhau = không test được gì
- KHÔNG dùng Canva/Photoshop — viết thẳng toàn bộ yêu cầu vào prompt

**Prompt 1** — *[mô tả hook: ví dụ: nhân vật / cảm xúc]*
- Title: `[MAIN TITLE, YEAR]` ← archival SEO, dài, đúng keyword
- Text overlay: "[LINE 1] / [LINE 2]" (center, 2 dòng, chữ to)
```
[SUBJECT], photorealistic, cinematic lighting, ultra detailed, dramatic chiaroscuro, 16:9, two lines of bold serif title text centered in frame: large gold letters #D4A017 "[LINE 1]" on the first line and "[LINE 2]" on the second line, both with heavy drop shadow
```
**Prompt 2** — *[mô tả hook: ví dụ: data / number / curiosity]*
- Title: `[NUMBER or DETAIL]: [TOPIC], [YEAR]` ← number-led hook, con số đứng đầu
- Text overlay: "[LINE 1] / [LINE 2]" (center, 2 dòng, chữ to)
```
[SUBJECT] viewed from overhead or low angle, [SETTING], dramatic raking light, deep shadows, muted [COLOR] tones, photorealistic, cinematic, ultra detailed, 16:9, two lines of bold serif title text centered in frame: large gold letters #D4A017 "[LINE 1]" on the first line and "[LINE 2]" on the second line, both with heavy drop shadow
```
**Prompt 3** — *[mô tả hook: ví dụ: quy mô / character / atmosphere]*
- Title: `The [ROLE/CHARACTER]: [TOPIC], [YEAR]` ← character hook, nhân vật hóa chủ đề
- Text overlay: "[LINE 1] / [LINE 2]" (center, 2 dòng, chữ to)
```
Wide atmospheric shot of [SETTING], [SUBJECT] as a small silhouette in the foreground, volumetric haze, [LIGHTING] casting long shadows, painterly realism, muted desaturated palette with warm [COLOR] accent, 16:9, two lines of bold serif title text centered in frame: large gold letters #D4A017 "[LINE 1]" on the first line and "[LINE 2]" on the second line, both with heavy drop shadow
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

#SleepStories #BoringHistory #[TopicHashtag]
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
