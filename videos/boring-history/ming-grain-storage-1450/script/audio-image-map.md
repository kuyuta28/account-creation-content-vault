# Audio-Image Map

> **Cách dùng:**
> - Mỗi chunk = 1 audio file = 1 image. Chunk boundary được xác định bởi khi nào image thay đổi.
> - Timestamp điền SAU khi có audio thực — nghe audio, xác định điểm ngắt câu tự nhiên, rồi ghi vào timeline editor.
> - Đừng dùng timestamp placeholder để assemble — sẽ không khớp với lời thoại thực tế.

| # | Audio | Image |
|---|-------|-------|
| 1 | 00-01.mp3 | 00-01 |
| 2 | 00-02.mp3 | 00-02 |
| 3 | 00-03.mp3 | 00-03 |
| 4 | 01-01.mp3 | 01-01 |
| 5 | 01-02.mp3 | 01-02 |
| 6 | 01-03.mp3 | 01-03 |
| 7 | 01-04.mp3 | 01-04 |
| 8 | 01-05.mp3 | 01-05 |
| 9 | 01-06.mp3 | 01-06 |
| 10 | 01-07.mp3 | 01-07 |
| 11 | 01-08.mp3 | 01-08 |
| 12 | 01-09.mp3 | 01-09 |
| 13 | 01-10.mp3 | 01-10 |
| 14 | 01-11.mp3 | 01-11 |
| 15 | 01-12.mp3 | 01-12 |
| 16 | 01-13.mp3 | 01-13 |
| 17 | 01-14.mp3 | 01-14 |
| 18 | 01-15.mp3 | 01-15 |
| 19 | 02-01.mp3 | 02-01 |
| 20 | 02-02.mp3 | 02-02 |
| 21 | 02-03.mp3 | 02-03 |
| 22 | 02-04.mp3 | 02-04 |
| 23 | 02-05.mp3 | 02-05 |
| 24 | 02-06.mp3 | 02-06 |
| 25 | 02-07.mp3 | 02-07 |
| 26 | 02-08.mp3 | 02-08 |
| 27 | 02-09.mp3 | 02-09 |
| 28 | 02-10.mp3 | 02-10 |
| 29 | 02-11.mp3 | 02-11 |
| 30 | 02-12.mp3 | 02-12 |
| 31 | 02-13.mp3 | 02-13 |
| 32 | 02-14.mp3 | 02-14 |
| 33 | 03-01.mp3 | 03-01 |
| 34 | 03-02.mp3 | 03-02 |
| 35 | 03-03.mp3 | 03-03 |
| 36 | 03-04.mp3 | 03-04 |
| 37 | 03-05.mp3 | 03-05 |
| 38 | 03-06.mp3 | 03-06 |
| 39 | 03-07.mp3 | 03-07 |
| 40 | 03-08.mp3 | 03-08 |
| 41 | 03-09.mp3 | 03-09 |
| 42 | 03-10.mp3 | 03-10 |
| 43 | 03-11.mp3 | 03-11 |
| 44 | 03-12.mp3 | 03-12 |
| 45 | 03-13.mp3 | 03-13 |
| 46 | 04-01.mp3 | 04-01 |
| 47 | 04-02.mp3 | 04-02 |

---

<!--
ASSEMBLY INSTRUCTIONS:
  1. Concatenate all 47 audio files in sequence — no gap between chunks
  2. Music: fade in 0:00–0:05 at full level, then drop to -16dB under voiceover
  3. Each image: slow zoom 100%→108% across its full display duration
  4. Transition between images: 0.3s crossfade
  5. End card: music fade out over 60 seconds
  6. Export: 1920×1080, 30fps, H.264, AAC 192kbps → exports/final.mp4
-->
