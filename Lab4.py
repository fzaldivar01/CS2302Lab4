#CS 2302 Lab #4 B-trees
# Programmed by Olac Fuentes, modified by Fernando Zaldivar
# Last modified March 15,2018

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
    
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6,7,8,9,12,13,14,15,16,17]

T = BTree()    
for i in L:
    #print('Inserting',i)
    Insert(T,i)
    #PrintD(T,'') 
    #Print(T)
    #print('\n####################################')
   



# return a sorted list of all the elemnts in B tree
def sortedList(T):
    L=[]

    if T.isLeaf:
        for i in range (len(T.item)):
            L.append(T.item[i])
        return L
    else:
        for i in range (len(T.item)):
            L.append(sortedList(T.child[i]))
            L.append(T.item[i])
        L.append(sortedList(T.child[len(T.item)]))
    return L
# rerurn the smallest element at a given depth
def minElement(T,d):
    if d == 0:
        return T.item[0]
    if T.isLeaf:
        return None
    else:
        return minElement(T.child[0], d-1)
# rerurn the largest element at a given depth
def maxElement(T,d):
    if d ==0:
        return T.item[-1]
    if T.isLeaf:
        return None
    else:
        return maxElement(T.child[-1],d-1)
# return the number of nodes at a certain depth
def nodeCount(T,d):
    if d > height(T):
        return None   
    if d == 0:
        return len(T.item)

    else:
        count =0
        for i in range(len(T.child)):
            count +=nodeCount(T.child[i], d-1)
        return count
# print the nodes at a given depth
def printAtDepth(T,d):
    if d == 0:
        print(T.item)
    else:
        for i in range(len(T.child)):
            printAtDepth(T.child[i], d-1)
#returns the number of leaves that are full
def fullLeaves(T):
    if T.isLeaf:
        if IsFull(T):
            return 1
        else:
            return 0
    count =0
    for i in range (len(T.child)):
        count += fullLeaves(T.child[i])
    return count
# returns the amount of nodes that are full
def fullNodes(T):
    if T.isLeaf:
        if IsFull(T):
            return 1
    
    if IsFull(T):
        count =1
        for i in range (len(T.child)):
            count += fullNodes(T.child[i])
        return count
    else:
        count =0
        for i in range (len(T.child)):
            count += fullNodes(T.child[i])
        return count
# looks for 'k' and retuns the depth it is located at
def searchDepth(T,k):
    if k in T.item:
        return 0
    else:
        count =0
        for i in range (len (T.child)):
            count = 1 + searchDepth(T.child[i],k)
        if Search(T,k) is None:
            return -1
        return count
        

print('height of the tree ',height(T))
print('the min element at depth ',minElement(T,2))
print('the max element at depth ',maxElement(T,2))
print('the number of nodes at  a depth is ',nodeCount(T,2))
print('nodes at depth' ,printAtDepth(T,1))
print('number of full leaves ',fullLeaves(T))
print('number of full nodes ',fullNodes(T))


print('k is at depth ',searchDepth(T,200))
print(sortedList(T))

#Print(T)
PrintD(T, ' ')