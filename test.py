a = '/a/d/s/f/f/a/c/c////'

print(a[len(a)-1 - a[::-1].index('/')])