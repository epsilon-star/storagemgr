import json
import os
import pydub
from pydub import AudioSegment
from pydub.playback import play
import io
from cryptography.fernet import Fernet

DEFAULT_METADATA = {
    'files':[
       
    ],
    'folders':[

    ],
    'blocks':[

    ]
}
DEFAULT_TEMPPATH = 'tmpsxa'

class Volume:
    Bytes = lambda a: a
    KiloBytes = lambda a: a * 1024
    MegaBytes = lambda a: a * 1024 * 1024
    GigaBytes = lambda a: a * 1024 * 1024 * 1024

class Encrypt:
    def __init__(self,key:bytes):
        self.fernet = Fernet(key)

    def encrypt(self,data:bytes):
        return self.fernet.encrypt(data)

    def decrypt(self,data:bytes) -> bytes:
        return self.fernet.decrypt(data)
    
    def tencrypt(self,key:bytes,data:bytes):
        fernet = Fernet(key)
        return fernet.encrypt(data)

    def tdecrypt(self,key:bytes,data:bytes) -> bytes:
        fernet = Fernet(key)
        return fernet.decrypt(data)

class Storage:
    def __init__(self,st_path:str = ''):
        self.spath = st_path
        self.path = '/'

        self.fernet = Encrypt(b'DXHc9Kfa_oaeGRyw5cKzYmTOu1m7UA4De4yLRJQ1qNs=')

        # self.fernet = None
        self.key = b''
        self.header = []
        self.metadata = {}

        self.header_size = 128
        self.metadata_size = Volume.KiloBytes(8)

        ## TEMP Folder
        if not os.path.exists(DEFAULT_TEMPPATH): 
            os.mkdir(DEFAULT_TEMPPATH)
            os.system(f'attrib +h {DEFAULT_TEMPPATH}')

    def fillEmpty(self,data:bytes,totalsize:int):
        if len(data) < totalsize:
            return data + (b'\x00' * (totalsize - len(data)))
        else:
            return data

    def loadStorage_old(self,file_path:str = ''):
        file_path = file_path if file_path else self.spath
        buff = b''

        ## HEADER
        with open(file_path,'rb') as fs:
            buff = fs.read(self.header_size)
            fs.close()
        mem = []
        for x in range(0,len(buff),4):
            mem.append(int.from_bytes(buff[x:x+4],'big'))
        self.header = mem

        ## KEY
        if self.header[1] > 0:
            with open(file_path,'rb') as fs:
                fs.seek(self.header_size)
                buff = fs.read(self.header[1])
                fs.close()
            self.key = buff

        ## METADATA
        with open(file_path,'rb') as fs:
            fs.seek(self.header[0] + self.header[1])
            buff = fs.read(self.header[2])
            fs.close()
        buff = buff.replace(b'\x00',b'')
        self.metadata = json.loads(buff.decode())

    def loadStorage(self,file_path:str = ''):
        file_path = file_path if file_path else self.spath
        # header,key,metadata = [],b'',{}
        buff = None

        self.header = []
        self.metadata = {}
        self.key = b''

        with open(file_path,'rb') as fs:
            buff = fs.read(self.header_size)
            for x in range(0,len(buff),4): self.header.append(int.from_bytes(buff[x:x+4],'big'))
            if self.header[1] > 0:
                fs.seek(self.header[0])
                self.key = fs.read(self.header[1])
            fs.seek(self.header[0] + self.header[1])
            buff = fs.read(self.header[2])
            self.metadata = json.loads(self.fernet.decrypt(buff.replace(b'\x00',b'')).decode())
            fs.close()

    def sortStorage(self,file_path:str = '',newfile_path:str = ''):
        file_path = file_path if file_path else self.spath
        oldpath = file_path
        buff,header,metadata = b'',[],{}
        ometadata = {}
        key = b''
        
        ## THE FILE
        with open(file_path,'rb') as fs:
            buff = fs.read(self.header_size)
            for x in range(0,len(buff),4): header.append(int.from_bytes(buff[x:x+4],'big'))
            if header[1] > 0:
                fs.seek(header[0])
                key = fs.read(header[1])
            fs.seek(header[0] + header[1])
            buff = fs.read(header[2])
            if key:
                buff = self.fernet.tdecrypt(key,buff)
            metadata = json.loads(buff.replace(b'\x00',b'').decode())
            ometadata = json.loads(buff.replace(b'\x00',b'').decode())
            fs.close()

        ## SORTING
        metadata['files'].sort(key=lambda x: x[-1])
        metadata['folders'].sort(key=lambda x: x[1])
        idx = header[0] + header[1] + header[2]
        for i,x in enumerate(metadata['files']):
            metadata['files'][i][2] = idx
            idx += metadata['files'][i][3]

        ## CHECKING
        if len(newfile_path) and newfile_path != file_path:
            file_path = newfile_path
        
        ## REWRITING
        with open(file_path,'wb') as fs:
            dheader = b''
            for x in header: dheader += int(x).to_bytes(4,'big')
            fs.write(dheader)
            fs.write(key)
            dmetadata = self.fillEmpty(self.fernet.tencrypt(key,json.dumps(metadata).encode()),header[2])
            fs.write(dmetadata)
            with open(oldpath,'rb') as fsx:
                for x in ometadata['files']:
                    # print(x)
                    fsx.seek(x[2])
                    fs.write(fsx.read(x[3]))
                fsx.close()
            fs.close()

    def updateHeader(self,header:list = []):
        header = header if len(header) else self.header
        bheader = b''
        for x in header: bheader += int(x).to_bytes(4,'big')
        self.writeData(self.spath,0,self.header[1],bheader)

    def updateMetadata(self,metadata:dict = {}):
        metadata = metadata if len(metadata) else self.metadata
        self.writeData(self.spath,self.header[0] + self.header[1],self.header[2],self.fernet.encrypt(json.dumps(metadata).encode()))

    def sortMetadata(self,metadata:dict = {}): pass

    def fileList(self,path:str = '',metadata:dict = {},idx:bool = False,meta:bool = False):
        metadata = metadata if len(metadata) else self.metadata
        path = self.correctPath(path) if len(path) else self.path
        output = []
        for i,x in enumerate(list(metadata['files'])):
            if x[0] == path:
                if not meta:
                    output.append([x[0],x[1]])
                else:
                    output.append(x)
                
                if idx: output[-1].append(i)
        return output

    def addFile(self,fpath:str,path:str = '',metadata:dict = {}):
        if os.path.basename(fpath) in [x[1] for x in self.fileList(path)]: return False
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        bfile = b''
        blocks = self.findBlocks()
        fname = os.path.basename(fpath)
        with open(fpath,'rb') as fs:
            bfile = fs.read()
            fs.close()
        offset = None
        for x in blocks:
            if len(bfile) <= abs(x[1]-x[0]):
                offset = x
        if offset:
            block = [path,fname,offset[0],len(bfile)]
        else:
            block = [path,fname,metadata['files'][-1][2] + metadata['files'][-1][3],len(bfile)]
        self.metadata['files'].append(block)
        self.updateMetadata()
        self.writeData(self.spath,block[2],block[3],bfile)

    def delFile(self,path:str = '',metadata:dict = {},filename:str = ''):
        if not len(filename): return
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        fbuff = []
        for i,x in enumerate(metadata['files']):
            if path == x[0] and filename == x[1]:
                fbuff = x
                self.metadata['files'].pop(i)
                self.updateMetadata()
                break
        if len(fbuff): self.writeData(self.spath,fbuff[2],fbuff[3],b'\x00')

    def getFile(self,path:str = '',metadata:dict = {},filename:str = ''):
        if not len(filename): return b''
        metadata = metadata if len(metadata) else self.metadata 
        path = self.correctPath(path) if len(path) else self.path
        flist = self.fileList(path,meta=True)
        for x in flist:
            if filename == x[1]:
                return self.readData(self.spath,x[2],x[3])
        return b''

    def moveFile(self,path:str,newpath:str,filename:str):
        path = self.correctPath(path) if len(path) else self.getPath()
        newpath = self.correctPath(newpath)
        if not self.pathExist(path) or not self.pathExist(newpath): return "Directroy Not Found In Storage"
        elif filename not in [x[1] for x in self.fileList(path)]: return "File Not Found In Directroy"
        elif filename in [x[1] for x in self.fileList(newpath)]: return "There Is Another File In New Directory With Same Name"
        else:
            for ms in self.fileList(path,idx=True):
                if filename == ms[1]:
                    self.metadata['files'][ms[-1]][0] = newpath
                    self.updateMetadata()
                    return True
            return False

    def renameFile(self,path:str = '',metadata:dict = {},filename:str = '',newfilename:str = ''):
        if not len(filename): return False
        if newfilename in [x[1] for x in self.fileList(path)]: return False
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        for i,x in enumerate(metadata['files']):
            if x[0] == path and x[1] == filename:
                self.metadata['files'][i][1] = newfilename 
                self.updateMetadata()
                break
        return False

    def extractFile(self,path:str = '',metadata:dict = {},filename:str = '',newfilename:str = ''):
        if not len(filename): return
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        flist = self.fileList(path,meta=True)
        fbyte = b''
        for x in flist:
            if filename == x[1]:
                fbyte = self.readData(self.spath,x[2],x[3])
                break
        if len(newfilename):
            with open(newfilename,'wb') as fs:
                fs.write(fbyte)
                fs.close()
        else:
            with open(filename,'wb') as fs:
                fs.write(fbyte)
                fs.close()

    def folderList(self,path:str = '',metadata:dict = {}):
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        output = []
        for x in list(metadata['folders']):
            if x[0] == path:
                output.append(x)
        return output

    def addFolder(self,path:str = '',metadata:dict = {},foldername:str = ''):
        if not len(foldername): return False
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        for x in metadata['folders']:
            if x[0] == path and x[1] == foldername:
                return False
        self.metadata['folders'].append([path,foldername]) 
        self.updateMetadata()
        return True
    
    def delFolder(self,path:str = '',metadata:dict = {},foldername:str = ''):
        if not len(foldername): return False
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        for i,x in enumerate(metadata['folders']):
            if x[0] == path and x[1] == foldername:
                self.metadata['folders'].pop(i) 
                self.updateMetadata()
                return True
        return False

    def renameFolder(self,path:str = '',metadata:dict = {},foldername:str = '',newfoldername:str = ''):
        if not len(foldername): return False
        if newfoldername in [x[1] for x in self.folderList(path)]: return False
        path = self.correctPath(path) if len(path) else self.path
        metadata = metadata if len(metadata) else self.metadata 
        for i,x in enumerate(metadata['folders']):
            if x[0] == path and x[1] == foldername:
                self.metadata['folders'][i][1] = newfoldername 
                self.updateMetadata()
                return True
        return False

    def changePath(self,path:str):
        output = ''
        if path == '/':
            output = '/'
        elif path[0] == '/' and len(path) > 1:
            output = path
        elif path[0] != '/' and len(path) > 1:
            output = self.path + ('/' if self.path[-1] != '/' else '') + path

        if self.pathExist(output):
            self.path = path
    
    def correctPath(self,path:str):
        output = ''
        if path == '/':
            output = '/'
        elif path[0] == '/' and len(path) > 1:
            output = path
        elif path[0] != '/' and len(path) > 1:
            output = self.path + ('/' if self.path[-1] != '/' else '') + path
        return output
            
    def getPath(self):
        return self.path
    
    def pathExist(self,path:str):
        if path == '/': return True
        path = self.correctPath(path)
        flist = path.split('/')
        for i in range(1,len(flist)):
            fbuff = '/'.join(flist[:i]) or '/'
            if flist[i] not in [x[1] for x in self.folderList(fbuff)]:
                return False
        return True

    def fileExsit(self,path:str,filename:str):
        if not self.pathExist(self.correctPath(path)):
            return False
        else:
            if filename not in [x[1] for x in self.fileList(path)]: return False
            else: return True

    def dirList(self,path:str = '',lsort:str = 'normal',reverse:bool = False):
        path = self.correctPath(path) if len(path) else self.path
        if not self.pathExist(path): return "Directory Not Found in Storage"
        output,folders,files = [],[],[]
        for x in self.fileList(path,meta=True):
            files.append([x[1],x[-1]])
        for x in self.folderList(path):
            folders.append([x[1],'f'])
        files.sort(key=lambda a: a[0],reverse=reverse)
        folders.sort(key=lambda a: a[0],reverse=reverse)
        output = folders + files
        return output

    def findBlocks(self):
        blocks = []
        datastart = self.header[0] + self.header[1] + self.header[2]
        flist = self.metadata['files']
        for i,x in enumerate(flist):
            if i == 0:
                if x[2] > datastart:
                    blocks.append([datastart,x[2]])
            elif flist[i-1][2]+flist[i-1][3] < x[2]:
                blocks.append([flist[i-1][2]+flist[i-1][3],x[2]])
        return blocks

    def readData(self,path:str,start:int,length:int):
        output = b''
        try:
            with open(path,'rb') as fs:
                fs.seek(start)
                output = fs.read(length)
                fs.close()
        except: output = b''
        return output

    def writeData(self,path:str,start:int,length:int,data:bytes):
        try:
            with open(path,'r+b') as fs:
                fs.seek(start)
                fs.write(data + (b'\x00' * (length - len(data))))
                fs.close()
        except: return False
        else: return True

if __name__ == "__main__":
    s = Storage('storage-1.sxa')
    s.loadStorage()
    # print(s.metadata)
    # print(Fernet.generate_key())

    # s.sortStorage(newfile_path='storage-1.sxa')
    # ns = Storage('storage-1.sxa')
    # ns.loadStorage()
    # ns.loadStorage_new()
    # print(s.metadata)
    # print(s.getFile('/',filename='Text1.txt'))
    # print(ns.metadata)
    # print(ns.getFile('/',filename='Text1.txt'))

    # s.sortStorage('storage_xx.sxa')

    path = '/'
    newpath = 'Music'
    # print(s.fileList(path,idx=True))
    # print(s.correctPath(path))
    # print(s.pathExist(path))
    # print(s.dirList(path))
    # print(s.dirList(newpath))
    # print("="*20)
    # print(s.metadata)
    # print(s.moveFile(path,newpath=newpath,filename='JoneyMusic.mp3'))
    # print(s.dirList())
    # print(s.metadata)
    # print(s.dirList(path))
    # print(s.dirList(newpath))

    # print(s.folderList())
    # s.changePath('Musics1')
    # s.renameFolder(foldername='Musics1',newfoldername='Music')
    # print(s.dirList())
    # print(s.fileList())
    # print(s.folderList())

    # print(s.fileList())
    # print(s.folderList())

    # print(s.getFile('/',filename='readme.md'))
    # print(ss.getFile('/',filename='readme.md'))
    # print(s.folderList('/'))


    # print(s.renameFolder('/',foldername='Musics',newfoldername='Musics1'))
    # print(s.delFolder('/',foldername='musics'))
    # s.addFolder('/',foldername='musics')

    # print(s.renameFile('/',filename='music.mp3',newfilename='JoneyMusic.mp3'))
    # print(s.addFile("readme.md"))
    # print(s.getFile('/',filename='readme.md'))
    # s.delFile('/',filename='Text1.txt')
    # s.extractFile('/',filename='readme.md',newfilename='readme_extracted.md')
    # print(s.metadata)
    # print(s.header)
    # s.header[3] = len(json.dumps(s.metadata))
    # s.updateHeader()
    # buff = DEFAULT_METADATA.copy()
    # buff['files'] = s.metadata['files']
    # print(buff)
    # print(s.metadata)
    # s.metadata = buff
    # print(s.metadata)
    # s.updateMetadata()