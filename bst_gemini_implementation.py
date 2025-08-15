"""
Binary Search Tree - Cost-Optimized Implementation
Created by: gemini-agent-cost-optimizer
Model: Gemini 1.5 Flash

Efficient BST implementation focusing on core functionality with minimal overhead.
Optimized for performance and reduced complexity.
"""

class Node:
    """Simple node structure for BST."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    """
    Cost-optimized Binary Search Tree with essential operations.
    Focuses on simplicity and efficiency.
    """
    
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        """Insert value into BST. Returns True if successful."""
        if not self.root:
            self.root = Node(data)
            return True
        
        current = self.root
        while True:
            if data == current.data:
                return False  # Duplicate
            
            if data < current.data:
                if not current.left:
                    current.left = Node(data)
                    return True
                current = current.left
            else:
                if not current.right:
                    current.right = Node(data)
                    return True
                current = current.right
    
    def search(self, data):
        """Search for value in BST. Returns True if found."""
        current = self.root
        while current:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False
    
    def delete(self, data):
        """Delete value from BST. Returns True if successful."""
        self.root, deleted = self._delete_node(self.root, data)
        return deleted
    
    def _delete_node(self, node, data):
        """Helper method for deletion."""
        if not node:
            return node, False
        
        deleted = False
        
        if data < node.data:
            node.left, deleted = self._delete_node(node.left, data)
        elif data > node.data:
            node.right, deleted = self._delete_node(node.right, data)
        else:
            deleted = True
            # Node to delete found
            if not node.left:
                return node.right, deleted
            elif not node.right:
                return node.left, deleted
            
            # Node with two children
            min_node = self._find_min(node.right)
            node.data = min_node.data
            node.right, _ = self._delete_node(node.right, min_node.data)
        
        return node, deleted
    
    def _find_min(self, node):
        """Find minimum value node."""
        while node.left:
            node = node.left
        return node
    
    def to_list(self):
        """Return sorted list of all values."""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        """Inorder traversal helper."""
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)


# Quick test function
def test_bst():
    """Efficient testing function."""
    bst = BST()
    
    # Test data
    data = [5, 3, 7, 2, 4, 6, 8]
    
    # Insert
    print("Inserting:", data)
    for x in data:
        bst.insert(x)
    
    # Search
    print("Tree contents:", bst.to_list())
    print("Search 4:", bst.search(4))
    print("Search 9:", bst.search(9))
    
    # Delete
    print("Deleting 3...")
    bst.delete(3)
    print("After deletion:", bst.to_list())

if __name__ == "__main__":
    test_bst()