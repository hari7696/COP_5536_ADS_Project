class TreeNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key, val):
        if not root:
            return TreeNode(key, val)
        elif key < root.key:
            root.left = self.insert(root.left, key, val)
        elif key > root.key:
            root.right = self.insert(root.right, key, val)
        else:
            root.val = val  # Update the value if the key already exists
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)

        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root

        elif key < root.key:
            root.left = self.delete(root.left, key)

        elif key > root.key:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.val = temp.val
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def rightRotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def inOrder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inOrder(root.left, result)
            result.append((root.key, root.val))
            self.inOrder(root.right, result)

        temp_dict = {}
        for item in result:
            temp_dict[item[0]] = item[1]
        return temp_dict


    def getSortedItems(self):
        return self.inOrder(self.root)
    
    def getNode(self, root, key):
        if root is None:
            return None
        if key < root.key:
            return self.getNode(root.left, key)
        elif key > root.key:
            return self.getNode(root.right, key)
        else:
            return root.val
        
    def update(self, root, key, new_val):
        if not root:
            return None
        if key < root.key:
            root.left = self.update(root.left, key, new_val)
        elif key > root.key:
            root.right = self.update(root.right, key, new_val)
        else:
            root.val = new_val
        return root

if __name__ == "__main__":
    # Driver code
    # avl = AVLTree()
    # avl.root = avl.insert(avl.root, 10, "Value 10")
    # avl.root = avl.insert(avl.root, 20, "Value 20")
    # avl.root = avl.insert(avl.root, 30, "Value 30")
    # avl.root = avl.insert(avl.root, 40, "Value 40")
    # avl.root = avl.insert(avl.root, 50, "Value 50")
    # avl.root = avl.insert(avl.root, 25, "Value 25")

    # print("Preorder traversal of the constructed AVL tree is")
    # avl.preOrder(avl.root)
    # print("\nSorted items in the AVL tree are")
    # print(avl.getSortedItems())

    # avl.root = avl.delete(avl.root, 20)
    # print("\nAfter deletion of 20")
    # print("Preorder traversal of the constructed AVL tree is")
    # avl.preOrder(avl.root)
    # print("\nSorted items in the AVL tree are")
    #print(avl.getSortedItems())

    # avl = AVLTree()   
    # avl.root = avl.insert(avl.root, 10, {"name": "Alice", "age": 30})
    # avl.root = avl.insert(avl.root, 20, {"name": "Bob", "age": 25})
    # avl.root = avl.insert(avl.root, 30, {"name": "Charlie", "age": 35})

    # # Printing the sorted items
    # print("\nSorted items in the AVL tree are")


    # new_value = {"name": "Bob", "age": 26}
    # avl.root = avl.insert(avl.root, 20, new_value)

    # # print(avl.getSortedItems())
    # # avl.root = avl.delete(avl.root, 20)
    # # print(avl.getSortedItems())
    # node_info = avl.getNode(avl.root, 100)
    # print(node_info)

    # Updating the age of the person with key 20
    # updated_value = avl.getNode(avl.root, 30).copy()
    # updated_value['age'] = 100
    # avl.root = avl.update(avl.root, 30, updated_value)

    # # Printing the sorted items
    # print("\nSorted items in the AVL tree after updating the age are")
    # print(avl.getSortedItems())
    pass
