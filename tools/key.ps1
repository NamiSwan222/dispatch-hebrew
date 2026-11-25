# Focus a process's window and press keys: key.ps1 <processName> <vk hex,vk hex,...> [delayMs]
param([string]$Name, [string]$Keys, [int]$Delay = 400)
Add-Type @"
using System; using System.Runtime.InteropServices;
public class K { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte sc, uint f, UIntPtr x);
[DllImport("user32.dll")] public static extern uint MapVirtualKey(uint c, uint t); }
"@
$p = Get-Process $Name | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[K]::SetForegroundWindow($p.MainWindowHandle) | Out-Null; Start-Sleep -Milliseconds 300
foreach ($k in $Keys.Split(',')) { $vk = [Convert]::ToByte($k, 16); $sc = [byte][K]::MapVirtualKey($vk, 0)
  [K]::keybd_event($vk, $sc, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 60
  [K]::keybd_event($vk, $sc, 2, [UIntPtr]::Zero); Start-Sleep -Milliseconds $Delay }
