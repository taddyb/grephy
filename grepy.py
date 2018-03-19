import sys


nfaFile = open(sys.argv[2],"w")
# dfaFile = open(sys.argv[2],"w")
inputFile = open(sys.argv[1],"r")

inputContents = inputFile.read()
inputFile.close()

nfaList = []
alphabetList = []
stateCount = 0
nfaList.append([stateCount])
stateCount = stateCount + 1

for character in inputContents:
    if (ord(character) > 47) and (ord(character) < 123):
        alphabetList.append(character)
        nfaList.append([stateCount])
        stateCount = stateCount + 1

alphabetSet = set(alphabetList)

print "Basic NFA"
for position in nfaList:
    if(position == nfaList[0]):
        print position
    else:
        print "--"
        print position

print nfaList

print "Alphabet:"
print alphabetSet


# Next Steps
# 1) write NFA to file.
# 2) use alphabet to make a dfa
# 3) minimize the dfaFile
# 4) make an accepting function
