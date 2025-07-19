import os

wdir = input("Insert Directory (Just Name of Desiered Folder)> ") + '/'
doing = exit() if input('Doing Number Sorting ? (y/n):').lower() == 'n' else None

data = os.listdir(wdir)

data.pop(data.index('namefixer.py'))

for i,x in enumerate(data):
    if x == 'namefixer.py': continue
    os.rename(wdir + x,wdir + f'{str(i+1).zfill(len(str(len(data))))}.{x.split(".")[-1]}')

# os.rename(wdir + 'oasdhnf.txt',wdir + 'oasdhnf1.txt')

# print(data)