Fixtures for research/gujarati-devotional-sound.md (track gujarati-devotional-sound).
Run 2026-10-19 in the cloud container. Public sources and public-domain or CC0 audio only; nothing here is about her, her family or any real person beyond the named public musicians a page lists.
It is research, not production code: the numbers came from short throw-away scripts kept in the session scratchpad (the sprint rule is "no code"); the method is described in the footer of the CSV so a build sprint can rebuild them.

Files
  phone_speaker_haveli_instruments_2026-10-19.csv   per-instrument PASS or FAIL against a crude phone-speaker high-pass at 300 Hz and 500 Hz (rule in the CSV footer). 26 rows: pakhawaj, the whole haveli ensemble, tanpura, jhanj (stand-in), manjira, bell, conch, a puja field recording, the hum (closed-mouth, and models of lower voices), an open-vowel hum, three seas, two swings and a pressure cooker (the sibling's number).
  saregama_navratri_garba_songs_2022_credits_as_read_*.csv   the composer credits printed on one label compilation of 12 garba tracks, with the status each implies. Credits are a platform's metadata, not a registry extract.
  archive_org_and_open_sources_rights_evidence_*.csv   what each open-looking source actually says about its licence, who set it, and the verdict.

Environment
  ffmpeg 6.1.1 (Ubuntu 24.04); Python 3.13 with numpy; archive.org metadata API (read-only) for the item records; Freesound pages and preview MP3s fetched with curl under a browser user agent; Wikimedia Commons file page read with the fetch tool.
  NOT run: any phone. The Android phone tone ladder (research/mobile-delivery.md protocol row 10) is the maker's step and replaces the 300 and 500 Hz corners.

How to redo the phone check on the maker's own captures (PowerShell or any shell with ffmpeg)
  1. Record the object (bell, jhanj, hum) mono, 48 kHz, 24-bit, in the empty room.
  2. ffmpeg -i take.wav -af "highpass=f=500:poles=2" take_hp500.wav   and the same with f=300.
  3. Compare RMS: ffmpeg -i take.wav -af astats=metadata=1:reset=0 -f null -   (read 'RMS level dB' overall) and the same on the filtered file. PASS when the loss is 6.0 dB or less at both corners; then play both takes on the project phone at 50% volume in a quiet room, and trust the ear over the model.
