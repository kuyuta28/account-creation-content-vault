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
- Voice: [voiceId] — xem docs/gemini-voices.md
- Provider: Gemini (`gemini-2.5-flash-preview-tts`)
- API key env: `GEMINI_API_KEY`
- Gen script: `tools/gen_audio.py`
- Ghi chú đặc biệt:

### Visuals — ý tưởng sơ bộ
<!-- Liệt kê loại ảnh cần theo từng phần — không cần prompt chi tiết ở đây, chi tiết sẽ trong script.md -->
- Intro:
- Part 1:
- Part 2:
- Part 3:

### Thumbnail

**YÊU CẦU BẮT BUỘC về người trong thumbnail:**
Vì story kể ở ngôi thứ 2 (you / second-person POV), thumbnail NHẤT ĐỊNH PHẢI CÓ NGƯỜI đại diện cho "người nghe đang trải nghiệm". Người này chiếm từ **1/3 đến 1/2 khung ảnh** — không quá nhỏ như silhouette, không quá lớn che mất context.

**Chi tiết về người:**
- Vị trí: center frame hoặc slightly off-center (rule of thirds)
- Tư thế: đang thực hiện hành động liên quan đến chủ đề (không đứng yên pose)
- Trang phục: đúng thời đại/lĩnh vực của story
- Không nhìn thẳng vào camera — nhìn vào object hoặc xuống dưới, tạo cảm giác "người xem đang ở trong cảnh"
- Tay và hành động phải rõ ràng — tay đang làm việc gì đó
- Mặt: có thể partially visible, side profile, hoặc out of focus — không cần portrait rõ mặt

**BỐI CẢNH xung quanh người:**
- Chiếm phần còn lại của frame (1/2 đến 2/3)
- Phải communicate ngay chủ đề là gì (văn phòng thời Han, con tàu Titanic, v.v.)
- Có depth layers: foreground (người + object đang tương tác), midground (bối cảnh), background (atmosphere)

**LIGHTING & MOOD:**
- Single dominant light source từ một bên (oil lamp, window light, v.v.)
- Strong chiaroscuro — contrast giữa người và background
- Warm accent color (amber, candlelight) trên người hoặc object chính
- Cool ambient fill cho background

**TEXT TRÊN THUMBNAIL:**
- Prompt 1 & 2: **"HISTORY FOR SLEEP"** — large gold serif #D4A017, centered near bottom
- Prompt 3: **"BORING HISTORY FOR SLEEP"** — large gold serif #D4A017, centered near bottom
- Heavy drop shadow, no other text

---

**Lưu ý — BẮT BUỘC để A/B test hiệu quả:**
- 3 prompt phải khác nhau về **composition** (close-up người làm việc / mid-shot người trong không gian / wide shot người + environment)
- 3 title phải khác nhau về **angle** (archival SEO / number hook / character hook) — KHÔNG chỉ đổi dấu ngăn cách
- Mục tiêu: sau khi upload, có thể swap thumbnail để test CTR — 3 cái giống nhau = không test được gì
- KHÔNG dùng Canva/Photoshop — viết thẳng toàn bộ yêu cầu vào prompt
- **Thumbnail không giới hạn ký tự** — càng chi tiết càng tốt: specify từng vật thể, ánh sáng, màu sắc, texture, depth, atmosphere

---

**⚠️ Thumbnails: TỰ LÀM** — Prompts quá dài (>300 chars), gen qua Midjourney/DALL-E. Folder `assets/thumbnails/` được tạo rỗng sẵn — copy ảnh vào sau khi gen.

---

**Prompt 1** — *[Close-up/Medium shot: người làm việc, tay và object]*
- Title: `[MAIN TITLE, YEAR]` ← archival SEO, dài, đúng keyword
```
Close-up medium shot of weathered hands [thực hiện hành động cụ thể: ví dụ "holding an ink brush over bamboo slips"], the hands occupy lower-center frame, aged skin texture visible, [object chính] in sharp focus, [setting chi tiết] blurred in background, single [light source] casting warm amber light from the left, cool shadows on the right side, photorealistic skin texture, fabric of [trang phục] visible at edge of frame, cinematic chiaroscuro lighting, dramatic shadows, ultra detailed material surfaces, 16:9, one line of bold serif title text centered near the bottom of the frame: large gold letters #D4A017 "HISTORY FOR SLEEP", heavy drop shadow, no other text in image
```

**Prompt 2** — *[Mid-shot: người trong không gian, tư thế rõ ràng]*
- Title: `[NUMBER or DETAIL]: [TOPIC], [YEAR]` ← number-led hook, con số đứng đầu
```
Medium shot from slightly low angle, a [mô tả nhân vật: tuổi, trang phục, đặc điểm] seated/standing at [vị trí cụ thể], body angled three-quarters away from camera, head bowed over [object đang làm việc], [tay đang làm gì] clearly visible in foreground, the figure occupies central 40% of frame, [setting: bàn, văn phòng, thiết bị xung quanh] filling the rest, volumetric light rays from [nguồn sáng], dust particles visible in air, warm [color] tones contrasting with cool grey-blue shadows, photorealistic fabric texture, cinematic depth of field, 16:9, one line of bold serif title text centered near the bottom of the frame: large gold letters #D4A017 "HISTORY FOR SLEEP", heavy drop shadow, no other text in image
```

**Prompt 3** — *[Wide shot: người nhỏ trong environment rộng, atmospheric]*
- Title: `The [ROLE/CHARACTER]: [TOPIC], [YEAR]` ← character hook, nhân vật hóa chủ đề
```
Wide atmospheric interior shot of [setting đầy đủ: ví dụ "Han dynasty county office at dawn"], a lone [mô tả nhân vật] as a clear silhouette in the middle-ground, positioned slightly left or right of center, occupying approximately one-third of frame height, the figure bent over [hành động] at [vị trí], [object xung quanh] creating depth layers — foreground detail, midground figure, background architecture, volumetric morning haze filtering through [nguồn sáng], warm [color] accent light catching the figure's [bộ phận: shoulder, hands] against cool desaturated [color] ambient, painterly realism, cinematic atmosphere, muted palette, 16:9, one line of bold serif title text centered near the bottom of the frame: large gold letters #D4A017 "BORING HISTORY FOR SLEEP", heavy drop shadow, no other text in image
```


---

## YouTube Description

```
[TITLE]

[1–2 câu đặt bối cảnh. Flat, không hype. Không câu hỏi tu từ.]

This recording covers [chủ đề] — [liệt kê ngắn các phần nội dung].

#SleepStories #BoringHistory #[TopicHashtag]
```

<!-- Duration và timestamps sẽ điền sau khi video assembled -->

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
