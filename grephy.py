import argparse
import re
import networkx as nx
import ConfigParser
import io

#A class of an NFA
class NFA(object):
    def __init__(self, regexp):
        self.regexp = regexp
        self.m = len(regexp)
        self.graph = nx.DiGraph()
        ops = []
        for i in range(0,self.m):
            lp = i
            if(self.regexp[i] == '(' or self.regexp[i] == '|'):
                ops.append(i)
            elif(self.regexp[i] == ')'):
                ore = ops.pop()
                if(self.regexp[ore] == '|'):
                    lp = ops.pop()
                    self.graph.add_edge(lp, ore + 1)
                    self.graph.add_edge(ore, i)

                elif(self.regexp[ore] == '('):
                    lp = ore
                else:
                    assert False

            # If there is a kleene star, the code maps back to itself
            if(i < (self.m-1) and self.regexp[i+1] == '*'):
                self.graph.add_edge(lp, i+1)
                self.graph.add_edge(i+1, lp)

            if(self.regexp[i] == '(' or self.regexp[i] == '|' or self.regexp[i] == '*'):
                self.graph.add_edge(i, i+1)


#DFA class
#DFA class
class DFA(object):
    # regular expression
    regexp = ""
    # the dfa
    dfa = ""
    # The length of the dfa
    m = 0
    def __init__(self, nfa):
        self.regexp = nfa.regexp
        self.m = len(regexp)
        self.dfa = nx.DiGraph()
        ops = []
        for i in range(0, (m+1)):
            lp = i
            if(self.regexp[i] == '(' or self.regexp[i] == '|'):
                ops.append(i)
            elif(self.regexp[i] == ')'):
                ore = ops.pop()
                if(self.regexp[ore] == '|'):
                    lp = ops.pop()
                    self.graph.add_edge(lp, ore + 1)
                    self.graph.add_edge(ore, i)

                elif(self.regexp[ore] == '('):
                    lp = ore
                else:
                    assert False

            # If there is a kleene star, the code maps back to itself
            if(i < (self.m-1) and self.regexp[i+1] == '*'):
                self.graph.add_edge(lp, i+1)
                self.graph.add_edge(i+1, lp)

            if(self.regexp[i] == '(' or self.regexp[i] == '|' or self.regexp[i] == '*'):
                self.graph.add_edge(i, i+1)

# A function to read the ini config FILE
def readConfig(configPath):
    with open(configPath) as f:
        sample_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_config))
    return config;

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

# A function to learn the alphabet of the regex
def learnRegex(regexp):
    alphabet = set()
    for character in regexp:
        if (ord(character) > 47) and (ord(character) < 123):
            alphabet.add(character)

#A function which takes in error codes and prints out error messages based on what is inputted
def error(code):
    if(code == 100):
        print("*************************\n ERROR: Regular Expression not valid\n*************************")
    elif(code == 101):
        print("No Matches")

# ***********************************************************************************************************************
# ***********************************************************************************************************************
# ***********************************************************************************************************************

#A main function
def main():
    config = readConfig("config/config.ini")
    args = parseArguments()
    if(checkRegex(args.regex)):
        alphabet = learnAlphabet(args.inputFile)
        regexAlpha = learnRegex(args.regex)
        if(config.get('DEBUG', 'printAlpha') == "True"):
             print(alphabet)
        if(config.get('DEBUG', 'checkAlphabets') == 'True'):
            isValid = False
            for character in regexAlpha:
                for letter in alphabet:
                    if(character == letter):
                        isValid == True
            if(isValid == False):
                error(101)
        nfa = NFA(args.regex)
        print(nfa.graph.edges())
    else:
        error(100)

if __name__ == "__main__":
    main()
