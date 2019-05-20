"""
AR extension classes and helper functions
"""

from Mapping import Mapping_CKAR
import random

class CkAR(object):
    """Main class for the AR extension"""
    
    def __init__(self):
        self.trees = 1
        self.mapping = Mapping_CKAR()
        self.navigate = 0
        self._parallelTrees = []
        
    def nextT(self):
        """ 
        Traverse the LS trees forward
        """
        self.navigate = self.navigate+1
        if self.navigate == self.trees:
            self.navigate = 0
        nextt = (self.navigate+self.trees)%self.trees
        print('go to next tree', nextt+1)
        self.mapping.websocketSend(self.makeJson('view', str(nextt+1)))
        
    
    def currentTree(self):
        tree = (self.navigate+self.trees)%self.trees
        return (tree + 1)
        
    def prev(self):
        """ 
        Traverse LS trees backward
        """
        self.navigate = self.navigate-1
        if self.navigate > self.trees:
            self.navigate = 0
        prev = (self.trees + self.navigate)%self.trees
        self.mapping.websocketSend(self.makeJson('view', str(prev+1)))
        print('go to previous tree', prev+1)

    def create(self):
        """ 
        Create a new LS tree
        """
        self.trees = self.trees + 1
        self.navigate = self.trees - 1
        print('create new tree', 'total trees: ', self.trees)
        self.mapping.websocketSend(self.makeJson('view', str(self.trees) ))
        
    def select(self, tree=1):
        """ Select a specific LS tree by ID
        """
        print('select tree id:', tree)
        
    def drop(self, tree=1):
        """ Drop a specific tree from the collection """
        if tree in self._parallelTrees:
            self._parallelTrees.remove(tree)
        else: 
            print('\ntree not created yet or already collected, TREE:', tree, '\n')

        print('collected trees:', self._parallelTrees)
        
    def collect(self, tree=1):
        """Collect a LS-tree for parallel processing"""
        if tree not in self._parallelTrees and tree <= self.trees:
            self._parallelTrees.append(tree)
        else: 
            print('\ntree not created yet or already collected, TREE:', tree, '\n')
            
        print('collected trees:', self._parallelTrees)
        
    def transform(self):
        current = self.currentTree()
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        self.mapping.websocketSend(self.makeJsonTransform(str(current), [x,y,0]))
        print('transform tree', current)
        
    def makeJsonTransform(self, tree, position):
        return self.mapping.prepareJsonTransform(tree, position)
        
    def makeJson(self, lstype='lsys', payload=''):
        return self.mapping.prepareJson(lstype, payload)
    
    
        

    
    