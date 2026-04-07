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
  1. Concatenate all audio files in sequence — no gap between chunks
  2. Music: fade in 0:00–0:05 at full level, then drop to -16dB under voiceover
  3. Each image: slow zoom 100%→108% across its full display duration
  4. Transition between images: 0.3s crossfade
  5. End card: last audio end → +2:00, music fade out over 60 seconds
  6. Export: 1920×1080, 30fps, H.264, AAC 192kbps → exports/final.mp4
-->
