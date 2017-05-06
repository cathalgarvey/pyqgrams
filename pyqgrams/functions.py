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
    Returns the PQ-Gram profile for the given P and Q for each tree.
    The returned profiles use the `filler` parameter to fill in PQ-Grams that
    contain padding nodes; in the paper these are denoted '*' and this value
    is probably appropriate for XML/HTML trees.

    Because LXML gives a unique "tag" attribute to all comment nodes in a tree,
    this function strips comments before profiling. This behaviour can be disabled
    using `decomment=False`.

    Because decommenting trees passed to this function silently might cause
    problems elsewhere, this function deep-copies tree objects by default before
    decommenting. This deep-copy can be disabled with `clone_tree=False` (in
    which case trees passed to this function will be decommented; beware!), or
    by disabling decommenting altogether.
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
