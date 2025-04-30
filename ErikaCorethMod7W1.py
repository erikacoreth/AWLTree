#ErikaCoreth mod 7 worksheet 1

#Create a tree node
class TreeNode(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1 #height of this node (starts at 1 for a leaf)

#AVL tree class with insert, delete, rotaions, and print
class AVLTree(object):
#Function to perform right rotation
#Used when tree is left-heavy
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        #perform rotation
        y.right = z
        z.left = T3
        #update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y #new root after rotation

    def leftRotate(self, z):
    #function to perform left rotation
    #used when tree is right-heavy
        y = z.right
        T2 = y.left
        #perform rotation
        y.left = z
        z.right = T2
        #update heights
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y #new root after rotation

    #returns the height of a node, or 0 if None
    def getHeight(self, root):
        if not root:
            return 0 #if no root node, return 0
        return root.height #if not 0, return the height

    #get balance factor of the node (left height - right height)
    def getBalance(self, root):
        if not root: #if no root node, return 0
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    #function to delete a node recursively
    def delete_node(self, root, data):
        #find the node to be deleted and remove it
        if not root:
            return root #value not found
        #recur down to find the node to delete
        elif data < root.data:
            root.left = self.delete_node(root.left, data)
        elif data > root.data:
            root.right = self.delete_node(root.right, data)
        else:
            #node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            #node with two children: get the inorder successor (smallest in right subtree)
            temp = self.getMinValueNode(root.right)
            root.data = temp.data #copy the inorder successor's value
            root.right = self.delete_node(root.right, temp.data) #delete the inorder successor

        if root is None:
            return root #if the tree had only one node
        # update the height
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:  #if left heavy, rotate right
            if data < root.left.data:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:  # if right heavy, rotate left
            if data > root.right.data:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    #returns the node with the smallest value in the subtree
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    #returns the node with the largest value in the subtree
    def getMaxValueNode(self, root):
        if root is None or root.right is None:
            return root
        return self.getMaxValueNode(root.right)

    #Recursively print tree structure
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            print(indent, end="")
            if last:
                print("R----", end="") #right child
                indent += "     "
            else:
                print("L----", end="") #left child
                indent += "|     "
            print(currPtr.data)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

    #Recursive insert method with balancing
    def insert_node(self, root, data):
        #find the correct location and insert the node (BST insertion)
        if not root: #if there is no root
            return TreeNode(data)
        #either insert left or right
        elif data < root.data:
            root.left = self.insert_node(root.left, data)
        else:
            root.right = self.insert_node(root.right, data)

        #update the height
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        #update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1: #if tallest right - balanceFactor > 1, rotate right
            if data < root.left.data:
                return self.rightRotate(root) #rotate the tree right
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1: #if unabalnce(tallest left - balanceFactor < -1), rotate left
            if data > root.right.data:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

#main function to interact with AVL Tree
def main():
    myTree = AVLTree()
    root = None
    inserted_values = set() #track values inserted into the tree

    while True:
        try:
            data = int(input("Enter a positive integer (or non-positive to quit): "))
        except ValueError: #non-integer asks user for again for a input
            print("Invalid input. Please enter a valid integer.")
            continue

        if data <= 0: #if integer is negative or 0, the program ends
            print("Exiting program.")
            break

        if data in inserted_values: #if integer exists, delete it and balance the tree
            print(f"{data} already in tree. Deleting...")
            root = myTree.delete_node(root, data)
            inserted_values.remove(data)
            print(f"After Deletion of {data}:")
            myTree.printHelper(root, "", True) #print tree after deletion
        else: #if integer entered is not yet there, insert it
            print(f"{data} not in tree. Inserting...")
            root = myTree.insert_node(root, data)
            inserted_values.add(data)
            print(f"After Insertion of {data}:")
            myTree.printHelper(root, "", True)


main()