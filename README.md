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
