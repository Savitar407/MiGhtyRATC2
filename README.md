# MiGhtyRATC2
WARNING DO NOT USE FOR ILLEGAL PURPOSES, RESEARCH ONLY, I TAKE NO RESPONSIBILITY FOR ANYTHING DONE WITH THIS TOOL

MiGhtyRATC2 is a rudementary custom C2 protocol and a client / server model to test antivirus / EDR by obfuscating a "beacon" written in powershell and 
obfuscated with Chimera, Chimera is a great obfuscator so go checkout their github here: https://github.com/tokyoneon/Chimera

NOTE - this program must be installed in /root to work properly.

Usage:

1.  ./MiGhtyRATC2.py
2.  specify the PAYLOAD lhost/lport which is the ip / port that any payload that requires another socket connection will use, currently MiGhtyRAT only 
supports a reverse shell so PAYLOAD lhost/lport is the reverse shell ip / port it will connect back to
3. BEACON lhost/lport is the ip / port that the beacon will use for its C2 channel with the C2 server. Theese two values are configured to be seperate 
in case you want your reverse shell going to a differrent server than your beacon's C2 communications

5. MiGhtyRATC2 will now generate an obfuscated beacon to test antivirus, this beacon is saved to /root/MiGhtyRATC2/Output and is called Final_Beacon.ps1
either copy / past the beacon into a powershell terminal or copy the file over to the test vm and run it my right clicking and selecting 
"run with powershell", if everything has worked properly and the beacon sends "Hello" down its C2 socket connection you will see the 
MiGhtyRATC2 terminal which is :

MiGhtyRATC2> 

if you see the above that means your beacon has successufully made its connection with your C2 server to test antivirus behavioral analysis. 

You can test if av will catch a reverse shell by starting a listener by typing "nc -nlvp 4444" into your kali linux terminal and typing "shell" into the 
MiGhtyRATC2 terminal, MiGhtyRATC2 will send its C2 command down the socket to the beacon telling it to establish a reverse shell on the test vm. 

You can test if antivirus will catch downloads by entering "install:persistence" which will initiate apache2 web server and send the command down to the 
beacon to download Final_Beacon.ps1 and persistenceB.bat from the C2 server. Theese files will be saved to C:\Users\Public and a registry run key is set 
in HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run for the batch file and the beacon will launch at the next system startup

you can also test antivirus with an open source github based keylogger by entering: "install:keylogger" which does the same thing as "install:persistence"
except it will download a keylogger and its associated persistent batch file and modify the registry to run at system startup. 

If you want to test other files you can use the command "install:<filename>" and if the specified file is in /var/www/html the beacon will download it
to C:\Users\public on your test vm.
  
THIS IS TO BE USED FOR RESEARCH PURPOSES ONLY, I TAKE NO RESPOLSIBILITY FOR ILLEGAL ACTIONS PERFORMED WITH THIS TOOL, I only create theese types of tools
  for learning about cyber security.

