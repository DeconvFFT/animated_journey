# Synthetic PC report fixtures (WP-01a)

Every file here is **invented**. No real computer, person, account, address or machine was read to make them. They are produced by `tests/win/make_fixtures.py` (run it with `--check` to see that the files match the generator).

The planted "identifying" values in `report_identifying.json` are written with JSON `\u` escapes for the punctuation (at-sign, dots, colons, backslashes), so the raw file does not contain the strings it tests for. The checkers see them after the file is parsed. Two files cannot hide their trigger that way (`report_hex65_leak.json` has a 65-character hex run; any file may quote a 64-character hash, which is allowed), so the repository's text scan must treat `tests/win/fixtures/` as the one place where synthetic planted values are expected.

| File | What it is | Expected result of `scripts/windows_check.py` |
|---|---|---|
| `report_gpu12_pro_16gb` | Pro edition, 15.9 GB RAM, a 12 GB NVIDIA card read by nvidia-smi | exit 0, gpu-8-12, RAM 16+, Pro, WSL2 ok |
| `report_nogpu_home_8gb` | Home edition, 7.8 GB RAM, no graphics device listed | exit 0, gpu none, RAM 8-15, BitLocker not offered |
| `report_gpu24_pro_32gb` | 24 GB card, 31.8 GB RAM | exit 0, gpu-16+ |
| `report_software_gpu` | only a "Basic Render" software device | exit 0, gpu none |
| `report_vram_capped_only` | NVIDIA card whose only memory figure is the 4 GB-capped field | exit 1, VRAM unreadable |
| `report_vram_nvidia_over_cap` | same kind of card, memory taken from nvidia-smi | exit 0, VRAM from nvidia-smi |
| `report_gpu_low_4gb` | 4 GB NVIDIA card | exit 0, gpu-low |
| `report_amd_16gb` | 16 GB AMD card read from the registry | exit 0, capped at gpu-low (not NVIDIA) |
| `report_below_blender_floor` | 2 cores, 3.9 GB RAM, no GPU | exit 0, "below on" is information |
| `report_old_ffmpeg6` | ffmpeg 6.0 without zscale | exit 0, optional filter noted |
| `report_ffmpeg9` | ffmpeg 9.0.2 | exit 0, "run the colour-patch test on this build" |
| `report_craft_pins_mixed` | one pin match, one fallback pin, one mismatch, three absent or unpinned | exit 1, one finding |
| `report_identifying` | planted e-mail, non-documentation IPv4, MAC, profile path; a documentation IPv4 that must not be a hit; an invented user and computer name that only a name check finds | exit 2, one `category= field= hit=xx**` line per hit |
| `report_short_username_collision` | invented 4-letter user name `zeta` is also part of the graphics card name | with `--forbid zeta`: exit 0 with NOTE lines |
| `report_short_username_leak` | the same name in a free-text field | with `--forbid zeta`: exit 2, category user_name, field tools.git.notes |
| `report_version_strings_not_ip` | driver, OS, PowerShell and tool versions shaped like IPv4 addresses, one with a zero-padded part | exit 0 |
| `report_sha256_ok` | a 64-hex checksum quoted in a note | exit 0 |
| `report_hex65_leak` | a 65-hex run in a note | exit 2, category guid_serial |
| `report_bom` | the gpu12 report saved with a UTF-8 byte-order mark | same result as the plain file |

A UTF-16 copy (with and without a byte-order mark) is generated at test time with `iconv`.
