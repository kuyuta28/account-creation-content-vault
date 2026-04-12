# content-vault

Kho nội dung cho các YouTube channel dạng AI-generated (voiceover + AI image).

## Cấu trúc

```
docs/
  templates/              # Template để copy khi tạo episode mới
    idea.md
    script.md
    assets/
    exports/
  workflow.md             # Hướng dẫn đầy đủ production pipeline

videos/
  {channel}/
    {topic-slug}/         # Đặt tên theo chủ đề, ví dụ: roman-senate-debates
      idea.md
      script.md
      assets/
      exports/
```

## Channels

| ID | Tên | Niche | Giọng | Độ dài |
|----|-----|-------|-------|--------|
| `boring-history` | Boring History for Sleep | history | onyx | ~30 min |

## Workflow nhanh

`idea.md` → `script.md` → TTS → Image gen → Assemble → Export → Upload

Chi tiết từng bước: xem [docs/workflow.md](docs/workflow.md)

## Full Flow

**"Full flow" = chạy toàn bộ pipeline từ TTS đến clips sẵn sàng assemble.** Khi bảo "chạy full flow" tức là:

```bash
cd content-vault/episodes/boring-history/{episode-slug}

# 1. Gen TTS audio VÀ images CHẠY SONG SONG (2 cái độc lập, không liên quan nhau)
python tools/gen_audio.py --project . &
python tools/gen_images.py --project . &
wait

# 2. Gen video clips (audio + image → mp4) — CHỈ chạy sau khi cả TTS và images xong
python tools/gen_clips.py --project .
```

**Điều kiện trước:**
- Script đã viết xong (tất cả files trong `script/`)
- Config `tts.yaml` đã tạo trong `config/` của episode
- tts-proxy đang chạy (port 8700)
- registrar đang chạy (port 8709) — cần cho gen_images
- ffmpeg đã cài — cần cho gen_clips
- AA accounts có đủ balance cho số ảnh cần gen

**Tại sao TTS và images chạy song song:** TTS chỉ cần tts-proxy (port 8700), images chỉ cần registrar + aa-proxy (port 8709). Hai cái hoàn toàn độc lập, chạy tuần tự chỉ lãng phí thời gian.

**Sau full flow:** clips sẵn sàng trong `assets/clips/`, import vào CapCut để assemble + export
