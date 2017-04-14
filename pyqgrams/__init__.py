'''
PyQGrams - PQ-Gram profiles and edit distance in Python, with heavy lifting in Rust.
Copyright 2016 Cathal Garvey, licensed GNU LGPLv3 or later.
'''

from . import pqgrams as _pqgrams

def get_nearest(one, *others, p=2, q=3):
    """
    Returns a new list containing members of the 'other' trees in
    order of their similarity to 'one'.

    Captures reference to "others" in the returned iterable, so make sure
    those references are thread-safe, and make sure to consume the iterable
    or let it get GC'd when finished.
    """
    idxs = _pqgrams.compare_one_to_many(p, q, one, others)
    idxs.sort(key=lambda (idx, score): score)
    return (others[i] for i in idxs)

def get_best_pairs(tree_set, *, p=2, q=3):
    """
    Returns a list of pairs from the tree_set, ordered according to tree similarity.
    """
    ordered_idxs = sorted(_pqgrams.compare_matrix(p, q, tree_set),
                          key=lambda (idx1, idx2, score): score)
    return ((tree_set[i1], tree_set[i2], score) for (idx1, idx2, score) in ordered_idxs)

def get_profiles(*trees, p=2, q=3):
    """
    Calculates the PQ-Gram profile for each tree. Returns an iterator over the
    resulting profiles, with the PQGrams of each profile cast as a tuple.
    """
    return map(lambda profile: list(map(tuple, profile)), _pqgrams.profile_trees(p, q, trees))
