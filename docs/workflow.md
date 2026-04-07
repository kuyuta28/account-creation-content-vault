# Production Workflow

## Tổng flow

```
[1] IDEA       idea.md      Angle, hook, outline, sources, asset requirements
     ↓
[2] SCRIPT     script.md    Narration đầy đủ + image prompts + timing map
     ↓
[3] TTS                     Generate audio từ script
     ↓
[4] IMAGE GEN               Generate ảnh theo prompts trong script.md
     ↓
[5] ASSEMBLE                Ghép video: audio + ảnh + music nền
     ↓
[6] EXPORT                  Render final → exports/
     ↓
[7] UPLOAD                  Upload YouTube + metadata
```

---

## Bước 1 — IDEA (`idea.md`)

Làm trước khi viết bất cứ thứ gì. Mục tiêu: khóa chặt **góc tiếp cận** và **cấu trúc** để script không bị lạc.

Cần có:
- **Angle / hook** — 1 câu tại sao video này đáng bật (hay đáng ngủ quên)
- **Outline** — bảng các section: tên, thời lượng, mô tả 1 câu
- **Script notes** — tone, pacing, từ cần tránh
- **Sources** — link / tài liệu để viết script
- **Voice & music** — giọng TTS, speed, mood nhạc

Status flow: `idea` → `scripting` → `recorded` → `editing` → `done`

Tạo episode mới:
```
cp -r docs/templates videos/{channel}/{topic-slug}
```

Folder structure sau khi tạo:
```
videos/{channel}/{topic-slug}/
  idea.md
  script.md          ← index file (links to script/ files)
  script/
    00-intro.md
    01-section.md    ← đổi tên theo nội dung thực
    02-section.md
    03-section.md
    04-outro.md
    image-prompts.md
    audio-image-map.md
  assets/
    audio/
    images/
    music/
  exports/
```

---

## Bước 2 — SCRIPT (`script/`)

Script tách thành nhiều file — mỗi section 1 file. `script.md` là index.

**Files:**

| File | Nội dung |
|------|----------|
| `script.md` | Index — frontmatter + bảng links đến từng section file |
| `script/00-intro.md` | Narration intro + image prompts |
| `script/01-section.md` | Narration section 1 + image prompts |
| `script/02-section.md` | Narration section 2 + image prompts |
| `script/03-section.md` | Narration section 3 + image prompts |
| `script/04-outro.md` | Narration outro + image prompts |
| `script/image-prompts.md` | Master list tất cả prompts để gen hàng loạt |
| `script/audio-image-map.md` | Bảng timing 31 dòng + assembly instructions |

**Cấu trúc mỗi section file:**
```markdown
### CHUNK audio-0N-01 (~500 words)
<!-- img: IMG-0N-01, IMG-0N-02 -->

[Nội dung nói — văn xuôi đầy đủ, tối đa 500 từ]

---image-prompts---
IMG-0N-01: [style], [subject], [setting], [lighting/mood].
IMG-0N-02: [style], [subject], [setting], [lighting/mood].
---end-prompts---
```

**Quy tắc chunk:**
- Tối đa ~500 từ/chunk → ~3:56 audio (onyx @ 0.85 = ~127 wpm)
- Intro/outro chunk: ~320 từ → ~2:30
- Chunk cuối mỗi section: ~445 từ (transition nhẹ sang section tiếp)
- KHÔNG đọc `<!-- comment -->` vào TTS

**Quy tắc image prompt:**
- Bắt đầu bằng style rõ: `Classical Chinese ink wash painting,` / `19th century engraving,`
- Subject + action + setting + lighting/mood — 1 câu hoặc 2 câu ngắn
- Không bullet, không text trong ảnh

**Số ảnh:** ~1 ảnh/90 giây → chunk 500 từ (~3:56) ≈ 2–3 ảnh

---

## Bước 3 — TTS

| Việc | Chi tiết |
|------|---------|
| Tool | OpenAI TTS |
| Copy source | Narration text từng chunk trong `script/0N-section.md` (bỏ `<!-- -->`, image prompts) |
| Đặt tên file | `audio-{section}-{chunk}.mp3` — ví dụ `audio-01-03.mp3` |
| Lưu vào | `assets/audio/` |
| Settings mặc định | voice: onyx, speed: 0.85 (override theo `idea.md`) |
| Rate thực tế | ~127 wpm → ~500 từ ≈ 3:56 | ~320 từ ≈ 2:30 |

---

## Bước 4 — Image Gen

| Việc | Chi tiết |
|------|---------|
| Lấy prompts | Copy block **Image Prompts tổng hợp** ở cuối `script.md` |
| Đặt tên file | `IMG-{section}-{number}.png` — ví dụ `IMG-02-01.png` |
| Lưu vào | `assets/images/` |
| Ratio | 16:9 (1920×1080 hoặc 1280×720) |
| Tool gợi ý | Midjourney / Flux / DALL-E |

---

## Bước 5 — Assemble

Timing cụ thể xem `script/audio-image-map.md` của từng episode.

Quy tắc chung:

```
0:00–0:05       — Intro music fade in (không voiceover)
0:05–~5:05      — Section 0: Intro  (~2 chunks × ~2:30)
~5:05–...       — Section 1–3: mỗi section ~N chunks × ~3:56
...–end         — Section 4: Outro  (~2 chunks × ~2:30)
end–end+2:00    — End card (music fade out over 60s)
```

Transition ảnh: 0.3s crossfade — không dùng hiệu ứng fancy.
Motion: slow zoom-in 100%→108% trong suốt duration của mỗi ảnh.

---

## Bước 6 — Export

```
Resolution : 1920×1080
FPS        : 30
Video codec: H.264 (High profile)
Audio codec: AAC 192kbps
Container  : MP4
Tên file   : exports/final.mp4
Thumbnail  : exports/thumbnail.png (1280×720)
```

---

## Bước 7 — Upload

- Title: [topic] — không clickbait, không caps lock
- Description: 2–3 câu giới thiệu + timestamps sections
- Tags: lấy từ `tags` trong `idea.md`
- Thumbnail: gen riêng theo prompt trong `idea.md` → thêm text overlay → `exports/thumbnail.png`
- Sau upload: update status trong `idea.md` → `done`

---

## Thumbnail — Hướng dẫn gen

**Nguyên tắc cho sleep/relaxation niche:**
- Màu tối, trầm — deep navy, dark brown, muted green. Không dùng màu sáng chói
- Subject rõ, centered — 1 vật/cảnh chính, không rối
- Không có mặt người (hoặc mặt người mờ/nhoè) — tránh uncanny valley
- Text overlay tối giản — ≤6 từ, font serif, màu trắng nhạt / vàng gold
- Signal "đây là để ngủ" ngay từ cái nhìn đầu tiên

**Cấu trúc prompt:**
```
{SUBJECT}, {SETTING}, deep [navy/charcoal/forest] background, dramatic low candlelight, 
centered composition, {STYLE}, cinematic atmosphere, muted earth tones, 
no text, no watermark, 16:9
```

**Style options theo niche:**
| Niche | Style gợi ý |
|-------|-------------|
| boring-history | `classical oil painting style` / `19th century engraving, detailed` |

**Ví dụ hoàn chỉnh (boring-history):**
```
Ancient Roman senate chamber interior, marble columns and wooden benches, 
deep navy background, dramatic low candlelight from wall torches, 
centered composition, classical oil painting style, cinematic atmosphere, 
muted earth tones, no text, no watermark, 16:9
```

**Text overlay (làm trong Canva / Photoshop sau khi gen ảnh):**
- Font: Playfair Display hoặc Georgia (serif)
- Màu: `#E8E0D0` (trắng kem) hoặc `#C9A84C` (gold)
- Size: đủ đọc ở thumbnail nhỏ (300px)
- Vị trí: bottom-center hoặc bottom-left, padding 5%
- Không shadow đậm — dùng subtle drop shadow hoặc text outline nhẹ
