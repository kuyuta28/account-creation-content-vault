# Gemini TTS — Voice Reference

**Platform:** https://aistudio.google.com  
**API endpoint:** `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent`  
**Pricing:** Free (gemini-2.5-flash-preview-tts, Standard tier)  
**Audio output:** WAV (PCM L16, 24kHz mono)

---

## Cách dùng

```bash
# CLI
python tools/gen_audio.py --project . --voice Charon

# Với API key explicit
python tools/gen_audio.py --project . --voice Fenrir --key AIza...
```

---

## Danh sách voices

| Voice | Đặc điểm gợi ý |
|-------|----------------|
| **Zephyr** | Nhẹ nhàng, hiện đại |
| **Puck** | Vui vẻ, trẻ trung |
| **Charon** | Trầm, quyền lực — tốt cho narration lịch sử |
| **Kore** | Nữ, rõ ràng |
| **Fenrir** | Nam trẻ, năng động |
| **Leda** | Nữ, mềm mại |
| **Orus** | Trầm ấm |
| **Aoede** | Nữ, nhẹ nhàng |
| Callirrhoe | — |
| Autonoe | — |
| Enceladus | — |
| Iapetus | — |
| Umbriel | — |
| Algieba | — |
| Despina | — |
| Erinome | — |
| Algenib | — |
| Rasalgethi | — |
| Laomedeia | — |
| Achernar | — |
| Alnilam | — |
| Schedar | — |
| Gacrux | — |
| Pulcherrima | — |
| Achird | — |
| Zubenelgenubi | — |
| Vindemiatrix | — |
| Sadachbia | — |
| Sadaltager | — |
| Sulafat | — |

---

## Config mặc định

Chỉnh trong `config/tts.yaml`:

```yaml
gemini:
  api_keys:
    - "AIza..."          # Gemini API key
  model: gemini-2.5-flash-preview-tts
  default_voice: Charon
```

Hoặc set env:

```bash
export GEMINI_API_KEY=AIza...
```

---

## Ghi chú

- Không support `speaking_rate` trực tiếp qua prebuilt voice config — phụ thuộc vào model
- Output là `.wav` (PCM 24kHz) — ffmpeg có thể đọc trực tiếp khi ghép video
- `gemini-2.5-flash-preview-tts` miễn phí (Standard tier, tính đến 2025)
