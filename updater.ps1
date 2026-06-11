Write-Host "Checking Windows Updates..."

if (-not(Get-Module -ListAvailable -Name PSWindowsUpdate)) {
    Install-Module PSWindowsUpdate -force

}

Import-Module PSWindowsUpdate

Get-WindowsUpdate -Install -AcceptAll -AutoReboot
