# PyQGrams
by Cathal Garvey, Copyright 2017, released under the GNU LGPLv3 or later.

## About
PQGrams can be used as a better-scaling approximation of tree-edit distance,
making them potentially very valuable when evaluating the similarity of
various websites or HTML fragments.

Even so, calculating these involves a lot of recursive tree-building,
which Python isn't very fast at. So, this is my attempt to create a Python
implementation with a [Rust back-end][rpqg], offering nice interfaces for common
queries.

This project includes Python bindings and wrapper functions to work with LXML-like
trees, and can be used to find best-matching trees between or within sets, or
to build a PQ-Gram profile from LXML trees.

It also includes an experimental Transformer class for [Scikit-Learn][sklearn],
designed to test the theory that PQ-Gram profiles could be treated similarly to
N-Grams for vectorisation and classification of page structure. The Transformer
is expected to be used upstream of a `CountVectorizer` or `TfidfVectorizer` in
a pipeline that accepts LXML trees. Probably, `CountVectorizer` makes more sense,
most of the time.

## Installation

You will need a Rust toolchain for your platform; I haven't yet evaluated
whether this works on Rust-stable, as I use Rust-nightly.

You will also need to install [setuptools_rust][sutr], prior to calling
`python3 setup.py install --user` to build and install the library. Because
`rustup` and other common Rust installers do *not* install system-wide, the
`--user` flag *is required*.

*Update*: If you are using 64-bit Linux and Python 3.5, there is a binary wheel in the
repository for version 0.3:

`pip install 'https://github.com/cathalgarvey/pyqgrams/raw/master/dist/pyqgrams-0.0.3-cp35-cp35m-linux_x86_64.whl'`

If anyone knows how to get x86_64 binary wheels uploaded to PyPI I'm happy to
package, but I get errors due to the x86_64 string being considered "invalid"
by PyPI. :shrug:

## WIP
* This isn't a fixed interface and will evolve quickly.
* I've done some manual testing but there is no actual test-suite, so things
  may break.

## TODO / Desiderata

* Rational wrappers for JSON trees
* "Find Similar Subtree" function
* Ability to re-use tree profiles

[rpqg]: https://github.com/cathalgarvey/pqgrams
[sutr]: https://github.com/fafhrd91/setuptools-rust
