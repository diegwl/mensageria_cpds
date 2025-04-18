Write-Output "Iniciando o servidor..."
Start-Process powershell -ArgumentList "python mensageria_distribuida/server.py"

Start-Sleep -Seconds 2

Write-Output "Iniciando cliente 1..."
Start-Process powershell -ArgumentList "python mensageria_distribuida/client.py"

Start-Sleep -Seconds 1

Write-Output "Iniciando cliente 2..."
Start-Process powershell -ArgumentList "python mensageria_distribuida/client.py"

Start-Sleep -Seconds 1

Write-Output "Iniciando cliente 3..."
Start-Process powershell -ArgumentList "python mensageria_distribuida/client.py"
