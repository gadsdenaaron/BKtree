

from typing import Any, Callable, List, Tuple
class BKtree:
    """
    Implementation of a Burkhard-Keller tree (used as a dictionary) for use in problems involving discret metric spaces, for example levenshtein distance on strings
    You can use a BK tree ti fasten the runtime of a problem involving a search for all the strings at most D (edit) distance away from search string S in a list L
    by first making a BK tree of L and then searching the BK tree for S.
    """

    def __init__(self, distance_function: Callable[[str, str], int]) -> None:
        self.distance_function = distance_function
        self.root = None
        self.itemDict = {}
        self.isempty = True

    def insert(self, key_string: str, value: Any) -> None:
        """
        Inserts a string into the BKtree

        Args:
            key_string: The string to be inserted.
            value     : The corresponding vlaue of the given key_string.

        Returns:
            This method does not return anyuthing, instead modifies the given tree

        Raises:
            KeyError if the key string supplied is already in the tree.
        """

        if key_string in self.itemDict:
            raise KeyError(f"{key_string} already in the BKtree cannot use insert to reassign dictionary values")
        else:
            self.itemDict[key_string] = value

            if self.isempty:
                self.rootNode = BKnode(key_string, self.distance_function)
                self.isempty  = False
            
            else:
                self.rootNode.add_child(key_string)

    def find_all_similar(self, search_word:str, limit: int) -> List[Any]:
        """
        Searches the BKtree for the seach_word, returns a list if possible (key, value, distance) tuples

        Args:
        search_word: the key to seach for in the dictionary
        limit: an integer

        Returns:
            A list of (key, value, distance) tuples of similar words from the tree
        """

        possible_words = self.rootNode.find(search_word, limit)
        return [(key, self.itemList[key], distance) for key, distance in possible_words]


    def find_closest_match():
        pass

    
    
class BKnode:

    def __init__(self, key_string: str, distance_function: Callable[[str, str], int]) -> None:
        self.key_string = key_string
        self.children = {}
        self.distance_function = distance_function

    def add_child(self, child_string: str) -> None:
        
        distance = self.distance_function(child_string, self.key_string)

        if distance in self.children:
            self.children[distance].add_child(child_string)
        else:
            self.children[distance] = BKnode(child_string, self.distance_function)

    def find(self, search_word: str, limit: int) -> List[Tuple[str, int]]:

        d = self.distance_function(self.key_string, search_word)
        return_list = []

        if d<limit:
            return_list.append((self.key_string, d))
        if self.children:

            for key in self.children.keys():
                if key>d-limit or key<d+limit:
                    next_node = self.children[key].find(search_word, limit)
                    if next_node is not None:
                        return_list += next_node
        return return_list
            
    def __repr__(self):
        return f"key - {self.key_string}, children - {self.children}"

    def __eq__(self, other) -> bool:

        return self.key_string == other.key_string and self.childen == other.children and self.distance_function == other.distance_function

if __name__ == "__main__":
    pass