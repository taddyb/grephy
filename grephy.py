import argparse
import re

#A main function
def main():
    args = parseArguments()
    if(checkRegex(args.regex)):
        alphabet = learnAlphabet(args.inputFile)
        print(alphabet)
    else:
        error(100)

#A function to parse the input and create a --help message
def parseArguments():
    parser = argparse.ArgumentParser(description='A program which emulates grep')
    parser = argparse.ArgumentParser(prog='Grepy')
    parser.add_argument('-n', metavar='NFA_FILE', type=argparse.FileType('rw'), help="A file to output an NFA of the regular expression to. Optional")
    parser.add_argument('-d', metavar='DFA_FILE', type=argparse.FileType('rw'), help="A file to output a DFA of the regular expression to. Optional")
    parser.add_argument('regex', metavar='Regex_Expression', type=str, help='A regular expression to search the input file')
    parser.add_argument('inputFile', metavar='Input_File', type=argparse.FileType('r'), help="A file which the Regex_Expression checks for matches")

    args = parser.parse_args()
    return args;

# A function which checks to make sure the regular expression is valid
def checkRegex(regex):
    try:
        re.compile(regex)
        return True;
    except re.error:
        return False;

#A function to learn the alphabet of the input file
def learnAlphabet(inputFile):
    alphabet = set()
    inputContents = inputFile.read()
    inputFile.close()
    for character in inputContents:
        if (ord(character) > 47) and (ord(character) < 123):
            alphabet.add(character)
    return alphabet;


#A function which takes in error codes and prints out error messages based on what is inputted
def error(code):
    if(code == 100):
        print("*************************\n ERROR: Regular Expression not valid\n*************************")


if __name__ == "__main__":
    main()

# Next Steps
# 1) write NFA to file.
# 2) use alphabet to make a dfa
# 3) minimize the dfaFile
# 4) make an accepting function
