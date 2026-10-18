# step0_pc_tests.ps1: one script that runs every "pending" check on the maker's Windows PC and writes ONE report to paste back.
# Research fixture for research/toolchain.md, "Follow-up research (round 2)", F9. Written 2026-10-18.
# STATUS: parse-checked and run on PowerShell 7.5.4 (Linux) with stand-in tools; NOT yet run on Windows. TODO(verify on the maker's PC).
#
# HOW TO RUN (about 10 minutes, no personal files are read or written):
#   1. Close the Claude desktop app (it is the memory hog; the script lists any Claude process it still sees).
#   2. Make an empty folder, for example C:\lj_step0, and copy into it: this file, r2_param.py (same folder as this
#      file) and r5_story.mlt (from skills\free-creative-toolchain\recipes). Open PowerShell in that folder.
#   3. Run:   powershell -ExecutionPolicy Bypass -File .\step0_pc_tests.ps1
#      Optional tool paths (when a tool is not on PATH):
#      .\step0_pc_tests.ps1 -Ffmpeg 'C:\Tools\kdenlive\bin\ffmpeg.exe' -Melt 'C:\Tools\kdenlive\bin\melt.exe' -Blender 'D:\blender-5.2.2-windows-x64\blender.exe'
#   4. Open step0_report.txt and paste the whole text back to the orchestrator. Nothing in it is personal.
#
# Written without PowerShell-7-only syntax (no ??, no ?:, no &&) so it should also run in Windows PowerShell 5.1; only PowerShell 7.5.4 was used.
# Every section is wrapped so one failure does not stop the rest.
param(
    [string]$Ffmpeg   = 'ffmpeg',
    [string]$Ffprobe  = '',
    [string]$Magick   = 'magick',
    [string]$Inkscape = '',
    [string]$Gimp     = '',
    [string]$Melt     = 'melt',
    [string]$Blender  = '',
    [string]$R2Param  = '.\r2_param.py',
    [string]$StoryMlt = '.\r5_story.mlt'
)
$ErrorActionPreference = 'Continue'
$here   = (Get-Location).Path
$report = Join-Path $here 'step0_report.txt'
Set-Content -Path $report -Value ("step0 report, started " + (Get-Date -Format 's')) -Encoding ascii
$isWin  = ($env:OS -eq 'Windows_NT')
function Abs([string]$p) { if ([System.IO.Path]::IsPathRooted($p)) { return $p } else { return (Join-Path $here ($p -replace '^\.[\\/]', '')) } }
$StoryMlt = Abs $StoryMlt     # resolved now, before the script changes folder
$R2Param  = Abs $R2Param
function Say([string]$t)     { Add-Content -Path $report -Value $t -Encoding ascii; Write-Host $t }
function Section([string]$t) { Say ''; Say ('=== ' + $t) }
function Has([string]$n)     { return [bool](Get-Command $n -ErrorAction SilentlyContinue) }
function Try-Run([string]$what, [scriptblock]$sb) {
    try { & $sb } catch { Say ("FAILED: $what : " + $_.Exception.Message) }
}
function First-Existing([string[]]$paths) { foreach ($p in $paths) { if ($p -and (Test-Path $p)) { return $p } }; return '' }
function Pass([string]$name, [bool]$ok, [string]$detail) { if ($ok) { Say ("PASS  $name  $detail") } else { Say ("FAIL  $name  $detail") } }

if (-not $Ffprobe) { if (Test-Path $Ffmpeg) { $Ffprobe = Join-Path (Split-Path $Ffmpeg) 'ffprobe.exe' } else { $Ffprobe = 'ffprobe' } }
if (-not $Inkscape) { $Inkscape = First-Existing @("$env:ProgramFiles\Inkscape\bin\inkscape.com", "${env:ProgramFiles(x86)}\Inkscape\bin\inkscape.com", "$env:LOCALAPPDATA\Programs\Inkscape\bin\inkscape.com") }
if (-not $Inkscape -and (Has 'inkscape')) { $Inkscape = 'inkscape' }
if (-not $Gimp) { $Gimp = First-Existing @("$env:LOCALAPPDATA\Programs\GIMP 3\bin\gimp-console-3.2.exe", "$env:ProgramFiles\GIMP 3\bin\gimp-console-3.2.exe") }
if (-not $Gimp -and (Has 'gimp-console-3.2')) { $Gimp = 'gimp-console-3.2' }

# ---------------------------------------------------------------- 1. inventory (the F3 block)
Section '1. Inventory'
Try-Run 'powershell version' { Say ("PowerShell " + $PSVersionTable.PSVersion + " edition " + $PSVersionTable.PSEdition) }
if ($isWin) {
    Try-Run 'os'  { $o = Get-CimInstance Win32_OperatingSystem; Say ("OS " + $o.Caption + " build " + $o.BuildNumber + " " + $o.OSArchitecture) }
    Try-Run 'ram' { $c = Get-CimInstance Win32_ComputerSystem; Say ("Model " + $c.Model + "; RAM_GB " + [math]::Round($c.TotalPhysicalMemory / 1GB, 1)) }
    Try-Run 'cpu' { Get-CimInstance Win32_Processor | ForEach-Object { Say ("CPU " + $_.Name + "; cores " + $_.NumberOfCores + "; threads " + $_.NumberOfLogicalProcessors) } }
    Try-Run 'gpu' { Get-CimInstance Win32_VideoController | ForEach-Object { Say ("GPU " + $_.Name + "; driver " + $_.DriverVersion + "; adapter RAM bytes " + $_.AdapterRAM) } }
    Try-Run 'free ram now' { $os = Get-CimInstance Win32_OperatingSystem; Say ("Free RAM now GB " + [math]::Round($os.FreePhysicalMemory / 1MB, 2)) }
    Try-Run 'disk' { Get-PSDrive -PSProvider FileSystem | ForEach-Object { if ($_.Used -ne $null) { Say ("Drive " + $_.Name + " free GB " + [math]::Round($_.Free / 1GB, 1)) } } }
}
Try-Run 'python' { if (Has 'py') { Say ((& py -0p 2>&1) -join ' | ') } else { Say 'py launcher: not found' }; if (Has 'python') { Say ((& python --version 2>&1) -join ' ') } }
Try-Run 'wsl' { if (Has 'wsl') { Say ("wsl --status: " + ((& wsl --status 2>&1) -join ' ' -replace "`0", '')) } else { Say 'wsl: not found' } }
Try-Run 'claude app' { $p = Get-Process | Where-Object { $_.ProcessName -match 'claude' }; if ($p) { Say ("WARNING Claude processes still running: " + (($p | ForEach-Object { $_.ProcessName + ' ' + [math]::Round($_.WorkingSet64 / 1MB) + 'MB' }) -join '; ')) } else { Say 'No Claude process running (good).' } }
Say 'Tools on PATH:'
foreach ($n in 'ffmpeg','ffprobe','magick','mogrify','inkscape','gimp-console-3.2','melt','blender','rsvg-convert','git','bash','python','pwsh') {
    $c = Get-Command $n -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c) { Say ("  $n : " + $c.Source) } else { Say "  $n : not on PATH" }
}
Say ("Paths used: ffmpeg=$Ffmpeg ffprobe=$Ffprobe magick=$Magick inkscape=$Inkscape gimp=$Gimp melt=$Melt blender=$Blender")

# ---------------------------------------------------------------- work folder with synthetic inputs
$work = Join-Path $here 'work'
New-Item -ItemType Directory -Force -Path $work | Out-Null
Set-Location $work
New-Item -ItemType Directory -Force -Path 'in','out','frames','photos_16x9' | Out-Null

# ---------------------------------------------------------------- 2. ImageMagick (R1a, Exercise 1)
Section '2. ImageMagick 7: magick, magick mogrify, identify loop (R1a, Exercise 1)'
Try-Run 'magick' {
    Say ((& $Magick -version 2>&1 | Select-Object -First 2) -join ' | ')
    1..3 | ForEach-Object { & $Magick -size 1800x1200 "gradient:#335588-#ddccaa" -rotate ($_ * 10) -gravity center -crop 1800x1200+0+0 +repage "in\img$_.jpg" }
    & $Magick mogrify -path out -resize 3840x -gravity center -crop 3840x2160+0+0 +repage -quality 92 'in\*.jpg'
    Pass 'magick mogrify with wildcard' ((Get-ChildItem out\*.jpg).Count -eq 3) ((Get-ChildItem out\*.jpg).Name -join ',')
    Copy-Item out\*.jpg photos_16x9\
    $lines = Get-ChildItem photos_16x9\*.jpg | ForEach-Object { & $Magick identify -format '%f %wx%h\n' $_.FullName }
    Say ($lines -join ' ; ')
    Pass 'Exercise 1 self-check (all 3840x2160)' ((($lines | Where-Object { $_ -match '3840x2160' }).Count) -eq 3) ''
}

# ---------------------------------------------------------------- 3. ffmpeg (R1, R9, Exercises 2 and 10)
Section '3. ffmpeg: R9 four commands, R1 Ken Burns, Exercise 2 and Exercise 10 checks'
Try-Run 'ffmpeg' {
    Say ((& $Ffmpeg -version 2>&1 | Select-Object -First 1) -join ' ')
    & $Ffmpeg -v error -y -f lavfi -i "testsrc2=size=1920x1080:rate=25:duration=5" -f lavfi -i "sine=frequency=440:sample_rate=48000:duration=5" -c:v ffv1 -c:a pcm_s24le master.mov
    & $Ffmpeg -v error -y -i master.mov -c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart deliver_usb.mp4
    & $Ffmpeg -v error -y -i master.mov -c:v libx264 -preset slow -crf 20 -maxrate 12M -bufsize 24M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart web_1080.mp4
    & $Ffmpeg -v error -y -i master.mov -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le -c:a pcm_s24le archive_prores422hq.mov
    & $Ffmpeg -v error -y -i master.mov -c:v ffv1 -level 3 -coder 1 -context 1 -g 1 -slicecrc 1 -c:a flac archive_ffv1.mkv
    foreach ($f in 'deliver_usb.mp4','web_1080.mp4','archive_prores422hq.mov','archive_ffv1.mkv') {
        $probe = (& $Ffprobe -v error -show_entries "stream=codec_name,profile,level,pix_fmt,width,height,sample_rate,channels" -of "default=nw=1" $f 2>&1) -join ' '
        Pass "R9 $f" (Test-Path $f) $probe
    }
    # R1: Ken Burns push-in, pan, dissolve (photoA/photoB are synthetic)
    Copy-Item 'photos_16x9\img1.jpg' photoA.jpg; Copy-Item 'photos_16x9\img2.jpg' photoB.jpg
    & $Ffmpeg -v error -y -loop 1 -i photoA.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z='min(1+0.0008*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 kbA.mp4
    & $Ffmpeg -v error -y -loop 1 -i photoB.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z=1.15:x='(iw-iw/zoom)*on/124':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 panB.mp4
    & $Ffmpeg -v error -y -i kbA.mp4 -i panB.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p out_kb.mp4
    $ex2 = (& $Ffprobe -v error -show_entries "stream=width,height,r_frame_rate,codec_name" -of csv=p=0 out_kb.mp4 2>&1) -join ' '
    Pass 'Exercise 2 self-check (1920x1080, 25 fps, h264)' ($ex2 -match 'h264,1920,1080,25/1') $ex2
    # Exercise 10: SHA256SUMS write and verify (PowerShell form from the playbook)
    Copy-Item deliver_usb.mp4 chapter_usb.mp4; Copy-Item web_1080.mp4 chapter_web_1080.mp4; Copy-Item archive_prores422hq.mov chapter_archive.mov
    Get-ChildItem chapter_usb.mp4, chapter_web_1080.mp4, chapter_archive.mov | ForEach-Object { '{0}  {1}' -f (Get-FileHash $_.Name -Algorithm SHA256).Hash.ToLower(), $_.Name } | Set-Content SHA256SUMS -Encoding ascii
    $ver = Get-Content SHA256SUMS | ForEach-Object { $h, $f = $_ -split '\s+', 2; if ((Get-FileHash $f -Algorithm SHA256).Hash -eq $h.ToUpper()) { "OK   $f" } else { "FAIL $f" } }
    Pass 'Exercise 10 self-check (3 files verify)' ((($ver | Where-Object { $_ -like 'OK*' }).Count) -eq 3) ($ver -join ' ; ')
    # Git Bash users: does sha256sum -c accept the CRLF file PowerShell wrote?
    if (Has 'sha256sum') { $r = (& sha256sum -c SHA256SUMS 2>&1) -join ' ; '; Say ("sha256sum -c on the PowerShell-written file: " + $r) }
}

# ---------------------------------------------------------------- 4. Inkscape (R3, Exercise 6)
Section '4. Inkscape: command-line PNG export (R3 replacement for rsvg-convert)'
if ($Inkscape) {
    Try-Run 'inkscape' {
        Say ((& $Inkscape --version 2>&1 | Select-Object -First 1) -join ' ')
        Set-Content -Path route.svg -Encoding ascii -Value '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="#f3ead8"/><path d="M200 800 C 600 200, 1000 1000, 1700 300" fill="none" stroke="#cc3333" stroke-width="18" stroke-linecap="round"/></svg>'
        $t = Measure-Command { & $Inkscape --export-type=png --export-width=1280 --export-filename=route_ink.png route.svg 2>&1 | Out-Null }
        $d = if (Test-Path route_ink.png) { (& $Magick identify -format '%wx%h' route_ink.png) } else { 'missing' }
        Pass 'inkscape --export-type=png' ($d -eq '1280x720') ("size $d; seconds " + [math]::Round($t.TotalSeconds, 1))
        Say ('Which exe answered: ' + (Get-Command $Inkscape).Source + ' (inkscape.com is the console wrapper; inkscape.exe prints nothing in a console)')
    }
} else { Say 'SKIPPED: Inkscape not found (give -Inkscape path to bin\inkscape.com)' }
Section '4b. rsvg-convert on Windows? and the two replacements (frame loop of Exercise 6)'
Say ("rsvg-convert on PATH: " + (Has 'rsvg-convert'))
Try-Run 'svg frames' {
    $L = 912.37; $n = 12
    for ($i = 0; $i -lt $n; $i++) {
        $f = $i / ($n - 1); $e = $f * $f * (3 - 2 * $f); $off = '{0:N2}' -f ($L * (1 - $e))
        $svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 640 360"><rect width="640" height="360" fill="#f7f1e3"/><path d="M 60 300 C 140 80, 240 80, 300 200 S 460 330, 580 60" fill="none" stroke="#222" stroke-width="6" stroke-linecap="round" stroke-dasharray="912.37 912.37" stroke-dashoffset="' + $off + '"/></svg>'
        Set-Content -Path ('frames\f_{0:D4}.svg' -f $i) -Value $svg -Encoding ascii
    }
    $t = Measure-Command { & $Magick mogrify -format png -density 96 'frames\f_*.svg' }
    Pass 'ImageMagick built-in SVG renderer (12 frames)' ((Get-ChildItem frames\*.png).Count -eq $n) ("seconds " + [math]::Round($t.TotalSeconds, 1))
    if ($Inkscape) {
        Remove-Item frames\*.png
        $files = (Get-ChildItem frames\f_*.svg).FullName
        $t = Measure-Command { & $Inkscape --export-type=png --export-width=1280 $files 2>&1 | Out-Null }
        Pass 'Inkscape one process, many files (12 frames)' ((Get-ChildItem frames\*.png).Count -eq $n) ("seconds " + [math]::Round($t.TotalSeconds, 1))
    }
    if (Has 'rsvg-convert') { Remove-Item frames\*.png; Get-ChildItem frames\f_*.svg | ForEach-Object { $png = $_.FullName -replace '\.svg$', '.png'; rsvg-convert -w 1280 $_.FullName -o $png }; Pass 'rsvg-convert frame loop (Exercise 6)' ((Get-ChildItem frames\*.png).Count -eq $n) '' }
}

# ---------------------------------------------------------------- 5. GIMP batch
Section '5. GIMP 3.2: batch from the command line (Script-Fu route; Python-fu route)'
if ($Gimp) {
    Try-Run 'gimp' {
        Say ((& $Gimp --version 2>&1 | Select-Object -First 1) -join ' ')
        $in  = ((Resolve-Path 'in\img1.jpg').Path -replace '\\', '/')
        $out = ((Join-Path (Get-Location).Path 'gimp_sf.png') -replace '\\', '/')
        $scm = "(let* ((image (car (gimp-file-load RUN-NONINTERACTIVE `"$in`")))) (gimp-image-scale image 1280 853) (gimp-file-save RUN-NONINTERACTIVE image `"$out`") (gimp-image-delete image))`n(gimp-quit 0)`n"
        Set-Content -Path batch.scm -Value $scm -Encoding ascii
        $t = Measure-Command { Get-Content batch.scm | & $Gimp -i -d -f -s --batch-interpreter=plug-in-script-fu-eval -b - 2>&1 | Out-Null }
        $d = if (Test-Path gimp_sf.png) { (& $Magick identify -format '%wx%h' gimp_sf.png) } else { 'missing' }
        Pass 'GIMP Script-Fu batch' ($d -eq '1280x853') ("size $d; seconds " + [math]::Round($t.TotalSeconds, 1))
        $py = "import gi`ngi.require_version('Gimp', '3.0')`nfrom gi.repository import Gimp, Gio`nimg = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, Gio.File.new_for_path('$in'))`nimg.scale(640, 427)`nGimp.file_save(Gimp.RunMode.NONINTERACTIVE, img, Gio.File.new_for_path('" + (($out) -replace 'gimp_sf', 'gimp_py') + "'), None)`nimg.delete()`n"
        Set-Content -Path batch.py -Value $py -Encoding ascii
        Get-Content batch.py | & $Gimp -i -d -f -s --batch-interpreter=python-fu-eval -b - --quit 2>&1 | Out-Null
        Pass 'GIMP Python-fu batch' (Test-Path gimp_py.png) 'under Wine this failed with a Python stdio error; on Windows it may work'
    }
} else { Say 'SKIPPED: GIMP not found (give -Gimp path to bin\gimp-console-3.2.exe)' }

# ---------------------------------------------------------------- 6. melt.exe (F1 command)
Section '6. melt.exe: the F1 story.mlt command'
Try-Run 'melt' {
    if ((Has $Melt) -or (Test-Path $Melt)) {
        Say ((& $Melt --version 2>&1 | Select-Object -First 1) -join ' ')
        if (Test-Path $StoryMlt) { Copy-Item $StoryMlt (Join-Path (Get-Location).Path 'story.mlt') } else { Say "WARNING: $StoryMlt not found; copy r5_story.mlt next to this script" }
        if (Test-Path story.mlt) {
            $t = Measure-Command { & $Melt story.mlt -silent -profile atsc_1080p_25 -consumer avformat:story.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p an=1 2>&1 | Out-Null }
            $pr = (& $Ffprobe -v error -show_entries "stream=codec_name,width,height,r_frame_rate,nb_frames" -of "default=nw=1" story.mp4 2>&1) -join ' '
            Pass 'melt story.mlt' ($pr -match 'width=1920' -and $pr -match 'nb_frames=200') ($pr + "; seconds " + [math]::Round($t.TotalSeconds, 1))
        }
    } else { Say 'SKIPPED: melt not found (give -Melt path, for example Kdenlive bin\melt.exe)' }
}

# ---------------------------------------------------------------- 7. Blender R2 timings (the two r2_param.py runs)
Section '7. Blender: r2_param.py at 640x360 and 1920x1080 (time per frame, peak working set)'
if (-not $Blender -and (Has 'blender')) { $Blender = 'blender' }
if ($Blender -and ((Has $Blender) -or (Test-Path $Blender)) -and (Test-Path $R2Param)) {
    Try-Run 'blender' {
        $r2 = (Resolve-Path $R2Param).Path
        New-Item -ItemType Directory -Force -Path layers | Out-Null
        & $Magick -size 4000x2250 "gradient:#ffd9a0-#6a8fb5" layers\bg.png
        & $Magick -size 4000x2250 xc:none -fill "#3a5a3a" -draw "ellipse 2000,1700 1800,500 0,360" layers\mid.png
        & $Magick -size 4000x2250 xc:none -fill "#552211" -draw "rectangle 0,1700 4000,2250" layers\fg.png
        $bver = (& $Blender --version 2>&1 | Select-Object -First 1) -join ' '
        Say "Blender: $bver"
        foreach ($case in @(@(640, 360, 'r640'), @(1920, 1080, 'r1080'))) {
            $env:R2_DIR = (Get-Location).Path; $env:R2_NF = '10'; $env:R2_SPP = '4'; $env:R2_LAYERS = 'layers'
            $env:R2_RX = [string]$case[0]; $env:R2_RY = [string]$case[1]; $env:R2_OUT = $case[2]
            New-Item -ItemType Directory -Force -Path $case[2] | Out-Null
            $stdout = Join-Path (Get-Location).Path ($case[2] + '.log')
            $p = Start-Process -FilePath $Blender -ArgumentList @('-b','--factory-startup','-noaudio','--python-exit-code','3','-P',$r2) -PassThru -NoNewWindow -RedirectStandardOutput $stdout
            $peak = 0
            while (-not $p.HasExited) { try { $p.Refresh(); if ($p.PeakWorkingSet64 -gt $peak) { $peak = $p.PeakWorkingSet64 } } catch {}; Start-Sleep -Milliseconds 250 }
            $line = (Select-String -Path $stdout -Pattern 'R2_RESULT' | Select-Object -Last 1).Line
            Say ("RESULT " + $case[0] + "x" + $case[1] + ": exit " + $p.ExitCode + "; peak working set MB " + [math]::Round($peak / 1MB) + "; " + $line)
        }
    }
} else { Say 'SKIPPED: Blender or r2_param.py not found (give -Blender path to blender.exe; keep r2_param.py beside this script)' }

# ---------------------------------------------------------------- 8. Git Bash (only if installed)
Section '8. Git Bash: argument conversion check (only if bash.exe exists)'
$bash = First-Existing @("$env:ProgramFiles\Git\bin\bash.exe", "${env:ProgramFiles(x86)}\Git\bin\bash.exe")
if ($bash) {
    Try-Run 'git bash' {
        Say ((& $bash --version 2>&1 | Select-Object -First 1) -join ' ')
        $cmd = "cd '" + ((Get-Location).Path -replace '\\', '/') + "' && '" + ($Ffmpeg -replace '\\', '/') + "' -v error -y -i master.mov -vf scale=640:360 -frames:v 1 gb_test.png && echo GITBASH_FFMPEG_OK"
        Say ((& $bash -lc $cmd 2>&1) -join ' ')
        if ($Melt -and (Test-Path $Melt) -and (Test-Path story.mlt)) {
            $cmd2 = "cd '" + ((Get-Location).Path -replace '\\', '/') + "' && MSYS2_ARG_CONV_EXCL='*' '" + ($Melt -replace '\\', '/') + "' story.mlt -silent -profile atsc_1080p_25 -consumer avformat:story_gb.mp4 vcodec=libx264 crf=20 pix_fmt=yuv420p an=1 && echo GITBASH_MELT_OK"
            Say ((& $bash -lc $cmd2 2>&1) -join ' ')
        }
    }
} else { Say 'Git Bash not found (fine; PowerShell is the lean).' }

# ---------------------------------------------------------------- 9. things only a person can read (print reminders into the report)
Section '9. By hand (write these in the report)'
Say 'A. DaVinci Resolve 21 Free: Preferences > System > General: is "External scripting using" missing, greyed out or present? (the manual says Studio only)'
Say 'B. Resolve installer Read Me / system requirements: copy the minimum RAM, GPU and OS lines here.'
Say 'C. Resolve: add a subtitle track, import an .srt, render with Burn into video: did it work on Free? Any watermark or message?'
Say 'D. Suno account page: downloads left this month, plan name, and whether free-tier downloads are offered.'
Say 'E. Zapsplat licence page and Musopen terms: paste the lines about public screening, attribution and commercial use.'
Say 'F. Venue: run the venue test kit (make_venue_test_kit.py) on the real screen and note the answers.'
Set-Location $here
Say ''
Say ("finished " + (Get-Date -Format 's') + ". Paste this whole file back.")
