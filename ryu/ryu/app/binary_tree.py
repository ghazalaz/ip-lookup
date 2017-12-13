
from sys import argv
from datetime import datetime

class Node:
    
    def __init__(self, value):
        self.left = None
        self.nexthop = value
        self.right = None

class BinaryTree() :
    def __init__(self,table):
        self.root = Node("*")
        self.setTable(table)

    def createNode(self, nexthop):
        return Node(nexthop)


    def traverseInorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traverseInorder(root.left)
            print(root.nexthop)
            self.traverseInorder(root.right)

    def traversePreorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            print root.nexthop
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)

    def traversePostorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)
            print root.nexthop

    def setTable(self,table):
        for rec in table:
            self.insert(self.root,rec,table[rec])

    def insert(self,node,prefix,nexthop,index = 0):
        
        if index == len(prefix) :
            if node is None:
                return self.createNode(nexthop)
            else:
                node.nexthop = nexthop
                return node
        
        if node is None:
            node = self.createNode(None)
    
        if prefix[index] == '0' :
            leftnexthop = None
            if node.left != None:
                leftnexthop = node.left.nexthop
            node.left = self.insert(node.left,prefix,nexthop,index+1)

            if leftnexthop != None and node.left.nexthop == None:
                node.left.nexthop = leftnexthop

            
        if prefix[index] == '1' :
            rightnexthop = None
            if node.right != None:
                rightnexthop = node.right.nexthop
                
            node.right = self.insert(node.right,prefix,nexthop,index+1)
            if rightnexthop != None and node.right.nexthop == None:
                node.right.nexthop = rightnexthop

            
        return node

    def search(self,ip):
        return self.inner_search(self.root,ip,0)

    def inner_search(self,node,ip,index ):
        if index == len(ip) :
            return node.nexthop

        nexthop = node.nexthop    
        if ip[index] == '0':
            if node.left != None:
                nexthop = self.inner_search(node.left,ip,index+1)
        if ip[index] == '1':
            if node.right != None:
                nexthop = self.inner_search(node.right,ip,index+1)
        
        if nexthop != None:
            return nexthop
        else:
            return node.nexthop    
        

class DisjointBT(BinaryTree):
    def __init__(self,table):
        BinaryTree.__init__(self,table)


    def searchtoinsert(self, node,prefix,index=0):
       while(index<=len(prefix)):
            if node.nexthop==None:
            # print "nago yeki shodan"
                return node

            nexthop = node.nexthop
            if node.left == None and node.right!= None:
                #nodeprev=node
                print "to left"
                self.createNode(nexthop)
                searchtoinsert(node.right,prefix,index+1)

            if node.right == None and node.left!=None:
                #nodeprev=node
                print "to right"
                self.createNode(nexthop)
                searchtoinsert(node.left,prefix,index+1)

    def pushToLeaf(self,node):
        flag = False
        if node.right != None:
            #print "{0} to right".format(node.nexthop)
            if node.right.nexthop == None:
                #print "{0} pushed to right".format(node.nexthop)
                node.right.nexthop = node.nexthop 
                flag = True
            self.pushToLeaf(node.right)
        if node.left != None:
            #print "{0} to left".format(node.nexthop)
            if node.left.nexthop == None:
                #print "{0} pushed to left".format(node.nexthop)
                node.left.nexthop = node.nexthop 
                flag = True
            self.pushToLeaf(node.left)
        if node.left != None and node.right == None:
            #print "{0} pushed to right".format(node.nexthop)
            node.right = self.createNode(node.nexthop)
            flag = True
        if node.left == None and node.right != None:
            #print "{0} pushed to left".format(node.nexthop)
            node.left = self.createNode(node.nexthop)
            flag = True
            
        if flag == True:
            node.nexthop = None

    def search(self,ip):
        return self.inner_search(self.root,ip)
    def inner_search(self,node,ip,index = 0):
        #print node.nexthop
        if node.right == None and node.left == None :
            return node.nexthop

        if ip[index] == '0':
            if node.left != None:
                return self.inner_search(node.left,ip,index+1)
        if ip[index] == '1':
            if node.right != None:
                return self.inner_search(node.right,ip,index+1)
        
class CompleteBT(BinaryTree):
    def __init__(self,max_length,table):
        self.root = Node("*")
        self.max_length = max_length
        self.lookup = {}
        self.setTable(table)

    def setTable(self,table):
        for rec in table:
            self.insert(self.root,rec,table[rec])

    def insert(self,node,prefix,nexthop,index = 0):
        #if index == len(prefix) :
        if index == self.max_length:
            self.lookup[prefix] = nexthop
            if node is None:
                return self.createNode(nexthop)
            else:
                node.nexthop = nexthop
                return node
        
        if node is None:
            node = self.createNode(None)

        if index >= len(prefix):
            leftnexthop = None
            if node.left != None:
                leftnexthop = node.left.nexthop
            node.left = self.insert(node.left,prefix+"0",nexthop,index+1)

            if leftnexthop != None and node.left.nexthop == None:
                node.left.nexthop = leftnexthop

            rightnexthop = None
            if node.right != None:
                rightnexthop = node.right.nexthop
                
            node.right = self.insert(node.right,prefix+"1",nexthop,index+1)
            if rightnexthop != None and node.right.nexthop == None:
                node.right.nexthop = rightnexthop
            return node

        if prefix[index] == '0' :
            leftnexthop = None
            if node.left != None:
                leftnexthop = node.left.nexthop
            node.left = self.insert(node.left,prefix,nexthop,index+1)

            if leftnexthop != None and node.left.nexthop == None:
                node.left.nexthop = leftnexthop

            
        if prefix[index] == '1' :
            rightnexthop = None
            if node.right != None:
                rightnexthop = node.right.nexthop
                
            node.right = self.insert(node.right,prefix,nexthop,index+1)
            if rightnexthop != None and node.right.nexthop == None:
                node.right.nexthop = rightnexthop

            
        return node


    def search(self,ip):
        return self.lookup[ip[0:self.max_length]]



