# Audio-Image Map — Han Dynasty Household Registry Correction, 2 AD

<!-- Fill timestamps AFTER real audio exists -->
<!-- Assembly: gen_clips.py merge image+audio → assets/clips/clip-0N-XX.mp4 -->
<!-- CapCut import → vignette + Ken Burns slow zoom 100%→108% → 0.3s crossfade → export -->

| Chunk | Audio File | Image | Duration est. |
|-------|-----------|-------|----------------|
| audio-00-01 | assets/audio/audio-00-01.wav | IMG-00-01 | ~4 min |
| audio-00-02 | assets/audio/audio-00-02.wav | IMG-00-02 | ~4 min |
| audio-00-03 | assets/audio/audio-00-03.wav | IMG-00-03 | ~4 min |
| audio-01-01 | assets/audio/audio-01-01.wav | IMG-01-01 | ~4 min |
| audio-01-02 | assets/audio/audio-01-02.wav | IMG-01-02 | ~4 min |
| audio-01-03 | assets/audio/audio-01-03.wav | IMG-01-03 | ~4 min |
| audio-01-04 | assets/audio/audio-01-04.wav | IMG-01-04 | ~4 min |
| audio-01-05 | assets/audio/audio-01-05.wav | IMG-01-05 | ~4 min |
| audio-01-06 | assets/audio/audio-01-06.wav | IMG-01-06 | ~4 min |
| audio-01-07 | assets/audio/audio-01-07.wav | IMG-01-07 | ~4 min |
| audio-01-08 | assets/audio/audio-01-08.wav | IMG-01-08 | ~4 min |
| audio-01-09 | assets/audio/audio-01-09.wav | IMG-01-09 | ~4 min |
| audio-01-10 | assets/audio/audio-01-10.wav | IMG-01-10 | ~4 min |
| audio-02-01 | assets/audio/audio-02-01.wav | IMG-02-01 | ~4 min |
| audio-02-02 | assets/audio/audio-02-02.wav | IMG-02-02 | ~4 min |
| audio-02-03 | assets/audio/audio-02-03.wav | IMG-02-03 | ~4 min |
| audio-02-04 | assets/audio/audio-02-04.wav | IMG-02-04 | ~4 min |
| audio-02-05 | assets/audio/audio-02-05.wav | IMG-02-05 | ~4 min |
| audio-02-06 | assets/audio/audio-02-06.wav | IMG-02-06 | ~4 min |
| audio-02-07 | assets/audio/audio-02-07.wav | IMG-02-07 | ~4 min |
| audio-02-08 | assets/audio/audio-02-08.wav | IMG-02-08 | ~4 min |
| audio-02-09 | assets/audio/audio-02-09.wav | IMG-02-09 | ~4 min |
| audio-03-01 | assets/audio/audio-03-01.wav | IMG-03-01 | ~4 min |
| audio-03-02 | assets/audio/audio-03-02.wav | IMG-03-02 | ~4 min |
| audio-03-03 | assets/audio/audio-03-03.wav | IMG-03-03 | ~4 min |
| audio-03-04 | assets/audio/audio-03-04.wav | IMG-03-04 | ~4 min |
| audio-03-05 | assets/audio/audio-03-05.wav | IMG-03-05 | ~4 min |
| audio-03-06 | assets/audio/audio-03-06.wav | IMG-03-06 | ~4 min |
| audio-03-07 | assets/audio/audio-03-07.wav | IMG-03-07 | ~4 min |
| audio-03-08 | assets/audio/audio-03-08.wav | IMG-03-08 | ~4 min |
| audio-03-09 | assets/audio/audio-03-09.wav | IMG-03-09 | ~4 min |
| audio-04-01 | assets/audio/audio-04-01.wav | IMG-04-01 | ~4 min |
| audio-04-02 | assets/audio/audio-04-02.wav | IMG-04-02 | ~4 min |
| audio-04-03 | assets/audio/audio-04-03.wav | IMG-04-03 | ~4 min |
| audio-04-04 | assets/audio/audio-04-04.wav | IMG-04-04 | ~4 min |
| audio-04-05 | assets/audio/audio-04-05.wav | IMG-04-05 | ~4 min |
| audio-04-06 | assets/audio/audio-04-06.wav | IMG-04-06 | ~4 min |
| audio-04-07 | assets/audio/audio-04-07.wav | IMG-04-07 | ~4 min |
| audio-05-01 | assets/audio/audio-05-01.wav | IMG-05-01 | ~4 min |
| audio-05-02 | assets/audio/audio-05-02.wav | IMG-05-02 | ~4 min |
| audio-05-03 | assets/audio/audio-05-03.wav | IMG-05-03 | ~4 min |
| audio-05-04 | assets/audio/audio-05-04.wav | IMG-05-04 | ~4 min |
| audio-05-05 | assets/audio/audio-05-05.wav | IMG-05-05 | ~4 min |
| audio-06-01 | assets/audio/audio-06-01.wav | IMG-06-01 | ~4 min |
| audio-06-02 | assets/audio/audio-06-02.wav | IMG-06-02 | ~4 min |
| audio-06-03 | assets/audio/audio-06-03.wav | IMG-06-03 | ~4 min |
| audio-06-04 | assets/audio/audio-06-04.wav | IMG-06-04 | ~4 min |
| audio-07-01 | assets/audio/audio-07-01.wav | IMG-07-01 | ~4 min |
| audio-07-02 | assets/audio/audio-07-02.wav | IMG-07-02 | ~4 min |
| audio-07-03 | assets/audio/audio-07-03.wav | IMG-07-03 | ~4 min |

**Total: 50 chunks, ~200 min, 50 images**

## Assembly Instructions

1. Generate audio: `tools/gen_audio.py` using `config/tts.yaml` per episode
2. Generate images: 50 images from `image-prompts.md` using image gen tool
3. Generate clips: `gen_clips.py` merges audio + image → `assets/clips/clip-0N-XX.mp4`
4. CapCut import:
   - Vignette overlay on all clips
   - Ken Burns slow zoom: 100% → 108% over each chunk duration
   - 0.3s crossfade between consecutive clips
5. Export: 1920×1080, 30fps, H.264, AAC 192kbps
6. Thumbnail: 3 variants from `idea.md` thumbnail section
7. Upload with description from `idea.md` YouTube Description section