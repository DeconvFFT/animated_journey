"""rt_common.py: small helpers shared by the round-trip tools (WP-06). Standard library only.

  Report     collects named checks (PASS / FAIL / WARN lines) and turns them into an exit code (build plan 4.3)
  png_info   reads a PNG header and walks its chunks (CRC-checked) without Pillow

Not a command. It prints nothing by itself, reads no file except the ones handed to png_info as bytes, and writes
only the JSON file a caller asks Report.finish() for.
"""
import json
import struct
import sys
import zlib

sys.dont_write_bytecode = True

PNG_SIG = b"\x89PNG\r\n\x1a\n"


class Report:
    """A list of named checks. Every row is (status, code, detail); status is PASS, FAIL or WARN.

    A FAIL names the reason (code) that a planted defect is expected to trigger. A WARN never changes the exit code.
    """

    def __init__(self, tool, subject, extra=None):
        self.tool = tool
        self.subject = subject
        self.rows = []
        self.extra = dict(extra or {})

    def ok(self, code, detail=""):
        self.rows.append(("PASS", code, detail))

    def fail(self, code, detail=""):
        self.rows.append(("FAIL", code, detail))

    def warn(self, code, detail=""):
        self.rows.append(("WARN", code, detail))

    def check(self, cond, ok_code, fail_code, detail_fail="", detail_ok="", soft=False):
        """PASS under ok_code when cond holds; otherwise FAIL (or WARN if soft) under fail_code, the named reason."""
        if cond:
            self.ok(ok_code, detail_ok)
        elif soft:
            self.warn(fail_code, detail_fail)
        else:
            self.fail(fail_code, detail_fail)
        return bool(cond)

    def failed_codes(self):
        return sorted({c for s, c, _ in self.rows if s == "FAIL"})

    def counts(self):
        n = {"PASS": 0, "FAIL": 0, "WARN": 0}
        for s, _, _ in self.rows:
            n[s] += 1
        return n

    def finish(self, json_path=None, quiet=False):
        """Print every row and the RESULT line; write the JSON if asked; return the exit code (0 or 1)."""
        if not quiet:
            for s, c, d in self.rows:
                print("%-4s %-34s %s" % (s, c, d))
            n = self.counts()
            print("RESULT %s: %d checks, %d FAIL, %d WARN%s" % (
                self.tool, len(self.rows), n["FAIL"], n["WARN"],
                (" (" + ", ".join("%s=%s" % kv for kv in sorted(self.extra.items())) + ")") if self.extra else ""))
            if n["FAIL"]:
                print("FAILED: " + ", ".join(self.failed_codes()))
        if json_path:
            doc = {"schema": "lj-roundtrip-report/1", "tool": self.tool, "subject": self.subject, "extra": self.extra,
                   "counts": self.counts(), "failed_codes": self.failed_codes(),
                   "checks": [{"status": s, "code": c, "detail": d} for s, c, d in self.rows]}
            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(doc, f, indent=2, sort_keys=True)
                f.write("\n")
        return 1 if self.counts()["FAIL"] else 0


def png_info(data):
    """Parse a PNG held in memory. Returns a dict with width, height, bit_depth, colour_type, interlace, chunks (names),
    icc_name (or None). Raises ValueError with a short reason when the bytes are not a well-formed PNG
    (bad signature, short chunk, CRC mismatch, no IHDR, no IDAT, no IEND). Does not decompress the pixels."""
    if len(data) < 33 or data[:8] != PNG_SIG:
        raise ValueError("not a PNG (bad signature)")
    pos = 8
    info = {"chunks": [], "icc_name": None}
    seen_ihdr = seen_idat = seen_iend = False
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        crc_bytes = data[pos + 8 + length:pos + 12 + length]
        if len(body) != length or len(crc_bytes) != 4:
            raise ValueError("truncated chunk %r" % ctype.decode("latin-1"))
        (crc,) = struct.unpack(">I", crc_bytes)
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise ValueError("CRC mismatch in chunk %r" % ctype.decode("latin-1"))
        name = ctype.decode("latin-1")
        info["chunks"].append(name)
        if name == "IHDR":
            if length != 13:
                raise ValueError("IHDR has the wrong length")
            w, h, depth, ctype_, comp, filt, inter = struct.unpack(">IIBBBBB", body)
            info.update(width=w, height=h, bit_depth=depth, colour_type=ctype_, interlace=inter)
            seen_ihdr = True
        elif name == "IDAT":
            seen_idat = True
        elif name == "iCCP":
            info["icc_name"] = body.split(b"\x00", 1)[0].decode("latin-1")
        elif name == "IEND":
            seen_iend = True
            break
        pos += 12 + length
    if not seen_ihdr:
        raise ValueError("no IHDR chunk")
    if not seen_idat:
        raise ValueError("no IDAT chunk")
    if not seen_iend:
        raise ValueError("no IEND chunk")
    if info["width"] <= 0 or info["height"] <= 0:
        raise ValueError("zero image size")
    return info
