dfa = {0:{'0':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

def accepts(transitions, initial, accepting, s):
    state = initial
    for c in s:
        state = transitions[state][c]
    return state in accepting


# class RegularLanguage:
#     """Takes in a regular language and turns it into another object which describes what it is"""
#     def __init__(self, arg):
#         if isintance
#         self.arg = arg
#
#     def accepts(input):
#         return accepts()
