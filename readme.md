# Python Storage Manager Porject
## Virtual Disk + Encryption
this project while is an alias of popular app `WinRar`, is also able to encrypt datas using Fernet Corner Formula.

## How's it Work ?
there is 4 part of every `.sxa` storage file

### [First] Header
this part stores `128` bytes of datas and saperated into 32 parts of `4` bytes

the 1st,2nd,3th part store how many byte header length have, length of ecnryption key and capacity of metadata

sum of this three together is data's starting byte, which is files stored in storage mixed togheter, some have parts and some is taking only one block

### [Second] Encrpytion Key
this is part is simple, just stored encrpytion key in it.

### [Third] Metadata
this part stores all data related to a file in storage, such as name, starting point & length, last modified date, created date and much more, just like a real file explorer.

this part also have 2 part, one fore folders and the other for files, every file and folder have a defined path, which shows where exactly a folder or file created.

### [Fourth] Datas
and at last but no least, this part stores data of files completly randomized and almost big group of devs cannot find that the exact block for a specific file, which also adds myself to that group ;)


## Attention !!!
any loss data will not be recovered, i put my life into this project for less loss percentage which currently the risk is `5.4%`.

*this project is very good and risky at same time, its like bet TBH.*

## As For You !
unfortunatly this project is currently under active developments, which is me <3.

You can find a file called `tasklist.md`, which can show you how much i worked on this, and where exactly we are right now.

## Contacting
Telegram : `@epsilon_star`
