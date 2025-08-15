"""
Binary Search Tree Implementation
Created by: claude-agent-api-documenter
Model: Claude Sonnet 4

A comprehensive implementation of a Binary Search Tree with insert, delete, 
and search operations, including extensive documentation and examples.
"""

class TreeNode:
    """
    Node class for Binary Search Tree.
    
    Attributes:
        val (int): The value stored in the node
        left (TreeNode): Reference to left child
        right (TreeNode): Reference to right child
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinarySearchTree:
    """
    Binary Search Tree implementation with comprehensive operations.
    
    This implementation provides O(log n) average case performance for
    insert, delete, and search operations on a balanced tree.
    """
    
    def __init__(self):
        """Initialize an empty BST."""
        self.root = None
    
    def insert(self, val):
        """
        Insert a value into the BST.
        
        Args:
            val (int): Value to insert
            
        Returns:
            bool: True if insertion successful, False if value already exists
            
        Time Complexity: O(log n) average, O(n) worst case
        Space Complexity: O(log n) due to recursion stack
        """
        if self.root is None:
            self.root = TreeNode(val)
            return True
        
        return self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        """Helper method for recursive insertion."""
        if val == node.val:
            return False  # Value already exists
        
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
                return True
            return self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
                return True
            return self._insert_recursive(node.right, val)
    
    def search(self, val):
        """
        Search for a value in the BST.
        
        Args:
            val (int): Value to search for
            
        Returns:
            bool: True if value found, False otherwise
            
        Time Complexity: O(log n) average, O(n) worst case
        Space Complexity: O(log n) due to recursion stack
        """
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        """Helper method for recursive search."""
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val):
        """
        Delete a value from the BST.
        
        Args:
            val (int): Value to delete
            
        Returns:
            bool: True if deletion successful, False if value not found
            
        Time Complexity: O(log n) average, O(n) worst case
        Space Complexity: O(log n) due to recursion stack
        """
        original_root = self.root
        self.root = self._delete_recursive(self.root, val)
        return self.root != original_root or (original_root and original_root.val == val)
    
    def _delete_recursive(self, node, val):
        """Helper method for recursive deletion."""
        if node is None:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Node has two children - find inorder successor
                successor = self._find_min(node.right)
                node.val = successor.val
                node.right = self._delete_recursive(node.right, successor.val)
        
        return node
    
    def _find_min(self, node):
        """Find the minimum value node in a subtree."""
        while node.left is not None:
            node = node.left
        return node
    
    def inorder_traversal(self):
        """
        Perform inorder traversal of the BST.
        
        Returns:
            List[int]: Values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper method for inorder traversal."""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
    
    def is_empty(self):
        """Check if the BST is empty."""
        return self.root is None
    
    def height(self):
        """
        Calculate the height of the BST.
        
        Returns:
            int: Height of the tree (0 for empty tree)
        """
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Helper method for calculating height."""
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                      self._height_recursive(node.right))


# Example usage and testing
if __name__ == "__main__":
    # Create a new BST
    bst = BinarySearchTree()
    
    # Test insertions
    print("=== Binary Search Tree Demo ===")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
    
    print(f"Inserting values: {values}")
    for val in values:
        success = bst.insert(val)
        print(f"Insert {val}: {'Success' if success else 'Failed (duplicate)'}")
    
    # Test duplicate insertion
    print(f"\nTrying to insert duplicate value 50: {bst.insert(50)}")
    
    # Test search operations
    print("\n=== Search Operations ===")
    search_values = [25, 35, 45, 80, 100]
    for val in search_values:
        found = bst.search(val)
        print(f"Search {val}: {'Found' if found else 'Not found'}")
    
    # Display tree structure
    print(f"\n=== Tree Structure ===")
    print(f"Tree height: {bst.height()}")
    print(f"Inorder traversal (sorted): {bst.inorder_traversal()}")
    
    # Test deletion operations
    print("\n=== Delete Operations ===")
    delete_values = [10, 30, 50]  # Delete leaf, node with one child, node with two children
    for val in delete_values:
        success = bst.delete(val)
        print(f"Delete {val}: {'Success' if success else 'Not found'}")
        print(f"Tree after deletion: {bst.inorder_traversal()}")
    
    print(f"\nFinal tree height: {bst.height()}")