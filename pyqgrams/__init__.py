'''
PyQGrams - PQ-Gram profiles and edit distance in Python, with heavy lifting in Rust.
Copyright 2016 Cathal Garvey, licensed GNU LGPLv3 or later.
'''

from . import pqgrams as _pqgrams
import copy

FILLER_NODE_VALUE = _pqgrams.FILLER_RANDOM_INT

def decomment_lxml(tree):
    """
    If you use PQGrams on LXML trees, the comment-tags may mess things up,
    because the "tag" of a comment is unique to that comment. This breaks
    lots of assumptions.

    The easiest remedy is to strip trees of comments before use with this
    library, which is all this function does.
    """
    import lxml.html
    import lxml.etree
    if not isinstance(tree, (lxml.etree._Element, lxml.html.HtmlElement)):
        return
    for desc in tree.iterdescendants():
        if isinstance(desc, lxml.html.HtmlComment):
            desc.drop_tag()


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
    return [others[i] for _,i,s in idxs]

def get_best_pairs_in_set(tree_list, *, p=2, q=3):
    """
    Returns a list of pairs from the tree_list, ordered according to tree similarity.

    Because this generates distances for each non-self pairing of trees, it
    will quickly become expensive as the number of input trees increases.

    NB: tree_list can be any *indexable* iterator; this is usually a list but not always.
    """
    ordered_idxs = sorted(_pqgrams.compare_matrix(p, q, tree_list),
                          key=lambda idxidxscore: idxidxscore[2])
    return [(tree_list[i1], tree_list[i2], score) for (i1, i2, score) in ordered_idxs]

def get_best_pairs_between_sets(tree_list_1, tree_list_2, *, p=2, q=3):
    """
    This returns a list of pairs of trees chosen between tree_list_1 and
    tree_list_2, with the highest-scoring pairs first and the lowest-scoring later.
    """
    ordered_idxs = sorted(_pqgrams.compare_many_to_many(p, 1, tree_list_1, tree_list_2),
                          key=lambda idxidxscore: idxidxscore[2])
    return [(tree_list_1[i1], tree_list_2[i2], score) for (i1, i2, score) in ordered_idxs]

def get_profiles(*trees, p=2, q=3, clone_tree=True, decomment=True, filler='*'):
    """
    Calculates the PQ-Gram profile for each tree. Returns an iterator over the
    resulting profiles, with the PQGrams of each profile cast as a tuple.

    Profiles consist of 64-bit integers. The PQGrams algorithm creates "filler" nodes,
    which denote the "extended" nodes added to a tree during the algorithm; because
    Python hashes certain values (0, "") to the zero-integer, a randomly selected large
    integer is used for these nodes, instead. This value is available on this library
    as FILLER_NODE_VALUE, in case you need it.

    To get an accurate tree when dealing with LXML trees, comment-stripping is
    performed. To avoid headaches due to silently mutated trees, this copies the
    tree before stripping and profiling it. However, for performance or memory
    sensitive applications, you can disable this clone and the comment-stripping
    will be performed directly on the passed trees without a deep copy operation.
    If you know there are no comments in your trees, you can also disable
    'decomment' which will avoid the deep copy, too.
    """
    if decomment:
        if clone_tree:
            trees = list(map(copy.deepcopy, trees))
        [decomment_lxml(t) for t in trees]
    profiles, translation = _pqgrams.profile_trees(p, q, trees)
    translation[_pqgrams.FILLER_RANDOM_INT] = filler
    nuprofiles = []
    for prof in profiles:
        nuprof = []
        for gram in prof:
            nuprof.append(tuple([translation[i] for i in gram]))
        nuprofiles.append(nuprof)
    return nuprofiles
