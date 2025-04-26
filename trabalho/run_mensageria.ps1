Write-Output "Iniciando o servidor..."
Start-Process powershell -ArgumentList "trabalho/server.py"

Start-Sleep -Seconds 2

Write-Output "Iniciando cliente 1..."
Start-Process powershell -ArgumentList "trabalho/client.py"

Start-Sleep -Seconds 1

Write-Output "Iniciando cliente 2..."
Start-Process powershell -ArgumentList "trabalho/client.py"

Start-Sleep -Seconds 1

Write-Output "Iniciando cliente 3..."
Start-Process powershell -ArgumentList "trabalho/client.py"
