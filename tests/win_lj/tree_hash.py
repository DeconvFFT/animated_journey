#!/usr/bin/env python3
"""tree_hash.py PATH [PATH ...] [--exclude NAME]: one SHA-256 over everything below the paths, without following links.

For every entry (sorted) it hashes: the relative path, the kind (file, folder, link), the mode, the size, the
modification time in nanoseconds, the link target for a link, and the content of a file. So a created, removed, renamed,
touched, re-permissioned or rewritten entry changes the hash. Prints "HASH <hex> entries=<n>" (nothing else on success).
--exclude NAME skips any entry with that name at any depth (used to leave out a folder another job writes to).
Exit 2 on bad usage or an unreadable path.
"""
import hashlib
import os
import stat
import sys


def main(argv):
    paths, excl = [], set()
    it = iter(argv)
    for a in it:
        if a == "--exclude":
            excl.add(next(it, ""))
        else:
            paths.append(a)
    if not paths:
        print("usage: tree_hash.py PATH [PATH ...] [--exclude NAME]", file=sys.stderr)
        return 2
    h = hashlib.sha256()
    n = 0
    for base in paths:
        base = os.path.abspath(base)
        if not os.path.lexists(base):
            print("tree_hash: not found: " + os.path.basename(base), file=sys.stderr)
            return 2
        entries = [base]
        for dp, dn, fn in os.walk(base, followlinks=False):
            dn[:] = sorted(x for x in dn if x not in excl)
            for x in dn + sorted(f for f in fn if f not in excl):
                entries.append(os.path.join(dp, x))
        for p in entries:
            st = os.lstat(p)
            rel = os.path.relpath(p, os.path.dirname(base))
            if stat.S_ISLNK(st.st_mode):
                kind, extra = "l", os.readlink(p).encode("utf-8", "surrogateescape")
            elif stat.S_ISDIR(st.st_mode):
                kind, extra = "d", b""
            else:
                kind = "f"
                c = hashlib.sha256()
                try:
                    with open(p, "rb") as f:
                        for chunk in iter(lambda: f.read(1 << 20), b""):
                            c.update(chunk)
                except OSError:
                    print("tree_hash: cannot read an entry", file=sys.stderr)
                    return 2
                extra = c.digest()
            h.update(("%s\0%s\0%o\0%d\0%d\0" % (rel, kind, st.st_mode, st.st_size, st.st_mtime_ns)).encode("utf-8", "surrogateescape"))
            h.update(extra)
            n += 1
    print("HASH %s entries=%d" % (h.hexdigest(), n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
