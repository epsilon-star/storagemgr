import os
import sys
import lzma
import typing

vol_table = [
    "",
    "K",
    "M",
    "G",
    "T",
]

def formatVolume(inputs,cot_format = 0):
    inputs = str(inputs)
    buff1 = inputs[::-1]
    output = ""
    if cot_format:
        # output = ','.join([inputs[x:x+3] for x in range(0,len(inputs),3)][y][::-1] for y in range())
        output = inputs + 'b'
    else:
        buff = [buff1[x:x+3] for x in range(0,len(buff1),3)]
        output = buff[-1][::-1] + "" + (vol_table[len(buff)-1] if len(buff)-1 < len(vol_table) else f'e^{len(buff1)-1}') + "b"
    return output


con = 6
val = 100
fl = "storage_masbvugasd.shadow"

# with open(fl,"wb") as fs:
#     fs.write(f'{"0"*((10**con)*val)}'.encode())
#     fs.close()

datas = None

with open(fl,"rb") as fs:
    datas = fs.read()
    fs.close()

def appendData(source:bytes,data:bytes,pos:int = 0):
    # buff = lzma.compress(data.encode())
    buff = data
    ins = f'|{buff}|'.encode() # type: ignore
    output = source[0:pos or 0] + ins + source[pos+len(ins):]
    return output


npdata = None
with open('music.mp3','rb') as fs:
    npdata = fs.read()
    fs.close()

newdatas = appendData(datas,npdata,3)

# print(len(datas[0:80]))
# print(len(newdatas[0:80]))
with open("mps.shadow","wb") as fs:
    fs.write(newdatas)
    fs.close()


# print(f'mobin'.encode())