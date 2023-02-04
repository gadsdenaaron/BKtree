def _edit_dist_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i  # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j  # row 0: 0,1,2,3,4,...
    return lev


def _last_left_t_init(sigma):
    return {c: 0 for c in sigma}


def _edit_dist_step(
    lev, i, j, s1, s2, last_left, last_right, substitution_cost=1, transpositions=False
):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (substitution_cost if c1 != c2 else 0)

    # transposition
    d = c + 1  # never picked by default
    if transpositions and last_left > 0 and last_right > 0:
        d = lev[last_left - 1][last_right - 1] + i - last_left + j - last_right - 1

    # pick the cheapest
    lev[i][j] = min(a, b, c, d)


def edit_distance(s1, s2, substitution_cost=1, transpositions=False):
    """
    Calculate the Levenshtein edit-distance between two strings.
    The edit distance is the number of characters that need to be
    substituted, inserted, or deleted, to transform s1 into s2.  For
    example, transforming "rain" to "shine" requires three steps,
    consisting of two substitutions and one insertion:
    "rain" -> "sain" -> "shin" -> "shine".  These operations could have
    been done in other orders, but at least three steps are needed.
    Allows specifying the cost of substitution edits (e.g., "a" -> "b"),
    because sometimes it makes sense to assign greater penalties to
    substitutions.
    This also optionally allows transposition edits (e.g., "ab" -> "ba"),
    though this is disabled by default.
    :param s1, s2: The strings to be analysed
    :param transpositions: Whether to allow transposition edits
    :type s1: str
    :type s2: str
    :type substitution_cost: int
    :type transpositions: bool
    :rtype: int
    """
    # set up a 2-D array
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)

    # retrieve alphabet
    sigma = set()
    sigma.update(s1)
    sigma.update(s2)

    # set up table to remember positions of last seen occurrence in s1
    last_left_t = _last_left_t_init(sigma)

    # iterate over the array
    # i and j start from 1 and not 0 to stay close to the wikipedia pseudo-code
    # see https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    for i in range(1, len1 + 1):
        last_right_buf = 0
        for j in range(1, len2 + 1):
            last_left = last_left_t[s2[j - 1]]
            last_right = last_right_buf
            if s1[i - 1] == s2[j - 1]:
                last_right_buf = j
            _edit_dist_step(
                lev,
                i,
                j,
                s1,
                s2,
                last_left,
                last_right,
                substitution_cost=substitution_cost,
                transpositions=transpositions,
            )
        last_left_t[s1[i - 1]] = i
    return lev[len1][len2]

class BKtree:

    """Python Implementation of a Burkhard-Keler tree"""

    def __init__(self, distance_function):
        self.distance_function = distance_function
        self.root = None
        self.itemset = {}

    def search(self, key_string: str):
        
        if key_string in self.itemset:
            return self.itemset[key_string]

        else:
            pass

    def insert(self, key_string: str, value):
        
        if self.root == None:
            self.itemset[key_string] = value
            self.root = BKnode(key_string, value, self.distance_function)
        else:
            if key_string in self.itemset:
                raise KeyError

            else:
                self.itemset[key_string] = value
                self.root.add_child(key_string, value)

    def update(self, key_string: str, new_value):
        
        if self.root == None:
            raise KeyError
        else:
            self.root.update_child(key_string, new_value)

    def depth(self):
        pass

    def __len__(self):
        pass

    def __repr__(self):
        return f"{self.root}"

    def __contains__(self):
        pass

    
class BKnode:

    def __init__(self, key_string: str, value, distance_function):
        self.key_string = key_string
        self.value = value
        self.children = {}
        self.distance_function = distance_function

    def add_child(self, child_string: str, child_value: str):
        
        distance = self.distance_function(child_string, self.key_string)

        if distance in self.children:
            self.children[distance].add_child(child_string, child_value)
        else:
            self.children[distance] = BKnode(child_string, child_value, self.distance_function)

    def update_child(self, key_string: str, new_value):
        
        if self.key_string == key_string:
            self.value = new_value

        else:
            distance = self.distance_function(key_string, self.key_string)

            if distance in self.children:
                self.children[distance].update_child(key_string, new_value)
            else:
                raise KeyError
            
    def __repr__(self):
        return f"key - {self.key_string}, value - {self.value}, children - {self.children}"



a = BKtree(edit_distance)
a.insert("hello", 5)
a.insert("hi", 1)
a.update("hello", 4)
a.update("hi", 7)

for x in [("test", 3), ("foodie", 7), ("Boobies", 70)]:
    a.insert(*x)