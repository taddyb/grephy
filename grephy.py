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
        string = ""
        info = []
        ops = []
        while(i < self.m):
            if(self.regexp[i] == '('):
                ops.append(i)
            elif(self.regexp[i] == '+'):
                info.append(string)
                string=""
            elif(self.regexp[i] == ')'):
                ore = ops.pop()
                if (self.regexp[ore] == '('):
                    info.append(string)
                    string = ""
                    if(len(ops) == 0):
                        if(i < (self.m-1) and self.regexp[i+1] == '*'):
                            self.graph.add_edge(state, state, transition=info)
                            i = i + 1
                        else:
                            self.graph.add_edge(state, state +1, transition=info)





            elif(i < (self.m-1) and self.regexp[i+1] == '*'):
                self.graph.add_edge(state, state, transition=check(self.regexp[i], state, self.graph))

            elif((self.regexp[i] == '(' or self.regexp[i] == '+' or self.regexp[i] == '*' or self.regexp[i] == ')') == False):
                if(len(ops) > 0):
                    string = string + self.regexp[i]
                else:
                    self.graph.add_edge(state, state+1, transition=self.regexp[i])
                    state = state + 1

            i = i + 1

    def recognizes(self, text):
        recog = []
        state = 0
        text.replace('.', '')
        words = text.split()
        length = self.graph.order()
        for i in range(0,len(words)):
            word = words[i]
            for char in word:
                if(state != -1):
                    listStates = self.graph[state].keys()
                    for j in listStates:
                        if(isinstance(j, list)):
                            for k in j:
                                if(isinstance(self.graph[state][k]['transition'], list)):
                                    for l in self.graph[state][k]['transition']:
                                        if(char == l):
                                            state = k
                                        if(state == (length -1)):
                                            recog.append(word)
                                            state= -1
                                else:
                                    if(char == self.graph[state][k]['transition']):
                                        state = k
                                    if(state == (length -1)):
                                        recog.append(word)
                                        state= -1
                        else:
                            if(isinstance(self.graph[state][j]['transition'], list)):
                                for l in self.graph[state][j]['transition']:
                                    if(char == l):
                                        state = j
                                    if(state == (length -1)):
                                        recog.append(word)
                                        state= -1
                            else:
                                if(char == self.graph[state][j]['transition']):
                                    state = j
                                if(state == (length -1)):
                                    recog.append(word)
                                    state= -1
            state = 0
        return recog;

##################################################################################
# Check function to see if a transition already exists in that direction
##################################################################################
def check(char, state, graph):
    if(graph.has_edge(state, state)):
        list = [graph[state][state]['transition']]
        list.append(char)
        return list
    else:
        return char

##################################################################################
# DFA class
##################################################################################
class DFA(object):
    def __init__(self, nfa, alphabet):
        nfaGraph = nfa.graph
        self.dfaGraph = nx.DiGraph()
        nfaNodes = nfaGraph.nodes()
        state=0
        alphabet = list(alphabet)
        for node in nfaNodes:
            tempStates = list(alphabet)
            listStates = nfaGraph[node].keys()
            for i in listStates:
                if(isinstance(i, list)):
                    for j in i:
                        transition = nfaGraph[node][j]['transition']
                        tempStates.remove(transition)
                        if(node == j):
                            self.dfaGraph.add_edge(state, state, transition=transition)
                        else:
                            self.dfaGraph.add_edge(state, state+ 2, transition=transition)
                        self.dfaGraph.add_edge(state, state+1, transition=tempStates)
                        self.dfaGraph.add_edge(state+1, state+1, transition=alphabet)
                        state = state + 2

                else:
                    transition = nfaGraph[node][i]['transition']
                    tempStates.remove(transition)
                    self.dfaGraph.add_edge(state, state+1, transition=tempStates)
                    self.dfaGraph.add_edge(state+1, state+1, transition=alphabet)
                    self.dfaGraph.add_edge(state, state+2, transition=transition)
                    state = state + 2


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
    parser.add_argument('-n', metavar='NFA_FILE', type=argparse.FileType('w'), help="A file to output an NFA of the regular expression to")
    parser.add_argument('-d', metavar='DFA_FILE', type=argparse.FileType('w'), help="A file to output a DFA of the regular expression to")
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
def learnAlphabet(inputContents):
    alphabet = set()
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
        inputContents = args.inputFile.read()
        alphabet = learnAlphabet(inputContents)
        regexAlpha = learnRegex(args.regex)
        if(config.get('DEBUG', 'printAlpha') == "True"):
             print(alphabet)
             print(regexAlpha)
        isValid = False
        for character in regexAlpha:
            for letter in alphabet:
                if(character == letter):
                    isValid = True
        if(isValid == False):
            error(101)
        else:
            nfa = NFA(args.regex)
            if(args.n is not None):
                nfaGraph = nfa.graph.edges(data = True)
                args.n.write('\n'.join('(%s, %s, %s)' % x for x in nfaGraph))
                args.n.close()
            if(args.d is not None):
                dfa = DFA(nfa, regexAlpha)
                dfaGraph = dfa.dfaGraph.edges(data = True)
                args.d.write('\n'.join('(%s, %s, %s)' % x for x in dfaGraph))
                args.d.close()

            recog = nfa.recognizes(inputContents)
            if(recog == []):
                print("No Matches")
            else:
                print(recog)
    else:
        error(100)

if __name__ == "__main__":
    main()
