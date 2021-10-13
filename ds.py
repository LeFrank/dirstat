import sys
import os
import copy
import math
import time
import datetime
from rich import print, inspect
from rich.console import Console
from rich.table import Table
from rich.progress import track
console = Console()
# print("Hello, [bold blue]Towards Data Science[/bold blue]!", ":thumbs_up:", "[u]By[/u]", "[i]Christopher Tao[/i]")

# import locale
# locale.setlocale(locale.LC_ALL, 'en_US')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)



fileTypeAndCount = []
fileTypeAndCountObj = {"file_extension" : "", "count" : 0, "size": 0}
dirSizeAndCountList = []
dirSizeAndCountObj = {"directory" : "", "child_count" : 0, "size": 0}
totalSizeOfFilesAndFolders = 0
largestFile = {"filename": "" , "file_path" : "", "size" : 0}
smallestFile = {"filename": "" , "file_path" : "", "size" : 0}
file_size_array = []
totalFilesIncludingSubDirectories = 0
oldestFile = {"filename": "" , "file_path" : "", "date" : 0}
youngestFile = {"filename": "" , "file_path" : "", "date" : 0}

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_size(start_path):
    # global oldestFile
    # global youngestFile
    total_size = 0
    total_children = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                try:
                    age = datetime.datetime.fromtimestamp(os.path.getctime(fp))
                    oDate = oldestFile["date"]
                    yDate = youngestFile["date"]
                    # print(age)
                    # print(oDate)
                    if oldestFile["date"] == 0 or age.time() < oDate.time():
                        oldestFile["filename"] = f
                        oldestFile["file_path"] = fp
                        oldestFile["date"] = age
                    if youngestFile["date"] == 0 or age.time() > yDate.time():
                        youngestFile["filename"] = f
                        youngestFile["file_path"] = fp
                        youngestFile["date"] = age
                    fsize = os.path.getsize(fp)
                    if fsize >= largestFile["size"]:
                        largestFile["filename"] = f
                        largestFile["file_path"] = fp
                        largestFile["size"] = fsize
                    total_size += fsize
                    total_children += 1
                except:
                    #print("Skipped")
                    antt = ""

    return [total_size, total_children]

def updateFileTypeCount(fullPath, filename, ext, totalSizeOfFilesAndFolders):
	# global oldestFile
	# global youngestFile
	# print(ext.strip())
	if not bool(ext.strip()):
		extTypeobj = next((item for item in fileTypeAndCount if item["file_extension"] == "None"), "")
	else:
		extTypeobj = next((item for item in fileTypeAndCount if item["file_extension"] == ext), "")
	if len(fileTypeAndCount) == 0:
		obj = copy.deepcopy(fileTypeAndCountObj)
		# print(obj["file_extension"])
		extension = ext
		if not bool(ext.strip()):
			extension = "None"
		obj["file_extension"] = extension
		obj["count"] = 1
		obj["size"] = os.path.getsize(fullPath)
		# if obj["size"] >= largestFile["size"]:
		# 	largestFile["filename"] = filename
		# 	largestFile["file_path"] = fullPath
		# 	largestFile["size"] = obj["size"]
		totalSizeOfFilesAndFolders += obj["size"]
		fileTypeAndCount.append(obj)
	elif extTypeobj == "" or not extTypeobj:
		# print("list already has values, but does not contain ext: %s" % (ext))
		obj = copy.deepcopy(fileTypeAndCountObj)
		# print(obj["file_extension"])
		extension = ext
		if not bool(ext.strip()):
			extension = "None"
		obj["file_extension"] = extension
		obj["count"] = 1
		obj["size"] = os.path.getsize(fullPath)
		# if obj["size"] >= largestFile["size"]:
		# 	largestFile["filename"] = filename
		# 	largestFile["file_path"] = fullPath
		# 	largestFile["size"] = obj["size"]
		fileTypeAndCount.append(obj)
		totalSizeOfFilesAndFolders += obj["size"]
	else:
		extTypeobj["count"] += 1  
		extTypeobj["size"] += os.path.getsize(fullPath)
		age = datetime.datetime.fromtimestamp(os.path.getctime(fullPath))
		if oldestFile["date"] == 0 or age.time() < oldestFile["date"].time():
			oldestFile["filename"] = filename
			oldestFile["file_path"] = fullPath
			oldestFile["date"] = age
		if youngestFile["date"] == 0 or age.time() > youngestFile["date"].time() :
			youngestFile["filename"] = filename
			youngestFile["file_path"] = fullPath
			youngestFile["date"] = age
		# if extTypeobj["size"] >= largestFile["size"]:
		# 	largestFile["filename"] = filename
		# 	largestFile["file_path"] = fullPath
		# 	largestFile["size"] = extTypeobj["size"]
		totalSizeOfFilesAndFolders += extTypeobj["size"]
		file_size_array.append(extTypeobj["size"])


if __name__ == "__main__":
	cwd = os.getcwd()
	try:
		fn = sys.argv[1]	
		if os.path.exists(fn):
			cwd = 	fn
	except:
		# print("failed to load path")
		err = "y"
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
	totalFilesIncludingSubDirectories = 0

	# print(listOfFiles)
	allFiles = list()

	# Iterate over all the entries
	for entry in track(listOfFiles, description="Calculating Files", get_time=None):
		# Create full path
		fullPath = os.path.join(cwd, entry)
		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullPath):
			# allFiles = allFiles + getListOfFiles(fullPath)
			obj = copy.deepcopy(dirSizeAndCountObj)
			obj["directory"] = entry
			obj["size"], obj["child_count"] = get_size(fullPath)
			totalFilesIncludingSubDirectories += obj["child_count"]
			dirSizeAndCountList.append(obj)
			directoryCount += 1
			totalSizeOfFilesAndFolders += obj["size"]
		elif os.path.islink(fullPath):
			symlinkCount += 1
		else:
			fileCount += 1
			allFiles.append(fullPath)
			filename, file_extension = os.path.splitext(entry)
			updateFileTypeCount(fullPath, filename, file_extension, totalSizeOfFilesAndFolders)
	print("--------------------------------------------------------------------------")
	print(cwd)
	print("--------------------------------------------------------------------------")
	print("Total Size: %s, Total Objects: %s, Directories: %s, Sym Links: %s, Files: %s" % (convert_size(totalSizeOfFilesAndFolders), totalNumberOfObjects ,directoryCount, symlinkCount, fileCount))
	# print(fileTypeAndCount)
	# print(allFiles)            
	# return allFiles
	# print("--------------------------------------------------------------------------")
	# print("%-50s%-15s%-10s" % ("Directories", "# children", "Size"))	
	# print("--------------------------------------------------------------------------")
	table = Table(show_header=True, header_style="bold magenta")
	table.add_column("Directories", style="dim", width=12)
	table.add_column("# children", justify="right")
	table.add_column("Size", justify="right")
	dirSizeAndCountList = sorted(dirSizeAndCountList, key = lambda i: i['size'],reverse=True)
	for entry in dirSizeAndCountList:
		# print("%-50s%-15s%10s" %(entry["directory"], '{:,}'.format(entry["child_count"]), convert_size(entry["size"])))
		table.add_row(
			entry["directory"], '{:,}'.format(entry["child_count"]), convert_size(entry["size"])
		)
	console.print(table)
	print("")
	# print("--------------------------------------------------------------------------")
	# print("%-50s%-10s%-10s" % ("Extension","Number", "Size"))
	# print("--------------------------------------------------------------------------")
	table = Table(show_header=True, header_style="bold magenta")
	table.add_column("Extension")
	table.add_column("Number", justify="right")
	table.add_column("Size", justify="right")
	fileTypeAndCount = sorted(fileTypeAndCount, key = lambda i: i['size'],reverse=True)
	for entry in fileTypeAndCount:
		# print("%-50s%-15s%10s" %(entry["directory"], '{:,}'.format(entry["child_count"]), convert_size(entry["size"])))
		table.add_row(
			entry["file_extension"], '{:,}'.format(entry["count"]), convert_size(entry["size"])
		)
	
	# fileTypeAndCount = sorted(fileTypeAndCount, key = lambda i: i['size'],reverse=True)
	# for entry in fileTypeAndCount:
	# 	print("%-50s%-10s%10s" %( entry["file_extension"], entry["count"], convert_size(entry["size"])))
	console.print(table)
	print("--------------------------------------------------------------------------")
	print("Largest File: ")
	print("File Size => %s" % ( convert_size(largestFile["size"])))
	print("Path => %s" % (largestFile["file_path"] ))
	print("Filename => %s" % (largestFile["filename"] ))
	print("--------------------------------------------------------------------------")		
	print("")
	# print("Average Filesize: %s" % ( convert_size( sum(file_size_array)/len(file_size_array))))
	print("")
	print("Total Number of Files in Child Folders: %s" %(totalFilesIncludingSubDirectories))
	print("")
	print("--------------------------------------------------------------------------")		
	print("")
	print("Youngest File > Date: %s, Filename: %s, File Path: %s" % (youngestFile["date"], youngestFile["filename"], youngestFile["file_path"]))
	print("")
	print("Oldest File: > Date: %s, Filename: %s, File Path: %s" % (oldestFile["date"], oldestFile["filename"], oldestFile["file_path"]))
	print("")




# table = Table(show_header=True, header_style="bold magenta")
# table.add_column("Date", style="dim", width=12)
# table.add_column("Title")
# table.add_column("Production Budget", justify="right")
# table.add_column("Box Office", justify="right")
# table.add_row(
#     "Dev 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
# )
# table.add_row(
#     "May 25, 2018",
#     "[red]Solo[/red]: A Star Wars Story",
#     "$275,000,000",
#     "$393,151,347",
# )
# table.add_row(
#     "Dec 15, 2017",
#     "Star Wars Ep. VIII: The Last Jedi",
#     "$262,000,000",
#     "[bold]$1,332,539,889[/bold]",
# )
# console.print(table)