# Audio-Image Map

> **Nguyên tắc:** 1 chunk = 1 audio file = 1 image. Timestamp điền SAU khi có audio thực.
> Không điền timestamp placeholder — sẽ không khớp lời thoại thực tế.

| # | Audio | Image |
|---|-------|-------|
| 1 | 00-01.mp3 | 00-01 |
| 2 | 00-02.mp3 | 00-02 |
| 3 | 00-03.mp3 | 00-03 |
| … | … | … |
| — | 04-01.mp3 | 04-01 |
| — | 04-02.mp3 | 04-02 |

<!--
ASSEMBLY INSTRUCTIONS:
  1. Gen clips: `python tools/gen_clips.py`
     → Merge mỗi image+audio pair → assets/clips/XX-XX.mp4 (duration = audio length)
  2. Import toàn bộ clips vào CapCut, stack theo thứ tự
  3. Effects: vignette + Ken Burns slow zoom (100%→108%) per clip
  4. Transition between clips: 0.3s crossfade
  5. Export: 1920×1080, 30fps, H.264, AAC 192kbps → exports/final.mp4
  Note: không thêm nhạc nền — voice-only là chuẩn cho sleep history format
-->
