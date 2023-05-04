import BKtree
from misc_functions import edit_distance

a = BKtree(edit_distance)
a.insert("hello", 5)
a.insert("hi", 1)
a.update("hello", 4)
a.update("hi", 7)

for x in [("test", 3), ("foodie", 7), ("Boobies", 70)]:
    a.insert(*x)