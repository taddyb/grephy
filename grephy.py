##################################################################################
# Grephy v1.0
# Author: Tadd Bindas
# A project which emulates grep
##################################################################################
# Imports
##################################################################################
import argparse
import re
import networkx as nx
import ConfigParser
import io

#################################################################################
#NFA Class
#################################################################################
class NFA(object):
    def __init__(self, regexp):
        self.regexp = regexp
        self.m = len(regexp)
        self.graph = nx.DiGraph()
        state = 0
        i = 0
        ops = []
        while(i < self.m):
            if(self.regexp[i] == '(' or self.regexp[i] == '|'):
                ops.append(state)

            elif(self.regexp[i] == ')'):
                ore = ops.pop()

                if(self.regexp[ore] == '|'):
                    lp = ops.pop()
                    self.graph.add_edge(lp, ore + 1, transition=self.regexp[i])

                elif(self.regexp[ore] == '('):
                    lp = ore
                else:
                    assert False

            # If there is a kleene star, the code maps back to itself
            if(i < (self.m-1) and self.regexp[i+1] == '*'):
                self.graph.add_edge(state, state, transition=self.regexp[i])


            elif((self.regexp[i] == '(' or self.regexp[i] == '|' or self.regexp[i] == '*') == False):
                self.graph.add_edge(state, state+1, transition=self.regexp[i])
                state = state + 1
            i = i + 1

    def recognizes(self, text):
        recog = []
        state = 0
        text.replace('.', '')
        words = text.split()
        for i in range(0,len(words)):
            word = words[i]
            for j in word:
                if(len(self.graph.successors(state)) > 1):
                    successors = self.graph.successors(state)
                    i = 0
                    while(i < len(successors) or i != -1):
                        if(word[j] == self.graph[state][successors[i]]['transtition']):
                            state = successors[i]
                            i = -1
                            if(self.graph.successors(state) == []):
                                recog.append(word)
                        else:
                            i = i + 1
                elif(word[j] == self.graph[state][state+1]['transtition']):
                    state = state +1
                    if(self.graph.successors(state) == []):
                        recog.append(word)
                else:
                    break
        return recog;




##################################################################################
# DFA class
##################################################################################
class DFA(object):
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
                        self.graph.add_edge(lp, ore + 1, transition=self.regexp[i])
                        self.graph.add_edge(ore, i, transition=self.regexp[i])

                    elif(self.regexp[ore] == '('):
                        lp = ore
                    else:
                        assert False

                # If there is a kleene star, the code maps back to itself
                if(i < (self.m-1) and self.regexp[i+1] == '*'):
                    self.graph.add_edge(lp, i+1, transition=self.regexp[i])
                    self.graph.add_edge(i+1, lp, transition="empty")

                if(self.regexp[i] == '(' or self.regexp[i] == '|' or self.regexp[i] == '*'):
                    self.graph.add_edge(i, i+1, transition="empty")
                else:
                    self.graph.add_edge(i, i+1, transition=self.regexp[i])



##################################################################################
# readConfig(): read the ini config FILE
##################################################################################
def readConfig(configPath):
    with open(configPath) as f:
        sample_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_config))
    return config;

##################################################################################
# parseArguments(): parse the input and create a --help message
##################################################################################
def parseArguments():
    parser = argparse.ArgumentParser(description='A program which emulates grep')
    parser = argparse.ArgumentParser(prog='Grepy')
    parser.add_argument('-n', metavar='NFA_FILE', type=argparse.FileType('rw'), help="A file to output an NFA of the regular expression to. Optional")
    parser.add_argument('-d', metavar='DFA_FILE', type=argparse.FileType('rw'), help="A file to output a DFA of the regular expression to. Optional")
    parser.add_argument('regex', metavar='Regex_Expression', type=str, help='A regular expression to search the input file')
    parser.add_argument('inputFile', metavar='Input_File', type=argparse.FileType('r'), help="A file which the Regex_Expression checks for matches")

    args = parser.parse_args()
    return args;

##################################################################################
# checkRegex(): checks to make sure the regular expression is valid
##################################################################################
def checkRegex(regex):
    try:
        re.compile(regex)
        return True;
    except re.error:
        return False;

##################################################################################
# learnAlphabet(): learn the alphabet of the input file
##################################################################################
def learnAlphabet(inputFile):
    alphabet = set()
    inputContents = inputFile.read()
    for character in inputContents:
        if (ord(character) > 47) and (ord(character) < 123):
            alphabet.add(character)
    return alphabet;

##################################################################################
# learnRegex(): learn the alphabet of the regex
##################################################################################
def learnRegex(regexp):
    alphabet = set()
    for character in regexp:
        if (ord(character) > 47) and (ord(character) < 123):
            alphabet.add(character)
    return alphabet;
##################################################################################
# error(): takes in error codes and prints out error messages based on what is inputted
##################################################################################
def error(code):
    if(code == 100):
        print("*************************\n ERROR: Regular Expression not valid\n*************************")
    elif(code == 101):
        print("No Matches")
    elif(code == 102):
        print("Text contains metacharacters")

##################################################################################
# main(): A main function
##################################################################################
def main():
    config = readConfig("config/config.ini")
    args = parseArguments()
    if(checkRegex(args.regex)):
        alphabet = learnAlphabet(args.inputFile)
        regexAlpha = learnRegex(args.regex)
        if(config.get('DEBUG', 'printAlpha') == "True"):
             print(alphabet)
             print(regexAlpha)
        if(config.get('DEBUG', 'checkAlphabets') == 'True'):
            isValid = False
            for character in regexAlpha:
                for letter in alphabet:
                    if(character == letter):
                        isValid = True
            if(isValid == False):
                error(101)
            else:
                nfa = NFA(args.regex)
                print(nfa.graph.edges(data = True))
                inputContents = args.inputFile.read()
                args.inputFile.close()
                recog = nfa.recognizes(inputContents)
                if(recog == []):
                    print("No Matches")
                else:
                    for i in range(0, len(recog)):
                        print recog + " "
                # dfa = DFA(nfa)
                # print(dfa.dfa.edges())
        else:
            nfa = NFA(args.regex)
            print(nfa.graph.edges(data= True))
            # dfa = DFA(nfa)
            # print(dfa.dfa.edges())
    else:
        error(100)

if __name__ == "__main__":
    main()
