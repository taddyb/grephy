import sys


nfaFile = open(sys.argv[2],"w")
# dfaFile = open(sys.argv[2],"w")
inputFile = open(sys.argv[1],"r")

inputContents = inputFile.read()
inputFile.close()

nfaList = []
alphabetList = []
stateCount = 0
for character in inputContents:
    if (ord(character) > 47) and (ord(character) < 123):
        alphabetList.append(character)
        nfaList.append([stateCount])
        stateCount = stateCount + 1

alphabetSet = set(alphabetList)

print nfaList







# class RegularLanguage:
#     """Takes in a regular language and turns it into another object which describes what it is"""
#     def __init__(self, arg):
#         if isintance
#         self.arg = arg
#
#     def accepts(input):
#         return accepts()
