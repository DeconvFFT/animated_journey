# lj.ps1: the session helper (version 0)

This is the first version of one small script, `win\lj.ps1`. It does two jobs:

- **`doctor`** tells you what kind of computer this is (the hardware tier the plans depend on).
- **`close`** shows you what an end-of-session clean-up **would** remove, so you can see it before anything is ever removed.

**Version 0 is a dry run. It cannot delete, move, rename, commit, push or write anything.** There is no switch that does. The switches for the real thing arrive in version 1 (week 4), after you have read these lists for a while and trusted them.

## What it never does

- It never removes or changes a file. Not a photo, not a sidecar, not a cache, not a log. It does not even write a log of its own.
- It never touches anything in a folder named `media`, `archive`, `masters` or `originals`, the project folder, another git repository, or an encrypted container. It does not open those folders, so it never shows the names of the files inside them.
- It never follows a shortcut-style link (a symbolic link or junction). It lists it as `SKIPPED (link)` and moves on.
- It never uses the network, never installs anything, and needs no administrator rights.
- It never prints your Windows user name, your computer name or your user folder. Your user folder is shown as `%USERPROFILE%`.

If you type `-Apply`, `-Commit` or `-IncludeWindowsRecent`, it answers `not in v0: planned for v1 in week 4; nothing was done` and stops with exit code 2.

## Before you start

Use the **whole project folder**, the same way as for the first PC inventory (see `README-MAKER.md`, the section about getting the files and about running a script for one session only). `lj.ps1` reads files that sit next to it, so a single downloaded file will not work.

All commands below are run from the project folder, in a normal (not administrator) PowerShell window. They start the script for this one run only and change no system setting.

To see the short built-in help:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 help
```

## doctor: what kind of computer is this?

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 doctor
```

What happens, in order:

1. It runs the same read-only inventory as before (`step0_pc_tests.ps1`). **That inventory script writes one file of its own, `%TEMP%\lj_pc_report.json`.** `lj.ps1` itself writes nothing. As before, you open that file in Notepad, read it, and paste it in chat only, never into the project folder.
2. It looks for Python (`py -3`, then `python`). If there is none, it says so and stops: that is fine, because pasting the report in chat gets you the same table.
3. It runs `scripts\windows_check.py` on the report and prints the **tier table**: graphics tier, memory tier, Windows edition, free disk, ffmpeg, Python, Git and the Craft app versions.

The table shows exact sizes, so it is for you and for chat. Do not copy it into the project folder.

If you already have a report and only want the table (nothing is collected from this computer), name it:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 doctor -FromReport "$env:TEMP\lj_pc_report.json"
```

If you want a small file that **is** safe to keep in the project (only buckets and verdict words, no hardware names and no exact sizes), add `-SaveTier`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 doctor -FromReport "$env:TEMP\lj_pc_report.json" -SaveTier .\pc_tier.json
```

`-SaveTier` writes that one derived file and nothing else. It refuses a file name that looks like a raw report, a name that does not end in `.json`, a folder, and any existing file that is not a tier file.

Exit codes for `doctor`: `0` the report is fine and nothing needs a human; `1` the report is valid but a finding needs a human (it is printed as `FINDING`); `2` the report was refused (invalid, or it looks like it holds identifying data, in which case nothing is saved); `3` something is missing (no Python, or a file next to the script).

## close: what would a clean-up remove?

### Set it up once

1. In File Explorer, open the `win` folder, copy `lj.config.example.json`, and rename the copy to `lj.config.local.json`. The copy stays on your PC (it is not for the project folder).
2. Open the copy in Notepad:

```powershell
notepad .\win\lj.config.local.json
```

3. Change `root` to the folder that holds your working folders, for example `C:/lj`. Use forward slashes. The tools folder (`tools`) must be **inside** the root.

The part of the file you will change most looks like this:

```json
{
  "schema": "lj-config/1",
  "root": "C:/lj",
  "tools_root": "tools",
  "work_folder_names": ["work"]
}
```

`close` refuses to run (exit code 2, nothing done) if the root is a whole drive (like `C:/`), the project folder or anything inside it, your user folder or a folder that contains it, a Windows system folder, a link, or another git repository.

### Run it

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 close
```

Add `-Config` to use a different config file, and `-SkipChecks` to leave out the two repo checks (they take about ten seconds):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\lj.ps1 close -Config .\win\lj.config.local.json -SkipChecks
```

### How to read the list

The script prints each step before it does it, then the result. Then:

- **WOULD REMOVE** is the numbered list. Nothing is removed in version 0. Each line says what it is, how many files, how big, and where (`<root>` stands for your root folder). It lists:
  - `*.xmp` sidecar files under any folder named `work`, one line per file;
  - folders named `Recovery`, `Auto-Save` or `cache` anywhere under the tools folder, **one line per folder** (the files inside are counted, not listed by name);
  - the entries of the per-app lists (below).
- **HELD BACK** lists things that look removable but that version 1 would not remove without you: a Recovery folder with a protected folder or a link inside it, or a per-app entry that was refused (and why).
- **NOT ON THE LIST** are entries with nothing there, or already counted above.
- **SKIPPED (link)** are links. They are never followed, so what they point at is never looked at.
- **NEVER TOUCHED** repeats the rule and shows which protected folders, other git repositories or possible encrypted-container files (`.hc`, `.tc`) were found under your root. A container that is currently mounted as a drive cannot be recognised by version 0; if yours is mounted inside the root, add its folder to `never_touch_paths` in your config.
- **PER-APP LISTS** show, for each Craft app, how many recent-file and cache entries are in your config, and the word **UNVERIFIED** (see the next section).
- **CHECKS** run `stale_check.py --new-only` and `public_lint.py` (read-only) if Python is present, and print what they say. In version 0 they are advice: they do not change the exit code of `close`. The two checks read the project folder and start `git` to look at what changed; they do not change anything.
- **BACKUP: not implemented in v0 (week 4)** is exactly what it says.
- **REMINDERS** ask you to dismount the encrypted container and close the Craft apps.
- The last lines say `files written: none`.

Exit codes for `close`: `0` the dry run finished; `1` it finished but the list may be incomplete (a folder could not be read, or the safety limit of 250,000 entries was reached); `2` it refused (a bad root, a bad config, or one of the version 1 switches); `3` something is missing.

### The per-app lists and the Saturday paste

Each Craft app keeps its recent-file list, and some keep a cache, in a folder we have only read about, never seen on your PC. Until you have run the five-minute tests, those lists are empty and marked **UNVERIFIED** on purpose: guessing a folder to delete would be worse than leaving it empty.

After each app's test, the Craft zips guide (the section called "Where did it write?") asks you to paste what changed. From that paste, the lists are filled in, with the folders written like this:

- a path that starts with `%USERPROFILE%\AppData\Roaming\` becomes `%APPDATA%/`
- a path that starts with `%USERPROFILE%\AppData\Local\` becomes `%LOCALAPPDATA%/`
- a folder beside the program becomes a path relative to the tools folder, for example `lightcraft-0.9.1/LightCraftData/recent.json` (a `*` stands for "any version", for example `lightcraft-*/LightCraftData/recent.json`)

An entry is accepted only if it sits **inside** the tools folder, `%APPDATA%` or `%LOCALAPPDATA%`, has a folder whose name contains the app's name, has no `..` in it, and does not go through a protected folder name or a link. Otherwise it is shown under HELD BACK as `REFUSED`, with the reason. The `note` text in the example config repeats what our notes say about each app; that text is **not** used to find anything.

Known gap in version 0: an `Auto-Save` folder that sits next to a project inside a `work` folder (FilmCraft writes one there) is not on the list, because the plan names only the tools folder for these folder names. Version 1 will decide this after the paste.

## If it says REFUSED

Read the sentence after `REFUSED:`. It names the reason and says `Nothing was done`. The usual causes are a missing `lj.config.local.json`, a `root` that does not exist, or a `root` that is too wide. Fix the config and run it again. You never need to change anything else, and you must not point `root` at a wider folder to "make it work".

## What comes next

Version 1 (week 4) adds the real clean-up: removing the items on this list after you confirm, committing the text changes to the project without pushing, running the backup, and writing a log. Only then does the end-to-end "close a session" run that the process lock asks for happen. Version 0 does not count as that run.

## What has not been checked on a real Windows PC (UNVERIFIED)

Everything above was tested on Linux with made-up folders and links. Not yet checked on Windows: how links and junctions show up on NTFS; whether `py -3` and `python` behave as expected (including the Microsoft Store stub); every behaviour of Windows PowerShell 5.1; short 8.3 folder names; `%APPDATA%` and `%LOCALAPPDATA%` on a managed PC; and every per-app list. Your first run is the check, and what you paste back is the evidence.
