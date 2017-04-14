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

## WIP
The Rust code portion probably works, but I haven't tested the Python
interface functions yet, so consider this potentially explosive. :)
