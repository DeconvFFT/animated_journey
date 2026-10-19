# Your PC inventory: how to run it, read it and share it

This is the first thing to run on your Windows PC. It takes about three minutes. It only **reads** facts about the computer and writes **one small file**. Nothing is installed, deleted or changed.

If anything below is unclear, stop and ask in chat before you run anything. A pause costs nothing.

## What this is and what it never does

The script `win\step0_pc_tests.ps1` looks up how powerful your PC is, so the plan can pick tools that really run on it. It asks Windows for:

- the Windows version and edition (Home or Pro), the processor, the memory (RAM);
- the graphics card and how much video memory it has;
- the drives and how much free space each has (letters and sizes only);
- the screen size;
- which of these programs are present and their version numbers: ffmpeg, ffprobe, Python, Git, winget, WSL, ImageMagick, Inkscape, Blender, VeraCrypt. To read a version it starts ffmpeg, ffprobe, Python, Git and winget with their `--version` option, and asks `nvidia-smi` (the graphics-memory tool, if you have an NVIDIA card), `wsl --status` and `vulkaninfo` for their status when they exist. It reads the ffmpeg program file once to compute its fingerprint (a SHA-256), so the colour test can say exactly which build it ran on. ImageMagick, Inkscape, Blender and VeraCrypt are only looked for as files; they are never started;
- the folder names under `C:\lj\tools` (and `C:\LifeJourney\tools`) to see which Craft apps are there. It never starts a Craft app.

It **never**:

- changes a setting, installs or removes anything, or touches the registry except to read it;
- uses the internet;
- opens your photos, documents, browser or any of your own files;
- records your user name, computer name, domain, serial numbers, ID numbers, network addresses, Wi-Fi names, disk labels or any folder inside your user folder;
- needs administrator rights.

Before it saves the report, it checks the report against a list of "identifying data" patterns and against your own user name and computer name (it reads those from Windows at that moment and does not save them). If something matches, it **refuses to save** and tells you what kind of thing matched.

**Not yet tested on a real Windows PC.** The script was built and tested on Linux with made-up reports. Every line that asks Windows a question (hardware, drives, screen, accounts) is untested until your first run. If something looks wrong, that is useful news, not your fault.

## How to get the files onto the PC

You need the **whole project folder**, not single files. The script reads `scripts\redaction_patterns.json` and stops if it is missing.

1. Open the project page from the link in your notes.
2. Use the green Code button, then Download ZIP. (If you already use Git, `git clone` works too.)
3. Right-click the ZIP in File Explorer, choose Properties, tick Unblock if you see it, press OK. Then right-click again and choose Extract All.
4. Put the extracted folder somewhere simple, for example `C:\lj\project`. Avoid folders that sync to the cloud, such as OneDrive, Desktop or Documents.

To open a PowerShell window in that folder: open the folder in File Explorer, click the address bar, type `powershell` and press Enter.

## How to run a script for one session only, without changing system policy

Windows blocks scripts by default. You do **not** need to change that for the whole PC. These two options allow one script for one window only.

**Option A (simplest).** This allows the script for this one run only:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\step0_pc_tests.ps1
```

**Option B.** This relaxes the rule for the current window only. When you close the window, everything is back to normal, and the machine and user settings are never touched:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\win\step0_pc_tests.ps1
```

Two read-only helpers if something does not work:

```powershell
Get-ExecutionPolicy -List
```

That shows the policy at each level. It changes nothing. Paste the result in chat if you are stuck.

```powershell
Unblock-File .\win\step0_pc_tests.ps1
```

Files from the internet carry a small "downloaded from the internet" mark. This command removes that mark from that one file and does nothing else.

**If your PC is managed by Group Policy** (a work or school computer), both options may still say the script is blocked by a policy. Then **stop and change nothing**. Tell the orchestrator in chat what the message says. Do not look for ways around it.

## The 3-minute PC inventory

1. Open PowerShell in the project folder (see above).
2. Run Option A. Windows PowerShell 5.1 (the blue window that comes with Windows) and PowerShell 7 both work.
3. Watch the lines. Each step prints what it is about to do, then `ok`, `skipped` or `failed`. A `failed` step does not stop the others.
4. At the end it prints the line `files written:` followed by `%TEMP%\lj_pc_report.json`. That is the only file it writes. (`%TEMP%` is Windows' temporary folder; the script does not print its real location, so what you paste never shows your user name.)

You can leave other programs open. The report only notes yes or no whether the Claude app is running. It matters later, for render tests.

## Reading the report yourself before you paste it

Open the file in Notepad:

```powershell
notepad "$env:TEMP\lj_pc_report.json"
```

Read it once. You should see hardware names, sizes and version numbers. You should **not** see your name, your computer's name, an e-mail address, a number like 192 dot 168, or a path that runs through your own user folder. If you do, do not paste it: tell the orchestrator in chat what kind of line it is (not the line itself).

Then paste the whole text **into the chat and nowhere else**:

- not into the project folder, not into Git, not into an e-mail or a note on a synced service;
- the report lists your exact graphics card, processor and sizes, which together are a fingerprint of this one machine, and the project page is public.

The orchestrator will turn what you paste into a short summary of hardware levels (for example "graphics: 8 to 12 GB class") and file only that summary.

When you are done you can delete the report in File Explorer (type `%TEMP%` in the address bar and delete `lj_pc_report.json`).

**Optional, for this PC only:** if you want the script to also refuse your family's names, create a plain text file `scripts\public_lint.deny.local.txt` in Notepad and put one name per line. The script and the checker read it. It never leaves the PC: do not copy it, paste it or commit it, and never type a name into a command.

## If the script refuses to write the report

You may see this:

```text
REDACTION CHECK FAILED, nothing was written
category=email field=notes[0] hit=ab******
```

What the three parts mean:

- `category` is the kind of thing it thinks it found (for example `email`, `user_name`, `computer_name`, `profile_path_windows`, `guid_serial`);
- `field` is where in the report it was found;
- `hit` is the first two letters of the match followed by stars.

These lines contain only a kind, a place and two letters, so they are **safe to paste into chat**.

Things to know:

- A short user name can collide with a vendor name. If a short word of yours also appears inside the processor or graphics card name, the script prints `NOTE ... (a hardware-name field: reported, not refused)` and still writes the report. That is fine.
- If it refuses, nothing is saved at all. **Do not edit the JSON by hand to get past it.** That would defeat the point.
- If it says `REDACTION PATTERNS UNAVAILABLE`, the file `scripts\redaction_patterns.json` is missing. Download the whole project folder again.

What to paste in chat so the orchestrator can adjust the rule the same day: the refusal lines above, plus the output of the six commands in the next section.

## If it fails

If the script will not run at all, paste these six lines one at a time into a PowerShell window and paste what each prints into chat. They only read. They print no names.

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, BuildNumber
```

```powershell
[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
```

```powershell
Get-CimInstance Win32_VideoController | Select-Object Name
```

```powershell
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, @{ n = 'FreeGB'; e = { [math]::Round($_.FreeSpace / 1GB, 1) } }
```

```powershell
ffmpeg -version | Select-Object -First 1
```

```powershell
py -0
```

The last line lists the Python versions you have. (If you ever see `py -0p` suggested, it prints folder paths that can contain your user name, so replace that part before pasting.) If ffmpeg or py is not found, say so; that is also an answer.

## What comes next

These arrive later, one at a time, each with its own short instructions. None exists as a file yet, so there is nothing to look for:

- the hours page (how to log the time you spend);
- the Craft-zip guide (downloading and checking the Craft apps, planned for Saturday);
- the Ken Burns and archive kit (the first small film move, and the archive with five stand-in scans);
- `lj.ps1` (a helper that will show you what a session close would do; first as a read-only preview, Tuesday 27 October).

## The VeraCrypt container

Later (planned for Wednesday 28 October) you will set up an encrypted container on your external drive for the family material. The container is **created from an administrator account** (it needs the extra rights once) and then **mounted from the project account** you use for this work, only while you are working, and dismounted before you leave the desk. BitLocker can be added on Windows Pro. None of this is needed for the inventory. It is only here so the plan makes sense.
