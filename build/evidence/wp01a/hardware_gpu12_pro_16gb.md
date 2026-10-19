# Hardware (derived, bucketed draft)

Draft written by `scripts/windows_check.py --hardware-md` from a pasted PC report. It carries tier words and buckets only: no CPU or GPU model, no driver, no exact size, no account count. The orchestrator reviews it before it is placed in `decisions/hardware.md`.

- Date run: 2026-10-20 (day only)
- GPU tier: gpu-8-12 (vendor family: NVIDIA)
- VRAM bucket (GB): 12-15
- RAM tier (GB): 16+ (WSL2 ok)
- Free disk tier: roomy (judged on the drive with the most free space; thresholds in `win/tiers.json`)
- Vulkan device listed: no (runtime library present: yes)
- Windows: build 22631, edition family pro-or-higher
- Display class: fhd
- Scanner: (the maker fills this in by hand; it is not read from the PC)
- Capture gear on hand: (the maker fills this in by hand)
