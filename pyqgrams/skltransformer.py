"""
Implements SciKit-Learn compatible transformers for PQ-Grams, so that PQGrams
can be used as features by estimators or classifiers in sklearn pipelines.
"""

from .functions import get_profiles
from sklearn.base import TransformerMixin, BaseEstimator
import lxml.html
import html_text


class LxmlParseTransformer(BaseEstimator, TransformerMixin):
    """
    Helpful pipeline-compatible way to parse HTML strings into LXML trees.
    Handy if you want to use PQGramVectoriser in a FeatureUnion where other
    feature extractors don't want LXML; just put this transformer above the
    PQGramVectoriser portion only and give raw strings to the pipeline.

    Putting this in a pipeline with PQGramVectoriser is necessary to permit
    parallel execution, for example using sklearn.model_selection.GridSearchCV's
    'n_jobs' parameter. If using this upstream of PQGramVectoriser, the trees
    produced are probably discarded shortly after creation, so disable the
    clone_trees option in PQGarmVectoriser for efficiency.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [lxml.html.fromstring(x) for x in X]


class HtmlToTextTransformer(BaseEstimator, TransformerMixin):
    """
    To help facilitate union-pipelines where other branches
    just want the text, thanks.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [html_text.extract_text(x) for x in X]


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

    Because CountVectorizer and TfidfVectorizer default to using a regex for
    text tokenisation that would exclude grams containing "*", the default filler
    character for this pipeline Vectoriser is "F". Setting this to "*" is a cheap
    way to exclude filler-nodes from Vectorisation, which may improve profiles
    in some cases.

    Also important is considering downstream options; it may make little sense
    to use N-Gram (N>1) windowing over the faux-text returned from the PQ-Grams
    profile builder, as these PQ-Grams already capture neighbour-semantic
    relationships, and additional adjacency emphasis may harm, not help,
    feature context.

    For some reason, this vectoriser alone will not work well with parallel
    execution within SKLearn, returning a somewhat cryptic error that seems to
    lie within LXML or etree. If the pipeline that is being parallel-fit includes
    LxmlParseTransformer immediately upstream of PQGramVectoriser, however, then
    things work again. Presumably tihs lets each executor have its own LXML
    tree. If doing so, implying that the pipeline is receiving immutable strings,
    remember to disable "clone_trees" for efficiency.
    """

    def __init__(self, p=2, q=3, filler='F', decomment=True, clone_trees=True):
        self.p = p
        self.q = q
        self.filler = filler
        self.decomment = decomment
        self.clone_trees = clone_trees

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        rawP = get_profiles(*X,
                            p=self.p,
                            q=self.q,
                            filler=self.filler,
                            decomment=self.decomment,
                            clone_tree=self.clone_trees)
        return [' '.join(''.join(gram) for gram in profile) for profile in rawP]
