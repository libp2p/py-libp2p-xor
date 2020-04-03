from .events import *
import key
import trie


def compute_expected_fill(events: Event):
    # compute the last known state of each peer
    state = {}  # peer -> state
    for e in events:
        for p in e.heard():
            state[p] = "heard"
        for p in e.waiting():
            state[p] = "waiting"
        for p in e.queried():
            state[p] = "queried"
        for p in e.unreachable():
            state[p] = "unreachable"
    # add all peers eligible for the routing table to a trie
    eligible = trie.Trie()
    for p in state:
        if state[p] in ["heard", "queried"]:
            eligible.add(p)
    return bucket_fill_for_trie(events[0].node, eligible)


def bucket_fill_for_trie(node: key.Key, eligible: trie.Trie):
    print("num eligible", eligible.size())
    fill = []
    finger = eligible
    for depth in range(node.bit_len()):
        dir = node.bit_at(depth)
        if finger.is_leaf():
            break
        else:
            fill.append(finger.branch[1 - dir].size())
            finger = finger.branch[dir]
    return fill
