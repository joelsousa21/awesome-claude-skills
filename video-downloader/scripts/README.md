$python = "C:/Users/joel/AppData/Local/Programs/Python/Python314/python.exe"
$script = "c:/DEV Project/awesome-claude-skills/video-downloader/scripts/download_video.py"
$output = "C:/DEV Project/awesome-claude-skills/downloads"

$urls = @(
    "https://youtu.be/rozsLFU75mY"
    "https://youtu.be/tn38pz1XMCU"
    "https://youtu.be/_NBiwpbauRI"
    "https://youtu.be/Ct9CbofH2J8"
    "https://youtu.be/zQQ5_f1BqhE"
    "https://youtu.be/y88MAEu_V0k"
    "https://youtu.be/WRLO0KyfU7U"
    "https://youtu.be/KylRDp4wsmI"
    "https://youtu.be/vZQwZyJuBiM"
    "https://youtube.com/shorts/WM_dsQyexBc"
    "https://youtu.be/DaZu9fvxkik"
    "https://youtu.be/rDEM490GaZ0"
    "https://youtu.be/802q_4HxWiw"
    "https://youtu.be/_mg2yl70f5I"
    "https://youtu.be/W3CUb8_rDm0"
    "https://youtu.be/J1Odf6qxqpY"
    "https://youtu.be/3ZNj-rZIIR4"
    "https://youtu.be/yHRwuG7wsKI"
    "https://youtu.be/G3rU_-ftIhI"
    "https://youtu.be/lti33jwtI0I"
    "https://youtu.be/T-4KTd3PpLM"
    "https://youtu.be/9EamfbLwlCw"
    "https://youtu.be/zci1RbLDyno"
    "https://youtu.be/a0Nmp9Ze91w"
    "https://youtu.be/BRHOuNYPsWE"
    "https://youtu.be/i3Ur0Qt_XdM"
    "https://youtu.be/0MghXqxONyo"
)

$total = $urls.Count
$i = 1
foreach ($url in $urls) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "[$i/$total] Baixando: $url" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Cyan
    & $python $script -a -o $output $url
    $i++
}

Write-Host "`n✅ Todos os $total downloads concluídos!" -ForegroundColor Green