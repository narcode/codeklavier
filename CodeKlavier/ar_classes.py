"""
AR extension classes and helper functions
"""

from Mapping import Mapping_CKAR

class CkAR(object):
    """Main class for the AR extension"""
    
    def __init__(self):
        self.trees = 1
        self.mapping = Mapping_CKAR()
        self.navigate = 0
        
    def nextT(self):
        """ 
        Traverse the LS trees forward
        """
        self.navigate = self.navigate+1
        if self.navigate == self.trees:
            self.navigate = 0
        nextt = (self.navigate+self.trees)%self.trees
        print('go to next tree', nextt)
        self.mapping.websocketSend(self.makeJson('view', str(nextt)))
        
    
    def currentTree(self):
        return (self.navigate+self.trees)%self.trees
        
    def prev(self):
        """ 
        Traverse LS trees backward
        """
        self.navigate = self.navigate-1
        if self.navigate > self.trees:
            self.navigate = 0
        prev = (self.trees + self.navigate)%self.trees
        self.mapping.websocketSend(self.makeJson('view', str(prev)))
        print('go to previous tree', prev)

    def create(self):
        """ 
        Create a new LS tree
        """
        self.trees = self.trees + 1
        print('create new tree', 'total trees: ', self.trees)
        self.mapping.websocketSend(self.makeJson('view', str(self.trees) ))
        
    def select(self, tree=0):
        """ Select a specific LS tree by ID
        """
        print('select tree id:', tree)
        
    def collect(self, tree=0):
        """Collect a LS-tree for parallel processing"""
        print('collect tree id:', tree)    
        
    def makeJson(self, lstype='lsys', payload=''):
        return self.mapping.prepareJson(lstype, payload)
        

    
    