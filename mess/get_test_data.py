fileName = './data/disneyData'
writeName = './data/test_disneyData'

def readTest():
    with open(fileName,'r') as fp:
        for line in fp:
            data = line.split()
            if data[0]  >= '1550544917294223495':
                yield line

def writeTest():
    read = readTest()
    with open(writeName,'w') as fp:
        try:
            while True:
                fp.write(next(read))
        except StopIteration:
            return

writeTest()
