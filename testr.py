
import os
print("my module loaded...")


def with_global():
    nonlocal a1
    a1 = "This var in the textbody"
    print("isi a1:", a1)
    return a1


    