---
channel: boring-history
status: idea
created: 2026-04-07
updated: 2026-04-07
tags: [ming-dynasty, china, bureaucracy, agriculture, 15th-century]
---

# Ming Dynasty Grain Storage Inspection Logs, 1450

## Angle / Hook
> Triều đình nhà Minh vận hành 230 kho lúa trải dài khắp đế chế — mỗi năm, quan lại địa phương phải nộp báo cáo kiểm tra chi tiết từng kho, từ độ ẩm tường đến số lượng chuột bị bắt

## Target Audience
- Người xem muốn: ngủ với giọng kể chuyện đều đều về lịch sử hành chính châu Á
- Mood target: thư giãn sâu, không cần tập trung, để giọng đọc trôi qua

---

## Outline

| # | Section | Duration | Mô tả |
|---|---------|----------|-------|
| 0 | Intro | ~2 min | Giới thiệu hệ thống kho lúa nhà Minh, năm Cảnh Thái nguyên niên (1450), bối cảnh hành chính |
| 1 | Part 1: Cấu trúc hệ thống kiểm tra | ~8 min | Phân cấp quan lại phụ trách, chu kỳ kiểm tra, biểu mẫu báo cáo chuẩn của Hộ Bộ |
| 2 | Part 2: Quy trình đo đạc và phân loại | ~8 min | Cách đo độ ẩm, phân loại lúa theo 5 mức chất lượng, quy trình cân và ghi chép sai số |
| 3 | Part 3: Biên bản sự cố và xử lý | ~8 min | Các trường hợp hư hỏng, báo cáo mất mát, thủ tục nộp phạt và điều chỉnh sổ sách |
| 4 | Outro | ~2 min | Số liệu tổng kết năm 1450, ghi chú cuối về những bản báo cáo còn lưu đến nay |

---

## Script Notes

- **Tone:** học thuật khô, như đang đọc báo cáo kiểm toán — không có cảm xúc, không nhận xét
- **Pacing:** rất chậm, câu dài nhiều mệnh đề phụ, để người nghe chìm vào số liệu
- **Tránh:** so sánh hiện đại, từ "fascinating/remarkable/surprising", không nói "hãy tưởng tượng"
- **Từ đặc trưng / style:** giữ nguyên tên quan chức Hán-Việt (Hộ Bộ, Tri huyện, Thương ty), số liệu bằng đơn vị gốc (thạch, thăng, cân)

---

## Sources / Research

- https://en.wikipedia.org/wiki/Ming_dynasty
- https://en.wikipedia.org/wiki/Ever-Normal_Granary
- Hucker, Charles O. — *A Dictionary of Official Titles in Imperial China* (1985)
- Ray Huang — *1587, A Year of No Significance* (tham khảo phong cách hành chính)
- https://en.wikipedia.org/wiki/Granary

---

## Asset Requirements

### Voice (TTS)
- Voice: Graham (Inworld AI — Profound, authoritative British male)
- Provider: Inworld AI (`inworld-tts-1.5-max`)
- Speed: 0.85
- Temperature: 0.9
- API key env: `INWORLD_API_KEY`
- Gen script: `tools/gen_audio.py`
- Ghi chú đặc biệt: không inflection, đọc số liệu và tên chức quan như đọc danh sách

### Music nền
- Mood: ambient drone, tối giản, không melody nhận ra được
- BPM range: 55–65
- Ghi chú: nếu có thể, dùng texture có hơi hướng nhạc cụ truyền thống (đàn tranh, erhu) nhưng cực kỳ mờ và chậm

### Visuals — ý tưởng sơ bộ
- Intro: bản đồ Trung Quốc thời nhà Minh, palace complex nhìn từ trên cao
- Part 1: quan lại trong trang phục triều đình đang ghi chép, scroll/sổ sách, kiến trúc kho lúa phía ngoài
- Part 2: cảnh bên trong kho — lúa đổ đống, cân gỗ, quan lại đo đạc bằng dụng cụ
- Part 3: tài liệu viết tay, dấu triện đỏ, cảnh kho bị ẩm/hư hại

### Thumbnail
- Subject (central image): Cổng kho lúa nhà Minh, kiến trúc truyền thống, sương mù nhẹ buổi sáng
- Text overlay (title ngắn, ≤6 từ): "Ming Grain Storage Logs"
- Mood / color palette: deep charcoal, muted terracotta, fog grey

**Prompt:**
```
Ancient Chinese Ming dynasty granary exterior, traditional wooden architecture with curved roof tiles, early morning mist, deep charcoal background, dramatic low diffused light, centered composition, classical Chinese painting style with ink wash influence, cinematic atmosphere, muted terracotta and grey tones, 16:9
```

<!-- Sau khi gen ảnh: thêm text overlay trong Canva/Photoshop -->
<!-- Font: Playfair Display, màu #E8E0D0, bottom-center, padding 5% -->

---

## Production Checklist

- [ ] `idea.md` hoàn chỉnh
- [ ] `script.md` viết xong (narration + image prompts)
- [ ] TTS generated → `assets/audio/`
- [ ] Images generated → `assets/images/`
- [ ] Music chọn xong → `assets/music/`
- [ ] Video assembled
- [ ] Thumbnail created → `exports/thumbnail.png`
- [ ] Export final → `exports/final.mp4`
- [ ] Uploaded YouTube

---

## Notes

- Tên chức quan cần tra kỹ trước khi viết script: Hộ Bộ (Ministry of Revenue), Thương ty (Granary Office), Tri huyện (County Magistrate)
- Đơn vị đo lường nhà Minh: 1 thạch ≈ 107 lít, 1 thăng = 1/10 thạch — dùng đơn vị gốc, không chuyển đổi
- Có thể tham khảo thêm hệ thống Ever-Normal Granary (Thường bình thương) để hiểu bối cảnh
