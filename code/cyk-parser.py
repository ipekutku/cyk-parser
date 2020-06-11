import random #importing random library

class CYK(object):
    
    rule_set = [] # list for rules
    root = {} #dict for ROOT rules
    nonterminal_rules = {} # dict for the rules that contain nonterminals on right-hand side
    terminal_rules = {} #dict for the rules that contain terminals on right-hand side
    rvr_nonterminals = {} #reverse dict of nonterminal rules, to use in CYK
    rvr_terminals = {} #reverse dict of terminal rules, to use in CYK
    _showTable = False #a boolean value to show the parse table of the given sentence
    
    #init function
    def __init__(self, folderpath):
        self.rule_set = self._rules(folderpath)
        self._classify_rules(self.rule_set)
        self._reverseAllDicts()
        return
    
    ### MAIN FUNCTIONS ###
    
    #takes the folder path as the argument returns the rule set
    def _rules(self, folderpath):
        rule_set = []
        with open(folderpath) as f:
            for line in f:
                if(line != '\n' and line[0] != '#'):
                    line_list = line.split()
                    if '#' in line_list:
                        temp = line.split('#', 1)[0]
                        rule = temp.split()
                    else:
                        rule = line_list
                    rule_set.append(rule)
        return rule_set
    
    #takes the rule set as the argument, creates random sentences, writes them to an output file, returns the generated sentences
    def randsentence(self):
        
        file = open('output.txt', 'w+')
        vocab_sentences = self._generateSentences(5, 5, file, True) #sentences generated only from vocabulary
        rule_sentences = self._generateSentences(30, 1, file) #sentences generated from rules
        file.close()
        return vocab_sentences, rule_sentences
    
    #takes a sentence as the argument, returns if the sentence is grammatically correct or not 
    def CYKParser(self, sentence):
        length = len(sentence)
        
        if(sentence[-1] == '?'):
            sentence = sentence[4:length-1]
        else:
            sentence = sentence[:length-1]
            
        parse_table = {} # parse table as dict
        for j in range(1, len(sentence) + 1):
            place = (j-1, j)
            try:
                left_hand = self.rvr_terminals[sentence[j-1]]
                parse_table[place] = []
                parse_table[place] += left_hand
                for val in left_hand:
                    if val in list(self.rvr_nonterminals.keys()):
                        parse_table[place].append(self.rvr_nonterminals[val][0])
            except KeyError:
                parse_table[place] = []
            
            for i in range(j-2, -1, -1):
                parse_table[(i,j)] = []
                for k in range(i+1, j):
                    for right_hand, left_hand in self.rvr_nonterminals.items():
                        right_hand = right_hand.split()
                        if len(right_hand) == 1:
                            continue
                        if len(right_hand) == 2 and right_hand[0] in parse_table[(i,k)] and right_hand[1] in parse_table[(k,j)]:
                            parse_table[(i,j)].append(left_hand[0])
                            
        #if true, returns the parse table
        if self._showTable == True: 
            return parse_table
        
        if 'S' in parse_table[0, len(sentence)]:
            return True
        else:
            return False
    
        
    ### HELPER FUNCTIONS ###
    
    #takes the rule_set as the argument, classifies the rules as root, nonterminal and terminals
    def _classify_rules(self, rule_set):
        for rule in rule_set:
            if rule[0] == 'ROOT':
                try:
                    self.root[rule[0]].append(' '.join(rule[1:]))
                except:
                    self.root[rule[0]] = [' '.join(rule[1:])]
            elif rule[0].isupper() or len(rule) == 3:
                try:
                    self.nonterminal_rules[rule[0]].append(' '.join(rule[1:]))
                except KeyError:
                    self.nonterminal_rules[rule[0]] = [' '.join(rule[1:])]
            elif rule[1].islower():
                try:
                    self.terminal_rules[rule[0]].append(rule[1])
                except KeyError:
                    self.terminal_rules[rule[0]] = [rule[1]]  
        return
    
    #function to generate sentences randomly
    def _generateSentences(self, num_of_sentences, sentence_length, file, onlyVocab=None):
        if(onlyVocab == True):
            file.write("-----FROM VOCABULARY-----\n")
        else:
            file.write("-----FROM RULES-----\n")
        all_sentences = []
        for j in range(num_of_sentences):
            sentence = []
            root_rule = random.choice(self.root['ROOT'])
            root_rule = root_rule.split()
            punctuation = root_rule[-1]
            length = len(root_rule)
            if(length > 2):
                beginning = ' '.join(root_rule[:length-2])
                sentence.append(beginning)
            if(onlyVocab == True):
                for i in range(sentence_length):
                    key = random.choice(list(self.terminal_rules.keys()))
                    word = random.choice(self.terminal_rules[key])
                    sentence.append(word)
                sentence.append(punctuation)
            else:
                for j in range(sentence_length):
                    rule = random.choice(list(self.rvr_nonterminals.keys()))
                    rule = rule.split()
                    while(len(rule) != 2):
                        rule = random.choice(list(self.rvr_nonterminals.keys()))
                        rule = rule.split()
                    for k in range(len(rule)):
                        sentence_part = self._choice(rule[k]) #choice function call
                        sentence.append(sentence_part)
                    sentence.append(punctuation)
            sentence = ' '.join(sentence)
            file.write(sentence + '\n')
            all_sentences.append(sentence)
        return all_sentences
    
    #a recursive function for sentence generation from rules  
    def _choice(self, key):
        try:
            word = random.choice(self.terminal_rules[key])
            return word
        except KeyError:
            sentence_part = []
            rule = random.choice(self.nonterminal_rules[key])
            #while(rule.isupper()):
                #rule = random.choice(self.nonterminal_rules[key])
            rule = rule.split()
            for i in range(len(rule)):
                word = self._choice(rule[i]) #recursive call
                sentence_part.append(word)
            return (' '.join(sentence_part))
        
    #takes a dict as the argument, returns a new dict as the values are the keys and the keys are the values
    def _reverseDict(self, Dict):
        reverse_dict = {}
        for key, value in Dict.items():
            for val in value:
                try:
                    reverse_dict[val].append(key)
                except:
                    reverse_dict[val] = [key]
        return reverse_dict
    
    #function to reverse all dicts
    def _reverseAllDicts(self):
        self.rvr_nonterminals = self._reverseDict(self.nonterminal_rules)
        self.rvr_terminals = self._reverseDict(self.terminal_rules)
        return
    
    #takes a sentence list as the argument, applies the CYKParser to all sentences in the list
    def applyCYK(self, sentences):
        for sentence in sentences:
            sentence_as_list = sentence.split()
            result = self.CYKParser(sentence_as_list)
            print(sentence + ' = ' + str(result))
        return
    
    #takes a sentence as the argument, prints it's parse table using CYKParser function
    def showTable(self, sentence):
        self._showTable = True
        result = self.CYKParser(sentence)
        print(result)
        self._showTable = False
        return

model = CYK('cfg.gr') #model creation
onlyVocabSentences, ruleSentences = model.randsentence() #lists of sentences
model.applyCYK(onlyVocabSentences) #apply CYK to the sentences from vocabulary
print('\n')
model.applyCYK(ruleSentences) #apply CYK to the sentences from rules
print('\n')
model.showTable('this sandwich kissed me  .'.split()) #an example parse table of a grammatically correct sentence
print('\n')
model.showTable('you in a president .'.split()) #an example parse table of a grammatically incorrect sentence