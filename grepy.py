import argparse

def main():
    args = parseArguments()

def parseArguments():
    parser = argparse.ArgumentParser(description='A program which emulates grep')
    parser = argparse.ArgumentParser(prog='Grepy')
    parser.add_argument('-n', metavar='NFA_FILE', type=argparse.FileType('rw'), help="A file to output an NFA of the regular expression to. Optional")
    parser.add_argument('-d', metavar='DFA_FILE', type=argparse.FileType('rw'), help="A file to output a DFA of the regular expression to. Optional")
    parser.add_argument('REGEX', metavar='Regex_Expression', type=str, help='A regular expression to search the input file')
    parser.add_argument('FILE', metavar='Input_File', type=argparse.FileType('r'), help="A file which the Regex_Expression checks for matches")

    args = parser.parse_args()
    return args;

if __name__ == "__main__":
    main()

#Old code
#
# import sys
#
#
# nfaFile = open(sys.argv[2],"w")
# # dfaFile = open(sys.argv[2],"w")
# inputFile = open(sys.argv[1],"r")
#
# inputContents = inputFile.read()
# inputFile.close()
#
# nfaList = []
# alphabetList = []
# stateCount = 0
# nfaList.append([stateCount])
# stateCount = stateCount + 1
#
# for character in inputContents:
#     if (ord(character) > 47) and (ord(character) < 123):
#         alphabetList.append(character)
#         nfaList.append([stateCount])
#         stateCount = stateCount + 1
#
# alphabetSet = set(alphabetList)
#
# print "Basic NFA"
# for position in nfaList:
#     if(position == nfaList[0]):
#         print position
#     else:
#         print "--"
#         print position
#
# print nfaList
#
# print "Alphabet:"
# print alphabetSet


# Next Steps
# 1) write NFA to file.
# 2) use alphabet to make a dfa
# 3) minimize the dfaFile
# 4) make an accepting function
