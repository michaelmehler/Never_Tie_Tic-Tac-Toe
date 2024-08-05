class Linked_List:
    
    class __Node:
        def __init__(self, val):
            self.val = val  
            self.next = None 
            self.prev = None 
    
    def __init__(self):
        self.__size = 0 
        self.__header = Linked_List.__Node(None)
        self.__trailer = Linked_List.__Node(None) 
        self.__header.next = self.__trailer 
        self.__trailer.prev = self.__header

    def __len__(self):
        return self.__size 
   
    #inserts at the back of the linked list 
    def append_element(self, val):
        new_node = Linked_List.__Node(val)
        current = self.__trailer.prev 
        new_node.next = self.__trailer 
        new_node.prev = current
        current.next = new_node 
        self.__trailer.prev = new_node 
        self.__size += 1 

    #inserts at specified element - throws an error if coder tries to insert at the back of the linked list using this method
    def insert_element_at(self, val, index):
        if index < 0 or index >= self.__size:
            raise IndexError 
        if index == self.__size:
            raise IndexError 
        current = self.__header.next 
        new_node = Linked_List.__Node(val)
        for k in range(0, index):
            current = current.next
        new_node.next = current
        new_node.prev = current.prev 
        current.prev.next = new_node
        current.prev = new_node
        self.__size += 1

    #removes an element at the specified index
    def remove_element_at(self, index):
        if index < 0 or index >= self.__size:
            raise IndexError
        current = self.__header.next
        for k in range(0, index):
            current = current.next
        current.prev.next = current.next
        current.next.prev = current.prev
        self.__size -= 1
        return current.val
    
    #returns the element at the specified index
    def get_element_at(self, index):
        if index < 0 or index >= self.__size:
            raise IndexError
        current = self.__header.next
        for k in range(0, index):
            current = current.next
        return current.val

    #rotates the entire linked list one place to the left
    def rotate_left(self):
        if self.__size == 0 or self.__size == 1:
            return 
        self.__trailer.prev.next = self.__header.next
        self.__header.next.prev = self.__trailer.prev
        self.__header.next = self.__header.next.next
        self.__header.next.prev = self.__header
        self.__trailer.prev = self.__trailer.prev.next
         
    #returns the linked list in a readable string format
    def __str__(self):
        if self.__size == 0:
            return "[ ]"
        result = "[ "
        current = self.__header.next 
        while current is not self.__trailer.prev:
            result += str(current.val) + ", "
            current = current.next
        result += str(current.val) + " ]" 
        return result 
        
    def __iter__(self):
        self.__current = self.__header.next 
        return self 

    def __next__(self):
        if self.__current == self.__trailer:
            raise StopIteration
        val = self.__current.val
        self.__current = self.__current.next 
        return val

    def __reversed__(self):
        reversed_list = Linked_List()
        current = self.__trailer.prev
        while current is not self.__header:
            reversed_list.append_element(current.val) 
            current = current.prev
        return reversed_list 

if __name__ == '__main__':
    pass