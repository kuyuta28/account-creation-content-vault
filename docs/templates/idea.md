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
- Text overlay (title ngắn, ≤6 từ):
- Mood / color palette:

**Prompt:**
```
[SUBJECT_PROMPT], deep navy background, dramatic low light, centered composition, photorealistic oil painting style, cinematic atmosphere, muted earth tones, no people faces, no text in image, 16:9 --ar 16:9 --no watermark
```

<!-- Sau khi gen ảnh: thêm text overlay trong Canva/Photoshop -->
<!-- Font gợi ý: serif (Georgia, Playfair Display), màu trắng nhạt hoặc gold, opacity 90% -->
<!-- Text đặt ở: bottom-left hoặc center, không che subject chính -->

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
