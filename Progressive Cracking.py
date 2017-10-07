#!/usr/bin/env python3

import os , math , threading , time

class Main():
	handshake = ''
	handshakeEscaped = ''
	wordlist = ''
	directory = ''
	directoryEscaped = ''
	fileSize = 100000
	keyFound = False
	key = ''
	timeToQuit = False
	totalNumOfFiles = 0
	startTime = 0
	endTime = 0
	beginTime = time.time()
	averageTime = 0
	quittingThread = None

	def startupPrep():
		alreadyStarted = input('Do you wish to start cracking a handshake from the beginning? (Y/n)\t')

		if ((alreadyStarted == 'Y') or (alreadyStarted == 'y')):
			print('\nNote: Do NOT escape spaces in directories.\n')
			Main.handshake = input('Please enter the location of the handshake:\t')
			Main.wordlist = input('Please enter the location of the wordlist:\t')
			Main.directory = input('\nWe will now break-up the wordlist for efficiency, and store all\nof the sub-wordlist files in a new directory.\n\nPlease enter the location of a NEW directory, which we will create to store these files:\t')
			Main.fileSize = input('\nPlease enter 1, 2, or 3, to indicate the speed of the current system:\n1 = Standard (Laptops)\n2 = Powerful (Gaming PCs)\n3 = Extremely Powerful (Multiple High-End CPUs/GPUs)\nNumber:\t')

			try:
				Main.fileSize = int(Main.fileSize)

				if (Main.fileSize == 1):
					Main.fileSize = 100000
				elif (Main.fileSize == 2):
					Main.fileSize = 350000
				elif (Main.fileSize == 3):
					Main.fileSize = 1000000
				else:
					print('\n\nInvalid Input, Please Try Again!')
					Main.startupPrep()
			except:
				print('\n\nInvalid Input, Please Try Again!')
				Main.startupPrep()

			if (Main.directory[(len(Main.directory) - 1)] != '/'):
				Main.directory += '/'


			os.system('clear')

			for chr in Main.directory:
				if (chr == ' '):
					Main.directoryEscaped += '\ '
				else:
					Main.directoryEscaped += chr

			for chr in Main.handshake:
				if (chr == ' '):
					Main.handshakeEscaped += '\ '
				else:
					Main.handshakeEscaped += chr

			command = ('sudo mkdir -p ' + Main.directoryEscaped)
			os.system(command)


			wordlistFile = open(Main.wordlist , 'r')
			words = 0
			wordString = ''
			filename = 0
			counter = 1
			counterNonstop = 1

			print('Please wait while we calculate the size of the wordlist...\n')

			for line in wordlistFile:
				words += 1

			print('This wordlist contains' , words , 'words.\n')

			print('Now, please wait while we breakup the wordlist into more-manageable chunks...\n')

			wordlistFile.close()
			wordlistFile = open(Main.wordlist , 'r')

			for line in wordlistFile:
				wordString += line

				if (counter >= Main.fileSize):
					os.system('clear')
					print((math.ceil(((counterNonstop / words) * 100000)) / 1000) , '% Done Generating Files...\n')

					filenameString = (Main.directory + str(filename) + '.txt')
					filename += 1

					file = open(filenameString , 'w')
					file.write(wordString)
					file.close()

					counter = 1
					wordString = ''
					counterNonstop += 1
				else:
					counter += 1
					counterNonstop += 1

			filenameString = (Main.directory + str(filename) + '.txt')
			filename += 1
			file = open(filenameString , 'w')
			file.write(wordString)
			file.close()

			counter = 1
			wordString = ''

			os.system('clear')

			command = ('ls -l ' + Main.directoryEscaped + ' > files.txt')
			os.system(command)

			filesFile = open('files.txt' , 'r')

			for line in filesFile:
				if ('total' in line):
					continue

				filenameForLargest = ''
				for chr in line:
					if (chr == ' '):
						filenameForLargest = ''
					else:
						filenameForLargest += chr

				tempFileName = ''
				for chr in filenameForLargest:
					if (chr == '.'):
						break
					else:
						tempFileName += chr

				filenameForLargest = tempFileName

				if ((int(filenameForLargest) > Main.totalNumOfFiles)):
					Main.totalNumOfFiles = int(filenameForLargest)

			filesFile.close()
			os.system('sudo rm files.txt')



		elif ((alreadyStarted == 'N') or (alreadyStarted == 'n')):
			print('\nNote: Do NOT escape spaces in directories.\n')
			Main.handshake = input('Please enter the location of the handshake:\t')
			Main.directory = input('Please enter the location of the directory containing the wordlist files (generated on the first run):\t')

			if (Main.directory[(len(Main.directory) - 1)] != '/'):
				Main.directory += '/'

			os.system('clear')


			for chr in Main.directory:
				if (chr == ' '):
					Main.directoryEscaped += '\ '
				else:
					Main.directoryEscaped += chr

			for chr in Main.handshake:
				if (chr == ' '):
					Main.handshakeEscaped += '\ '
				else:
					Main.handshakeEscaped += chr


			command = ('ls -l ' + Main.directoryEscaped + ' > files.txt')
			os.system(command)

			filesFile = open('files.txt' , 'r')

			for line in filesFile:
				if ('total' in line):
					continue
				filenameForLargest = ''
				for chr in line:
					if (chr == ' '):
						filenameForLargest = ''
					else:
						filenameForLargest += chr

				tempFileName = ''
				for chr in filenameForLargest:
					if (chr == '.'):
						break
					else:
						tempFileName += chr

				filenameForLargest = tempFileName

				if ((int(filenameForLargest) > Main.totalNumOfFiles)):
					Main.totalNumOfFiles = int(filenameForLargest)

			filesFile.close()
			os.system('sudo rm files.txt')


		else:
			print('Unrecognized input.\n')
			Main.startupPrep()


		Main.beginTime = time.time()

	def controlCenter():
		counter = 0
		firstFileFound = False
		tolerance = 0

		time.sleep(1)
		Main.quittingThread = threading.Thread(target = Main.checkForQuit , args = ())
		Main.quittingThread.start()

		while True:
			if ((Main.keyFound) or (Main.timeToQuit)):
				break

			while True:
				filepath = (Main.directory + str(counter) + '.txt')
				filepathEscaped = (Main.directoryEscaped + str(counter) + '.txt')

				if os.path.isfile(filepath):
					counter += 1
					firstFileFound = True
					break
				else:
					if (firstFileFound):
						if (tolerance >= 100000):
							Main.timeToQuit = True
							os.system('clear')
							print('NO KEY WAS FOUND.')
							while True:
								deleteParentDirect = input('\n\nWould you like to delete the directory that contained the wordlist files?\n(Y/n):\t')
								if ((deleteParentDirect == 'Y') or (deleteParentDirect == 'y')):
									command = ('sudo rm -rf ' + Main.directoryEscaped)
									os.system(command)
									break
								elif ((deleteParentDirect == 'N') or (deleteParentDirect == 'n')):
									break
								else:
									print('INVALID INPUT!')
									continue

							print('\n\nPlease press q and hit enter, to exit.')
							break
						else:
							tolerance += 1
					counter += 1

			if ((Main.keyFound) or (Main.timeToQuit)):
				break


			Main.endTime = time.time()

			print('Starting to check:\t' , filepath)

			if (Main.totalNumOfFiles <= 0):
				Main.totalNumOfFiles = 1

			print((math.ceil(((counter / Main.totalNumOfFiles) * 100000)) / 1000) , '% Done With Entire Wordlist...' , sep = '')
			print('Runtime:\t' , (time.time() - Main.beginTime) , 'Seconds')
			if (not ((Main.startTime == 0) or (Main.endTime == 0))):
				if (Main.averageTime == 0):
					Main.averageTime = 1
				elif (Main.averageTime == 1):
					Main.averageTime = (Main.endTime - Main.startTime)
				else:
					Main.averageTime = (((Main.endTime - Main.startTime) + Main.averageTime) / 2)

				timeRemainingSec = ((Main.averageTime) * (Main.totalNumOfFiles - (counter + 1)))
				timeRemainingMin = math.floor((timeRemainingSec / 60))
				timeRemainingHr = math.floor((timeRemainingMin / 60))
				timeRemainingDay = math.floor((timeRemainingHr / 24))

				timeRemainingSec %= 60
				timeRemainingSec = (math.ceil(timeRemainingSec))
				timeRemainingMin %= 60
				timeRemainingHr %= 24

				if (not((Main.averageTime == 0) or (Main.averageTime == 1))):
					if ((int(time.time() - Main.beginTime)) < 600):
						Main.averageTime = 1
						#This is so that the average will not be messed up: computers are more-efficient in the first ten minutes, before they get hot.
						print('Time Remaining Will Appear Here After 10 Minutes.\n\n')
					else:
						print('Estimated Time Remaining:\t' , timeRemainingDay , 'Day(s)' , timeRemainingHr , ' Hour(s)' , timeRemainingMin , ' Minute(s)' , timeRemainingSec , 'Second(s)' , '\n\n')
				else:
					print('\n')

			else:
				print('\n')

			Main.startTime = time.time()

			Main.crack(filepathEscaped)

			if (Main.keyFound == True):
				print('\n\nPress q and hit enter to exit.\n')
				break


	def crack(filepath):
		command = ('sudo aircrack-ng ' + Main.handshakeEscaped + ' -w ' + filepath + ' > results.txt')
		os.system(command)

		resultsFile = ('results.txt')
		file = open(resultsFile , 'r')

		for line in file:
			if ('KEY FOUND' in line):
				Main.keyFound = True
				Main.key = line

				os.system('clear')

				print('Key Found! The key is between the brackets, in this results line, from aircrack-ng:\n' , Main.key)
				print('\nPlease give us a few minutes to finish all cracking operations, and exit the program correctly. Thanks!')

				file2 = open('KEY.txt' , 'w')
				file2.write(line)
				file2.close()

				break

		file.close()
		command = ('sudo rm ' + resultsFile)
		os.system(command)
		command = ('sudo rm ' + filepath)
		os.system(command)
		if (Main.keyFound):
			while True:
				deleteLeftovers = input('\nWould you like to delete all remaining wordlist files, and their parent directory?\n(This will not delete the original wordlist)\n(Y/n):\t')
				if ((deleteLeftovers == 'Y') or (deleteLeftovers == 'y')):
					command = ('sudo rm -rf ' + Main.directoryEscaped)
					os.system(command)
					break
				elif ((deleteLeftovers == 'N') or (deleteLeftovers == 'n')):
					break
				else:
					print('Invalid Input!\n')
					continue

	def checkForQuit():
		print('\nIf, at any point, you wish to quit, simply type "q" and press enter.\nThen, wait a few minutes, while the program finishes up.\n\n')
		time.sleep(6)

		while True:
			quit = input('')
			if ((quit == 'q') or (quit == 'Q')):
				print('\nQuitting...\n')
				Main.timeToQuit = True
				break


Main.startupPrep()
Main.controlCenter()

Main.quittingThread.join()

print('\n\nProgram has finished! Thanks!')
