
import paramiko
paramiko.util.log_to_file("paramiko.log")
hiddenimports = ["paramiko",  "os", "stat", "fnmatch"]
import fnmatch
import stat
from stat import S_ISDIR, S_ISREG
import os
import datetime,time

rootLocalDirectoty 	  = ""
pathToLogDirectoryes  = ""
pathToRemmoteLogs 	  = ""


# Open a transport
host,port = "",22
transport = paramiko.Transport((host,port))

# Auth    
username,password = "",""
transport.connect(None,username,password)


def createDirectoryIfNotExist(path):
	if not os.path.exists(rootLocalDirectoty + path):
    		os.makedirs(rootLocalDirectoty + path)

def deleteOldLogFiles():
	try:
	    with open((pathToLogDirectoryes + 'log.txt')) as f:
	        os.remove(pathToLogDirectoryes + 'log.txt')
	except IOError:
	    print("log path dont create") 

deleteOldLogFiles()


def getLocalFileInfo(path, remmotFileM, remmotFileC, remooteSize ):
	try:
	    with open(rootLocalDirectoty + path) as f:
	    	size  = os.stat(rootLocalDirectoty + path).st_size
	    	dataC = os.stat(rootLocalDirectoty + path).st_atime
	    	dataM = os.stat(rootLocalDirectoty + path).st_mtime
	    	dataCTs = datetime.datetime.fromtimestamp(dataC)
	    	dataMTs = datetime.datetime.fromtimestamp(dataM)
	    	remmotFileMTs = datetime.datetime.fromtimestamp(remmotFileM)
	    	remmotFileCTs = datetime.datetime.fromtimestamp(remmotFileC)
	    	__remoteDateCreat = remmotFileCTs.strftime('%Y-%m-%d %H:%M:%S')
	    	__remooteDateMod  = remmotFileMTs.strftime('%Y-%m-%d %H:%M:%S')
	    	__localDateCreate = dataCTs.strftime('%Y-%m-%d %H:%M:%S')
	    	__localDateMod    = dataMTs.strftime('%Y-%m-%d %H:%M:%S')
	    	if __remooteDateMod != __localDateMod:
	    		return True
	        return False
	except IOError:
	    return True 

def creteFilesInfoLogForNodeScript(data):
	with open((pathToLogDirectoryes + 'log.txt'), 'a') as f:
		f.write(data + "\r'")

def loadSftpFiles(remotepath, localPath, transportProtocol, dateC, dateM):
	transportProtocol.get(remotepath, (rootLocalDirectoty + localPath))
	os.utime((rootLocalDirectoty + localPath), (dateM, dateC))

def deleteOldLocalFiles(localElement, remmotList):
	if localElement in remmotList:
		print(localElement, "dont deleted")
	else: 
		os.remove(rootLocalDirectoty + localElement)

def localDirFolesLists(remmoteList, dirPath):
	for top, dirs, files in os.walk(dirPath):
	    for nm in files:
	    	name = os.path.join(top, nm)
	    	creteFilesInfoLogForNodeScript(name)
	        deleteOldLocalFiles(name.replace(rootLocalDirectoty, ''), remmoteList)

def localFileSynchronisatyon(listRemooteFoles):
	localDirFolesLists(listRemooteFoles, rootLocalDirectoty)

def getRemotInformation():
	countRemmoteElement = 0
	indexFiles = 0
	indexDirectories = 0
	directoryesCount = 0
	listRemooteFoles = []
	sftp = paramiko.SFTPClient.from_transport(transport)
	for filename in sftp.listdir('/radio/'):
	    info = sftp.lstat('/radio/' +  filename)
	    indexDirectories = indexDirectories + 1
	    directoryesCount = len(sftp.listdir('/radio/'))
	    atributes = sftp.listdir_attr('/radio/' +  filename)
	    countRemmoteElement = countRemmoteElement + len(atributes)
	    for file in atributes:
	    	createDirectoryIfNotExist(filename + "/")
	    	listRemooteFoles.append(filename + "/" + file.filename)
	    	indexFiles = indexFiles + 1
	    	neadLoad = getLocalFileInfo(filename + "/" + file.filename, file.st_mtime, file.st_atime, file.st_size)
	    	if neadLoad  == True:
	    		loadSftpFiles(("/radio/" + filename + "/" + file.filename), filename + "/" + file.filename,  sftp, file.st_mtime, file.st_atime)
	    	if indexDirectories == directoryesCount:
		    	if indexFiles == countRemmoteElement:
		    		localFileSynchronisatyon(listRemooteFoles)
	     
getRemotInformation()

