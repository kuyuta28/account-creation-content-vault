# Audio-Image Map

> **Nguyên tắc:** 1 chunk = 1 audio file = 1 image. Timestamp điền SAU khi có audio thực.
> Không điền timestamp placeholder — sẽ không khớp lời thoại thực tế.

| # | Audio | Image |
|---|-------|-------|
| 1 | audio-00-01.wav | IMG-00-01 |
| 2 | audio-00-02.wav | IMG-00-02 |
| 3 | audio-01-01.wav | IMG-01-01 |
| 4 | audio-01-02.wav | IMG-01-02 |
| 5 | audio-01-03.wav | IMG-01-03 |
| 6 | audio-01-04.wav | IMG-01-04 |
| 7 | audio-01-05.wav | IMG-01-05 |
| 8 | audio-01-06.wav | IMG-01-06 |
| 9 | audio-01-07.wav | IMG-01-07 |
| 10 | audio-01-08.wav | IMG-01-08 |
| 11 | audio-01-09.wav | IMG-01-09 |
| 12 | audio-02-01.wav | IMG-02-01 |
| 13 | audio-02-02.wav | IMG-02-02 |
| 14 | audio-02-03.wav | IMG-02-03 |
| 15 | audio-02-04.wav | IMG-02-04 |
| 16 | audio-02-05.wav | IMG-02-05 |
| 17 | audio-02-06.wav | IMG-02-06 |
| 18 | audio-02-07.wav | IMG-02-07 |
| 19 | audio-02-08.wav | IMG-02-08 |
| 20 | audio-02-09.wav | IMG-02-09 |
| 21 | audio-03-01.wav | IMG-03-01 |
| 22 | audio-03-02.wav | IMG-03-02 |
| 23 | audio-03-03.wav | IMG-03-03 |
| 24 | audio-03-04.wav | IMG-03-04 |
| 25 | audio-03-05.wav | IMG-03-05 |
| 26 | audio-03-06.wav | IMG-03-06 |
| 27 | audio-03-07.wav | IMG-03-07 |
| 28 | audio-03-08.wav | IMG-03-08 |
| 29 | audio-04-01.wav | IMG-04-01 |
| 30 | audio-04-02.wav | IMG-04-02 |

<!--
ASSEMBLY INSTRUCTIONS:
  1. Gen audio: `python tools/gen_audio.py --project . --voice Charon`
  2. Gen images: `python tools/gen_images.py --project .`
  3. Gen clips: `python tools/gen_clips.py`
     → Merge mỗi image+audio pair → assets/clips/clip-XX-XX.mp4 (duration = audio length)
  4. Import toàn bộ clips vào CapCut, stack theo thứ tự
  5. Effects: vignette + Ken Burns slow zoom (100%→108%) per clip
  6. Transition between clips: 0.3s crossfade
  7. Export: 1920×1080, 30fps, H.264, AAC 192kbps → exports/final.mp4
  Note: không thêm nhạc nền — voice-only là chuẩn cho sleep history format
-->