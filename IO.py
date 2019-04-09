import os
from pathlib import Path
class CSVFileReader:
    def __init__(self, path, hasHeaders=False):
        self.path = Path(path)
        #check if path exists, is readable
        self.readable = None
        self.maxColumns = None
        self.minColumns = None
        self.rows = None
        self.hasHeaders=False
        self.readable = False
        if not str(path).lower().replace('\n','').split('.')[len(str(path).split('.'))-1] == 'csv':
            raise Exception("File: '{}' does not have a .csv extension".format(self.path))
        if os.access(self.path, os.F_OK) and os.access(self.path, os.R_OK):
            self.readable = True
        else:
            raise PermissionError("File: '{}' does not exist or does not have read permissions on this user".format(self.path))
        
        #read path

    def read(self):
        if self.readable:
            self.data=[]
            self.file = open(self.path, 'r')
            for line in self.file:
                if line.replace('\n','')!=',' and len(line)>3:
                    self.data.append(line.replace(' ', '').replace('\n', '').strip().split(','))
            self.file.close()
            self.rows = len(self.data)
            self.minColumns = len(self.data[0])
            self.maxColumns = 0
            for row in self.data:
                if len(row)+1>self.maxColumns:
                    self.maxColumns = len(row)
                if len(row)+1<self.minColumns:
                    self.minColumns = len(row)
class CSVFileWriter:
    def __init__(self, path, data):
        self.path = path
        self.data = data
        if not str(path).lower().replace('\n','').split('.')[len(str(path).split('.'))-1] == 'csv':
            raise Exception("File: '{}' does not have a .csv extension".format(self.path))
        self.writeable = True
        #if os.access(self.path, os.W_OK):
            #self.writeable = True
        #else:
            #raise PermissionError("File: '{}' does not exist or does not have read permissions on this user".format(self.path))
    def write(self):
        if self.writeable:
            self.file = open(self.path, 'w')
            for line in self.data:
                self.file.write((','.join(line)+'\n'))
            self.file.close()
class Directory:
    def __init__(self, path):
        self.path = Path(path)
        self.readable = False
        if not (os.access(self.path, os.F_OK) and os.access(self.path, os.R_OK)):
            raise PermissionError("File: '{}' does not exist or does not have read permissions on this user".format(self.path))
        elif not os.path.isdir(self.path):
            raise Exception("Path provided: '{}' is not a folder".format(self.path))
        else:
            self.readable = True
        self.subdirectories = []
        self.files = []
        if self.readable:
            children = os.listdir(self.path)
            for child in children:
                if os.path.isdir(self.path/child):
                    self.subdirectories.append(self.path/child)
                else:
                    self.files.append(self.path/child)
        self.rsubdirectories = []
        self.rfiles = []
    #add recursive method and recursive refresh method
    def recursivelist(self):
        if len(self.rsubdirectories)==0 and len(self.rfiles)==0:
            self.rsubdirectories.extend(self.subdirectories)
            self.rfiles.extend(self.files)
            for sub in self.subdirectories:
                subdir = Directory(sub)
                folders, files = subdir.recursivelist()
                self.rsubdirectories.extend(folders)
                self.rfiles.extend(files)
        return self.rsubdirectories, self.rfiles
    
    """Forces a refresh of the recursive directory and file listings. Does not return, for return values use this, then recursivelist()"""
    def forceRecursiveRefresh(self):
        self.rsubdirectories = []
        self.rfiles = []
        self.recursivelist()
        
    """Searches recursively through the directory and returns a list of files with an extension matching file_type_extension. Is not case sensetive."""
    def recursvieFileTypeSearch(self, file_type_extension):
        if len(self.rfiles)==0:
            self.recursivelist()
        matches = []
        for file in self.rfiles:
            filename = str(file).split('.')
            if str(filename[len(filename)-1]).lower()==str(file_type_extension).lower():
                matches.append(file)
        return matches
                

    
    
            
