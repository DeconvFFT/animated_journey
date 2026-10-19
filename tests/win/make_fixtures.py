#!/usr/bin/env python3
"""make_fixtures.py: writes the SYNTHETIC pc_report fixtures under tests/win/fixtures/ (WP-01a).

Every name, address and number below is invented. The planted "identifying" values use JSON \\u escapes for
the characters an identifying-data regex keys on (at-sign, dots, backslashes, colons), so the files on disk
do not contain the strings they are testing for; the checkers see them after the JSON is parsed.

Usage:  python3 -I tests/win/make_fixtures.py            write the fixtures
        python3 -I tests/win/make_fixtures.py --check    exit 1 if a fixture on disk differs from what this script makes
"""
import copy
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "fixtures"

SHA_A = "3f2a9c41d7e85b60a1c4e9f0b2d37a85c6e1f4092b8d3a7e5c1f60d9b4a28e73"   # 64 hex, invented
SHA_B = "9b1e4c7a02d58f36e1a7c4b90d2f5e83a6c1b7049e3d8f25a0c6b1e47d92f3a5"   # 64 hex, invented


_PLANTED = []
DOT, AT, BS, COLON = ".", chr(64), chr(92), ":"   # built from parts so this source file never contains the strings it plants


def Planted(text):
    """Register a planted value; the returned token is swapped for the \\u-escaped text when the file is written."""
    _PLANTED.append(text)
    return "QQPLANT%dQQ" % (len(_PLANTED) - 1)


def tool(found, version=None, notes=None):
    return {"found": found, "version": version, "notes": notes}


def base():
    ffm = tool(True, "7.1-full_build-www.gyan.dev", "found on PATH; the path is not recorded")
    ffm.update({"has_libx264": True, "has_libass": True, "has_zscale": True, "sha256": SHA_A})
    return {
        "schema_version": 1, "tool": "lj-step0-pc-tests", "tool_version": "1.0.0",
        "generated_utc": "2026-10-20T07:30:00Z",
        "powershell": {"version": "5.1.22621.4391", "edition": "WindowsPowerShell"},
        "os": {"platform": "windows", "caption": "Microsoft Windows 11 Pro", "version": "10.0.22631", "build": "22631.4317",
               "edition_id": "Professional", "architecture": "64-bit"},
        "cpu": {"name": "AMD Ryzen 5 5600X 6-Core Processor", "cores": 6, "logical": 12},
        "ram": {"total_gb": 15.9},
        "gpus": [{"name": "NVIDIA GeForce RTX 3060", "vendor": "NVIDIA", "vram_gb": 12.0, "vram_source": "nvidia-smi",
                  "driver_version": "31.0.15.5222", "is_software": False}],
        "vulkan": {"runtime_dll_present": True, "vulkaninfo_found": False, "devices": []},
        "disks": [{"drive": "C", "type": "fixed", "fs": "NTFS", "size_gb": 476.3, "free_gb": 212.4},
                  {"drive": "D", "type": "fixed", "fs": "NTFS", "size_gb": 931.5, "free_gb": 640.2}],
        "display": {"primary": {"width": 1920, "height": 1080, "refresh_hz": 60, "scale_percent": 100}, "count": 1},
        "tools": {
            "ffmpeg": ffm,
            "ffprobe": tool(True, "7.1-full_build-www.gyan.dev", "found on PATH; the path is not recorded"),
            "python": tool(True, "3.13.15", "found through the py launcher"),
            "git": tool(True, "2.55.0", "found on PATH"),
            "winget": tool(True, "1.9.25200", "found on PATH"),
            "magick": tool(False, None, "not found"),
            "inkscape": tool(False, None, "not found"),
            "blender": tool(False, None, "not found"),
            "wsl": tool(True, "2", "wsl.exe present; default version read"),
            "veracrypt_installed": False,
        },
        "craft_apps": {"tools_roots_scanned": [], "found": [],
                       "not_found": ["photocraft", "vectorcraft", "lightcraft", "filmcraft", "effectcraft", "soundcraft"]},
        "local_accounts_count": 1, "claude_desktop_running": False,
        "redaction": {"user_name_removed": True, "machine_name_removed": True, "paths_generalised": True,
                      "self_scan_passed": True, "patterns_version": 1, "name_hits_in_hardware_fields": []},
        "notes": [], "errors": [],
    }


def make():
    del _PLANTED[:]
    f = {}

    # --- hardware tiers
    r = base(); f["report_gpu12_pro_16gb"] = r

    r = base()
    r["os"].update(caption="Microsoft Windows 11 Home", edition_id="Core")
    r["cpu"].update(name="11th Gen Intel(R) Core(TM) i3-1115G4 @ 3.00GHz", cores=2, logical=4)
    r["ram"]["total_gb"] = 7.8
    r["gpus"] = []
    r["vulkan"]["runtime_dll_present"] = False
    r["disks"] = [{"drive": "C", "type": "fixed", "fs": "NTFS", "size_gb": 237.9, "free_gb": 61.5}]
    r["display"]["primary"].update(width=1366, height=768)
    r["tools"]["wsl"] = tool(False, None, "not found on PATH")
    r["local_accounts_count"] = 2
    f["report_nogpu_home_8gb"] = r

    r = base()
    r["cpu"].update(name="Intel(R) Core(TM) i9-13900K", cores=24, logical=32)
    r["ram"]["total_gb"] = 31.8
    r["gpus"] = [{"name": "NVIDIA GeForce RTX 4090", "vendor": "NVIDIA", "vram_gb": 24.0, "vram_source": "nvidia-smi",
                  "driver_version": "32.0.15.6094", "is_software": False}]
    r["disks"] = [{"drive": "C", "type": "fixed", "fs": "NTFS", "size_gb": 1862.6, "free_gb": 1320.8}]
    r["display"]["primary"].update(width=3840, height=2160, refresh_hz=144, scale_percent=150)
    r["display"]["count"] = 2
    f["report_gpu24_pro_32gb"] = r

    r = base()
    r["gpus"] = [{"name": "Microsoft Basic Render Driver", "vendor": "Microsoft Corporation", "vram_gb": None, "vram_source": "unreadable",
                  "driver_version": "10.0.22621.3672", "is_software": True}]
    f["report_software_gpu"] = r

    r = base()
    r["gpus"] = [{"name": "NVIDIA GeForce RTX 3070", "vendor": "NVIDIA", "vram_gb": None, "vram_source": "adapterram_capped_4gb",
                  "driver_version": "31.0.15.5222", "is_software": False}]
    r["notes"] = ["nvidia-smi was not found on PATH; the memory size comes from the next fallback"]
    f["report_vram_capped_only"] = r

    r = base()
    r["gpus"] = [{"name": "NVIDIA GeForce RTX 3090", "vendor": "NVIDIA", "vram_gb": 24.0, "vram_source": "nvidia-smi",
                  "driver_version": "31.0.15.5222", "is_software": False}]
    r["notes"] = ["the adapter listing showed the 4 GB ceiling; nvidia-smi gave the real memory size"]
    f["report_vram_nvidia_over_cap"] = r

    # extra tier cases of my own (my rules deserve their own tests)
    r = base()
    r["gpus"] = [{"name": "NVIDIA GeForce GTX 1650", "vendor": "NVIDIA", "vram_gb": 4.0, "vram_source": "nvidia-smi",
                  "driver_version": "31.0.15.5222", "is_software": False}]
    f["report_gpu_low_4gb"] = r

    r = base()
    r["gpus"] = [{"name": "AMD Radeon RX 6800 XT", "vendor": "Advanced Micro Devices, Inc.", "vram_gb": 16.0,
                  "vram_source": "registry_qwMemorySize", "driver_version": "31.0.21921.1000", "is_software": False}]
    f["report_amd_16gb"] = r

    r = base()
    r["ram"]["total_gb"] = 3.9
    r["cpu"].update(cores=2, logical=2)
    r["gpus"] = []
    f["report_below_blender_floor"] = r

    # --- tools
    r = base()
    for k in ("ffmpeg", "ffprobe"):
        r["tools"][k]["version"] = "6.0-essentials_build-www.gyan.dev"
    r["tools"]["ffmpeg"]["has_zscale"] = False
    r["tools"]["ffmpeg"]["sha256"] = SHA_B
    f["report_old_ffmpeg6"] = r

    r = base()
    for k in ("ffmpeg", "ffprobe"):
        r["tools"][k]["version"] = "9.0.2-essentials_build-www.gyan.dev"
    f["report_ffmpeg9"] = r

    r = base()
    r["craft_apps"] = {
        "tools_roots_scanned": ["C:\\lj\\tools", "C:\\LifeJourney\\tools"],
        "found": [
            {"app": "photocraft", "version": "0.10.0", "pinned_version": "0.10.0", "matches_pin": True},
            {"app": "filmcraft", "version": "0.8.0", "pinned_version": "0.9.0", "matches_pin": False},
            {"app": "vectorcraft", "version": "0.12.9", "pinned_version": "0.13.1", "matches_pin": False},
        ],
        "not_found": ["lightcraft", "effectcraft", "soundcraft"],
    }
    f["report_craft_pins_mixed"] = r

    # --- redaction cases
    r = base()
    r["notes"] = [
        Planted("gateway " + DOT.join(["10", "77", "88", "99"]) + " answered"),   # an IPv4 outside the documentation ranges
        "operator tamsinwrex asked for this run",                     # found only when the name is given (a fake user)
        "machine BRAMBLE-Q7 was busy",                                # found only when the name is given (a fake computer)
        Planted("adapter " + COLON.join(["02", "1A", "2B", "3C", "4D", "5E"]) + " ready"),   # a MAC
        "documentation address " + Planted(DOT.join(["203", "0", "113", "9"])) + " is allowed",  # allowed range, must NOT be a hit
        "reserved address " + Planted("wrex" + AT + "example" + DOT + "invalid") + " is allowed",  # reserved documentation domain, must NOT be a hit
    ]
    r["errors"] = [Planted("Access to the path '" + COLON.join(["C", BS.join(["", "Users", "tamsinwrex", "AppData", "Local", "Temp"])]) + "' was denied")]
    r["tools"]["git"]["notes"] = Planted("contact tamsin" + DOT + "wrex" + AT + "brambleworks" + DOT + "zz")     # an invented, non-reserved domain: a hit
    f["report_identifying"] = r

    r = base()   # the invented 4-letter user name "zeta" is also part of a vendor string: reported, not refused
    r["gpus"] = [{"name": "Zeta-Gfx 7 Series", "vendor": "Zeta Graphics", "vram_gb": 8.0, "vram_source": "registry_qwMemorySize",
                  "driver_version": "1.2.3", "is_software": False}]
    f["report_short_username_collision"] = r

    r = base()   # the same name in a free-text field: refused
    r["tools"]["git"]["notes"] = "set up by zeta last week"
    f["report_short_username_leak"] = r

    r = base()   # version strings that are shaped like IPv4 addresses, including a zero-padded last part
    r["gpus"][0]["driver_version"] = Planted(DOT.join(["23", "40", "27", "06"]))
    r["os"].update(version=Planted(DOT.join(["10", "0", "22631", "4317"])), build="22631.4317")
    r["powershell"]["version"] = Planted(DOT.join(["5", "1", "22621", "4391"]))
    r["tools"]["wsl"]["version"] = Planted(DOT.join(["2", "0", "9", "0"]))
    r["tools"]["winget"]["version"] = "1.9.25200"
    r["tools"]["python"]["version"] = "3.13.15"
    f["report_version_strings_not_ip"] = r

    r = base()   # a published checksum quoted in free text: exactly 64 hex characters, allowed
    r["tools"]["ffmpeg"]["notes"] = "matches the published checksum " + SHA_A
    f["report_sha256_ok"] = r

    r = base()   # 65 hex characters: not a SHA-256, refused
    r["notes"] = ["token " + SHA_A + "f"]
    f["report_hex65_leak"] = r

    # BOM copy of the plain gpu12 report (written below with a UTF-8 BOM)
    f["report_bom"] = copy.deepcopy(f["report_gpu12_pro_16gb"])
    return f


def esc_planted(s):
    return "".join(ch if (ch.isalnum() or ch == " ") else "\\u%04x" % ord(ch) for ch in s)


def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=True)
    for i, original in enumerate(_PLANTED):
        text = text.replace("QQPLANT%dQQ" % i, esc_planted(original))
    return text + "\n"


def main():
    check = "--check" in sys.argv
    fixtures = make()
    bad = 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, obj in sorted(fixtures.items()):
        # mixed strings (plain + Planted) lose their Planted type under +; escape the known planted spans explicitly
        text = dump(obj)
        data = text.encode("utf-8")
        if name == "report_bom":
            data = b"\xef\xbb\xbf" + data
        p = OUT / (name + ".json")
        if check:
            if not p.is_file() or p.read_bytes() != data:
                print("DIFFERS: %s" % p.name)
                bad += 1
        else:
            p.write_bytes(data)
    if check:
        print("fixtures in sync" if not bad else "%d fixture(s) differ" % bad)
        return 1 if bad else 0
    print("wrote %d fixtures to %s" % (len(fixtures), OUT.name + "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
