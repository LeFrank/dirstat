import sys
import os


if __name__ == "__main__":
	cwd = os.getcwd()
	listOfFiles = os.listdir(cwd)
	# slist  = listOfFiles.sort()
	# print(slist)
	fileCount = 0
	visibleFilesCount = 0
	hiddenFilesCount = 0
	directoryCount = 0
	visibleDirectories = 0
	hiddenDirectories = 0
	symlinkCount = 0
	NumFileTypes = 0
	totalNumberOfObjects = len(listOfFiles)
	# print(listOfFiles)
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFiles:
		# Create full path
		fullPath = os.path.join(cwd, entry)
		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullPath):
			# allFiles = allFiles + getListOfFiles(fullPath)
			directoryCount += 1
		elif os.path.islink(fullPath):
			symlinkCount += 1
		else:
			fileCount += 1
			allFiles.append(fullPath)
	print("Total Objects: %s, Directories: %s, Sym Links: %s, Files: %s" % (totalNumberOfObjects ,directoryCount, symlinkCount, fileCount))
	# print(allFiles)            
	# return allFiles
