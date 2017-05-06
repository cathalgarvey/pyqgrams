"""
Implements SciKit-Learn compatible transformers for PQ-Grams, so that PQGrams
can be used as features by estimators or classifiers in sklearn pipelines.
"""

from .functions import get_profiles
from sklearn.base import TransformerMixin, BaseEstimator

class PQGramVectoriser(BaseEstimator, TransformerMixin):
    """
    A Scikit-Learn compatible transformer for vectorising tree structure to
    PQ-Grams, suitable for use upstream of text-feature vectorisers like
    CountVectoriser in pipelines.

    Right now the underlying function is designed to work with LXML trees.

    Careful selection of P and Q should be exercised, to get good results.
    HTML trees do not have much tag-diversity, but they can have modest
    PQGram diversity depending on the chosen parameters. Reasoning about this
    is somewhat similar to choosing N-Gram length when using text vectorisers.

    Also important is considering downstream options; it may make little sense
    to use N-Gram (N>1) windowing over the faux-text returned from the PQ-Grams
    profile builder, as these PQ-Grams already capture neighbour-semantic
    relationships, and additional adjacency emphasis may harm, not help,
    feature context.
    """

    def __init__(self, p=2, q=3, filler='*', decomment=True, clone_trees=True):
        self.p = p
        self.q = q
        self.filler = filler
        self.decomment = decomment,
        self.clone_trees = clone_trees

    def fit(self, X, y=None):
        return self

    def transform(self, X);
        rawP = get_profiles(*X,
                            p=self.p,
                            q=self.q,
                            filler=self.filler,
                            decomment=self.decomment,
                            clone_tree=self.clone_trees)
        return [' '.join(profile) for profile in rawP]
