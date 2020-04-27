from key import *
from trie import *
import numpy as np
import matplotlib.pyplot as plt

KEY_SIZE = 16


def build_balanced_random_trie(n):
    t = Trie()
    for i in range(n):
        k1, k2, k3 = choose_key(KEY_SIZE), choose_key(KEY_SIZE), choose_key(KEY_SIZE)
        d1, _ = t.add(k1)
        t.remove(k1)
        d2, _ = t.add(k2)
        t.remove(k2)
        d3, _ = t.add(k3)
        t.remove(k3)
        if d1 <= d2 and d1 <= d3:
            t.add(k1)
        elif d2 <= d1 and d2 <= d3:
            t.add(k2)
        else:
            t.add(k3)
    return t


def build_unbalanced_random_trie(n):
    t = Trie()
    for i in range(n):
        t.add(choose_key(KEY_SIZE))
    return t


def balanced_vs_unbalanced_depths(n):
    bal = build_balanced_random_trie(n)
    unbal = build_unbalanced_random_trie(n)
    bal_depths = bal.list_of_depths()
    unbal_depths = unbal.list_of_depths()
    fig, ax = plt.subplots(1)
    bins = np.linspace(0, 30, 30)
    ax.set_title("trie leaf depth distribution, {} peers".format(n))
    ax.set_ylabel('peers')
    ax.set_xlabel('leaf depth')
    ax.hist(bal_depths, bins, alpha=0.5, label='balanced')
    ax.hist(unbal_depths, bins, alpha=0.5, label='unbalanced')
    ax.legend(loc='upper right')
    plt.show()


# balanced_vs_unbalanced_depths(10000)
