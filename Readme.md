# PyQGrams
by Cathal Garvey, Copyright 2017, released under the GNU LGPLv3 or later.

## About
PQGrams can be used as a better-scaling approximation of tree-edit distance,
making them potentially very valuable when evaluating the similarity of
various websites or HTML fragments.

Even so, calculating these involves a lot of recursive tree-building,
which Python isn't very fast at. So, this is my attempt to create a Python
implementation with a Rust back-end, offering nice interfaces for common
queries.

## Installation

You will need a Rust toolchain for your platform; I haven't yet evaluated
whether this works on Rust-stable, as I use Rust-nightly.

You will also need to install [setuptools_rust][sutr], prior to calling
`python3 setup.py install --user` to build and install the library. Because
`rustup` and other common Rust installers do *not* install system-wide, the
`--user` flag *is required*.

In the future I plan to compile and distribute binary wheels for 64-bit Linux.

## WIP
The Rust code portion probably works, but I haven't tested the Python
interface functions yet, so consider this potentially explosive. :)

This isn't a fixed interface and will evolve quickly.

## TODO / Desiderata

* Rational wrappers for JSON trees
* "Find Similar Subtree" function
* Ability to re-use tree profiles
