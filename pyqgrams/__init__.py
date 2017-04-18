'''
PyQGrams - PQ-Gram profiles and edit distance in Python, with heavy lifting in Rust.
Copyright 2016 Cathal Garvey, licensed GNU LGPLv3 or later.
'''

from . import pqgrams as _pqgrams

FILLER_NODE_VALUE = _pqgrams.FILLER_RANDOM_INT

def get_nearest(one, *others, p=2, q=3):
    """
    Returns a new list containing members of the 'other' trees in
    order of their similarity to 'one'.

    Captures reference to "others" in the returned iterable, so make sure
    those references are thread-safe, and make sure to consume the iterable
    or let it get GC'd when finished.
    """
    idxs = _pqgrams.compare_many_to_many(p, q, [one], others)
    idxs.sort(key=lambda idx_score: idx_score[2])
    return (others[i] for _,i,s in idxs)

def get_best_pairs_in_set(tree_set, *, p=2, q=3):
    """
    Returns a list of pairs from the tree_set, ordered according to tree similarity.

    Because this generates distances for each non-self pairing of trees, it
    will quickly become expensive as the number of input trees increases.
    """
    ordered_idxs = sorted(_pqgrams.compare_matrix(p, q, tree_set),
                          key=lambda idxidxscore: idxidxscore[2])
    return ((tree_set[i1], tree_set[i2], score) for (i1, i2, score) in ordered_idxs)

def get_best_pairs_between_sets(tree_set_1, tree_set_2, *, p=2, q=3):
    """
    """
    ordered_idxs = sorted(_pqgrams.compare_many_to_many(p, 1, tree_set_1, tree_set_2),
                          key=lambda idxidxscore: idxidxscore[2])
    return ((tree_set_1[i1], tree_set_2[i2], score) for (i1, i2, score) in ordered_idxs)

def get_profiles(*trees, p=2, q=3):
    """
    Calculates the PQ-Gram profile for each tree. Returns an iterator over the
    resulting profiles, with the PQGrams of each profile cast as a tuple.

    Profiles consist of 64-bit integers. The PQGrams algorithm creates "filler" nodes,
    which denote the "extended" nodes added to a tree during the algorithm; because
    Python hashes certain values (0, "") to the zero-integer, a randomly selected large
    integer is used for these nodes, instead. This value is available on this library
    as FILLER_NODE_VALUE, in case you need it.
    """
    return map(lambda profile: list(map(tuple, profile)), _pqgrams.profile_trees(p, q, trees))
