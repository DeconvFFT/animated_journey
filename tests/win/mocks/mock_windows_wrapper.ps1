<#
  mock_windows_wrapper.ps1  (TEST ONLY, WP-01a)
  Runs win\step0_pc_tests.ps1 as if it were on Windows, with INVENTED answers for the Windows-only cmdlets, so the
  Windows branches of the script (adapter list, nvidia-smi merge, registry memory, drives, screen, accounts, Craft scan)
  can be exercised on Linux with pwsh. It proves the script's own logic; it does NOT prove how real Windows answers
  (that stays UNVERIFIED until the maker's first run).
  Every name and number below is made up.
#>
param(
    [Parameter(Mandatory = $true)][string]$Script,
    [Parameter(Mandatory = $true)][string]$Out,
    [string]$ToolsRoot = '',
    [string]$Scenario = 'nvidia'
)

$env:OS = 'Windows_NT'
$global:LJMockScenario = $Scenario

function Get-CimInstance {
    param([string]$ClassName, [string]$Filter, $ErrorAction)
    switch ($ClassName) {
        'Win32_OperatingSystem' { [pscustomobject]@{ Caption = 'Microsoft Windows 11 Pro'; Version = '10.0.22631'; BuildNumber = '22631'; OSArchitecture = '64-bit' } }
        'Win32_Processor' {
            if ($global:LJMockScenario -eq 'steperror') { throw ("Access to the path '" + 'C:' + [char]92 + 'Users' + [char]92 + 'tamsinwrex' + [char]92 + "x' is denied for tamsinwrex on BRAMBLE-Q7") }
            if ($global:LJMockScenario -eq 'note_cpu') { [pscustomobject]@{ Name = 'Fakeco tamsinwrex 9000'; NumberOfCores = 6; NumberOfLogicalProcessors = 12 }; return }
            [pscustomobject]@{ Name = '  Fakeco  Model  9000   Processor '; NumberOfCores = 6; NumberOfLogicalProcessors = 12 }
        }
        'Win32_ComputerSystem' { [pscustomobject]@{ TotalPhysicalMemory = [uint64]17083908096 } }
        'Win32_VideoController' {
            switch ($global:LJMockScenario) {
                'nvidia' {
                    [pscustomobject]@{ Name = 'NVIDIA GeForce RTX 3060'; AdapterCompatibility = 'NVIDIA'; DriverVersion = '31.0.15.5222'; AdapterRAM = [uint32]4293918720; CurrentHorizontalResolution = 2560; CurrentVerticalResolution = 1440; CurrentRefreshRate = 144 }
                    [pscustomobject]@{ Name = 'Fakeco Integrated Graphics'; AdapterCompatibility = 'Intel Corporation'; DriverVersion = '31.0.101.4502'; AdapterRAM = [uint32]1073741824; CurrentHorizontalResolution = $null; CurrentVerticalResolution = $null; CurrentRefreshRate = $null }
                }
                'amd_registry' {
                    [pscustomobject]@{ Name = 'AMD Radeon RX 6800 XT'; AdapterCompatibility = 'Advanced Micro Devices, Inc.'; DriverVersion = '31.0.21921.1000'; AdapterRAM = [uint32]4293918720; CurrentHorizontalResolution = 1920; CurrentVerticalResolution = 1080; CurrentRefreshRate = 60 }
                    [pscustomobject]@{ Name = 'AMD Radeon RX 550'; AdapterCompatibility = 'Advanced Micro Devices, Inc.'; DriverVersion = '31.0.21921.1000'; AdapterRAM = [uint32]4294967295; CurrentHorizontalResolution = $null; CurrentVerticalResolution = $null; CurrentRefreshRate = $null }
                }
                'capped_only' {
                    [pscustomobject]@{ Name = 'NVIDIA GeForce RTX 3070'; AdapterCompatibility = 'NVIDIA'; DriverVersion = '31.0.15.5222'; AdapterRAM = [uint32]4294967295; CurrentHorizontalResolution = 1920; CurrentVerticalResolution = 1080; CurrentRefreshRate = 60 }
                }
                { $_ -in @('software', 'steperror', 'leak_fs', 'note_cpu', 'deny_word') } {
                    [pscustomobject]@{ Name = 'Microsoft Basic Render Driver'; AdapterCompatibility = 'Microsoft Corporation'; DriverVersion = '10.0.22621.3672'; AdapterRAM = [uint32]0; CurrentHorizontalResolution = 1280; CurrentVerticalResolution = 720; CurrentRefreshRate = 60 }
                }
            }
        }
        'Win32_LogicalDisk' {
            $fsName = 'NTFS'
            if ($global:LJMockScenario -eq 'leak_fs') { $fsName = 'NTFS-tamsinwrex' }
            if ($global:LJMockScenario -eq 'deny_word') { $fsName = 'NTFS-zorbax' }
            [pscustomobject]@{ DeviceID = 'C:'; DriveType = 3; FileSystem = $fsName; Size = [uint64]511999999488; FreeSpace = [uint64]214748364800 }
            [pscustomobject]@{ DeviceID = 'D:'; DriveType = 2; FileSystem = 'exFAT'; Size = [uint64]1000204886016; FreeSpace = [uint64]999000000000 }
            [pscustomobject]@{ DeviceID = 'E:'; DriveType = 4; FileSystem = 'NTFS'; Size = [uint64]999999999999; FreeSpace = [uint64]5 }
            [pscustomobject]@{ DeviceID = 'F:'; DriveType = 5; FileSystem = $null; Size = $null; FreeSpace = $null }
            [pscustomobject]@{ DeviceID = 'G:'; DriveType = 3; FileSystem = $null; Size = $null; FreeSpace = $null }
        }
        'Win32_UserAccount' { 1..3 | ForEach-Object { [pscustomobject]@{ Name = 'fakeaccount' + $_ } } }
        default { throw ('mock has no answer for ' + $ClassName) }
    }
}

function Get-LocalUser {
    param($ErrorAction)
    if ($global:LJMockScenario -eq 'nvidia') {
        [pscustomobject]@{ Name = 'a'; Enabled = $true }
        [pscustomobject]@{ Name = 'b'; Enabled = $true }
        [pscustomobject]@{ Name = 'c'; Enabled = $false }
    } else {
        throw 'the accounts module is not available in this mock'
    }
}

function Get-ItemProperty {
    param([string]$Path, $ErrorAction)
    if ($Path -eq 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion') { return [pscustomobject]@{ EditionID = 'Professional'; UBR = 4317 } }
    if ($Path -eq 'HKCU:\Control Panel\Desktop\WindowMetrics') { return [pscustomobject]@{ AppliedDPI = 144 } }
    if ($Path -eq 'FAKE:0000') { return [pscustomobject]@{ DriverDesc = 'AMD Radeon RX 6800 XT'; 'HardwareInformation.qwMemorySize' = [int64]17163091968 } }
    if ($Path -eq 'FAKE:0001') { return [pscustomobject]@{ DriverDesc = 'AMD Radeon RX 550'; 'HardwareInformation.qwMemorySize' = [byte[]](0, 0, 0, 0, 2, 0, 0, 0) } }
    if ($Path -eq 'FAKE:Configuration') { return [pscustomobject]@{ Other = 1 } }
    Microsoft.PowerShell.Management\Get-ItemProperty @PSBoundParameters
}

function Get-ChildItem {
    $a = $args
    if ($a.Count -ge 2 -and "$($a[0])" -eq '-Path' -and "$($a[1])".StartsWith('HKLM:')) {
        foreach ($n in @('0000', '0001', 'Configuration')) { [pscustomobject]@{ PSChildName = $n; PSPath = ('FAKE:' + $n) } }
        return
    }
    Microsoft.PowerShell.Management\Get-ChildItem @a
}

function Add-Type { }

& $Script -Out $Out -ToolsRoot $ToolsRoot
exit $LASTEXITCODE
