'''
Created on Feb 12, 2016

@author: ranuva
'''

#helper function
def testOverlap(setA, setB):
    '''
    checks if two sets(set A,setB) are disjoint
    '''
    return set(setA).isdisjoint(setB)


class SetGame():
    '''
    SetGame class 
    '''
    def __init__(self, filename = ''):
        '''
        Constructor
        '''
        
        # self.cards is a dictionary containing the mapping of each card to each of its 4 attributes
        self.cards = {}
        # card index to string mapping
        self.strCards = {}
        self.filename = filename
        
    def readInput(self):
        '''
        There are four attributes for each card. 
        Each of the attributes can take 3 different values.
        We shall map the values of each attribute to 1,2 and 3 according to the 
        following mapping.
        attr 1: color {1-blue, 2-green, 3-yellow}
        attr 2: symbol {1-A, 2-S, 3-H}
        attr 3: shade {1-lower case, 2-upper case, 3-symbol case}
        attr 4: number {1-one, 2-two, 3-three}
        '''
        if self.filename!='':
            # open the input file in read mode
            textFile = open(self.filename,'r')
            # get lines from the file
            lines = textFile.readlines()
        else:
            lines = []
            N = raw_input()
            lines.append(N)
            for i in range(int(N)):
                lines.append(raw_input())
        
        # No of cards
        self.N = int(lines[0])
        
        # for loop to run over each line to read and note each card's description
        for i in xrange(1,self.N+1,1):
            [str1, str2] = lines[i].split()
            
            # read the color 
            if str1.lower() =='blue':
                color = 1
            elif str1.lower() == 'green':
                color = 2
            else:
                color = 3
            
            # count no of chars in str2
            number = len(str2)

            # get the symbol
            if str2[0]=='a' or str2[0]=='A' or str2[0]=='@':
                symbol = 1
            elif str2[0]=='s' or str2[0]=='S' or str2[0]=='$':
                symbol = 2
            else:
                symbol = 3
            
            # get the shade
            # check for small case
            if ord(str2[0])>=97 and ord(str2[0])<=122:
                shade = 1
            # check for capital case
            elif ord(str2[0])>=65 and ord(str2[0])<=90:
                shade = 2
            # symbol case
            else:
                shade = 3
                
            # add this card and its attributes to the cards dictionary
            self.cards[i-1] = [color,symbol,shade,number]
            self.strCards[i-1] = lines[i].strip()
    
    
    def isSet(self,triplet):
        '''
        triplet - indices of three cards 
        
        This function checks if a set of three cards(triplet) forms a valid set 
        as described in the problem statement
        logic:
        each card is a 4d vector, we add them dimension wise.
        claim:
        In the resulting vector if any of the dimension is not either of 3,6,9
        then the three cards do not form a valid set
        reason: 
        valid combination of attribute value for each dimensions are
        1+1+1 = 3
        2+2+2 = 6
        3+3+3 = 9
        1+2+3 = 6
        
        invalid combination of attribute value for each dimensions are
        1+2+2 = 5
        1+1+2 = 4
        1+3+3 = 7
        1+1+3 = 5
        2+2+3 = 7
        2+3+3 = 8
        
        set of valid sums and invalid sums are mutually exclusive
        
        Args:
            triplet(list of int):  set of 3 cards
            
        Returns:
            True if triplet is a valid set
            else False
        
        '''
        # Add the three cards along each dimension(attribute)
        sumOfCards = map(sum, zip(self.cards[triplet[0]],self.cards[triplet[1]],self.cards[triplet[2]]))
        for i in sumOfCards:
            if i!=3 and i!=6 and i!=9:
                return False
        return True
            
    def getSets(self, curCards, attr):
        '''
        This is a recursive function
        curCards - current set of cards that are under consideration
        attr - current attr under consideration
        
        Logic:
        For each attribute, all the three cards should have the same value
        of the attribute or all different.
        So we group the cards with values of current attribute(attr)
        and recurse for each group if we want the attribute to be equal in all
        the three cards or find exhaustively all valid sets containing different 
        values for the current attribute (no recursion)
        
        Args:
            curCards(list of int): Current Working set of Cards
            
        Returns:
            sets(list of int triplets) : All possible sets of valid triplets formed from the curCards
        
        
        '''
        # to store groups
        groups = [[],[],[]]
        [groups[self.cards[k][attr]-1].append(k) for k in curCards]
        
        #to store and return valid sets
        sets = []
        
        # if the value of the current attribute is same
        for grp in groups:
            # we cannot form a valid set with less than 3 cards
            if len(grp)<3:
                continue
            
            # recurse with the next attribute, as all the cards are distinct
            # recursion won't go past attr 4, else it would mean that there are identical cards.
            sets += self.getSets(grp,attr+1)  
            
        # if the value of the current attribute is different in the three cards    
        # brute force valid set check for all triplets, one from each group                                    
        sets += [(i,j,k) for i in groups[0] for j in groups[1] for k in groups[2] if self.isSet((i, j, k))]
        
        return sets
    
    
    def setSets(self, sets):
        self.sets = sets
        
    def makeCompatibleList(self):
        '''
        We form a dictionary list of compatibility for each valid set that we discovered
        For each valid set, we find all other valid sets which do not overlap with it.
        We use indices to represent the valid sets
        
        Updates class variable compatible
        '''
        # dictionary storing the compatibility list for each valid set
        compatible = {}
        for i in xrange(len(self.sets)):
            compatible[i] = [ setKey for setKey in xrange(i+1, len(self.sets))
                            if testOverlap(self.sets[i], self.sets[setKey])]
        self.compatible = compatible


    def findMaxSet(self,curCompatible):
        '''
        We do a DFS in the search space of possibilities. 
        This function returns the maxSet of valid sets given the current valid sets.
        Initially maxSet can contain any of the valid sets that we have,
        so, curCompatibility is all valid sets initially.
        
        After we pick one valid set, the set of possible valid sets that are disjoint with it
        reduce, we can get the possible valid sets by finding the intersection of curCompatibility 
        and the list of compatible valid sets for the valid set we picked. 
        We now update the curCompatibility and recurse.
        
        Args:
            curCompatible(list of int triplets): Current Possible Compatible Valid sets 
            
        Returns:
            maxSet(list of int triplets) : Maximum Possible Disjoint Valid Sets from the given curCompatible valid sets
        
        '''
        maxSet = []
        for triplet in curCompatible:
            curSet = self.findMaxSet(set(self.compatible[triplet]).intersection(curCompatible))
            
            # We append the current triplet(valid set) with the best maxSet of the rest
            curSet.append(triplet)
            if len(curSet)>len(maxSet):
                maxSet = curSet
        # return maximum valid disjoint triplets
        return maxSet
    
    def prettyPrint(self,triplets):
        for triplet in triplets:
            for card in self.sets[triplet]:
                print self.strCards[card]
            print ''
        
    def run(self):
        '''
        reads input from file and calls relevant functions to complete the given task
        '''
        self.readInput()
        sets = self.getSets(range(self.N),0)
        self.sets = sets
        self.makeCompatibleList()
        self.maxSet = self.findMaxSet(range(len(self.sets)))
        print len(self.sets)
        print len(self.maxSet)
        print ''
        self.prettyPrint(self.maxSet)
        
def main():
    '''
    This program can take input from either file or stdIN
    for input from file 
    use: S = SetGame('input.txt')
    for input from stdIN
    use: S = SetGame()
    '''
    # Input from file
    #S = SetGame('input2.txt')
    
    # Input from stdin
    S = SetGame()
    S.run()

if __name__ == "__main__":
    main()