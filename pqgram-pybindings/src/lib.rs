/// This module expects that certain objects passed to it will fulfil
/// an API that facilitates tree building; this is enforced in the Python
/// code of the module, so don't bypass that and things should be just fine. :)

#[macro_use]
extern crate cpython;
extern crate pqgrams;
extern crate itertools;
use itertools::Itertools;
use std::collections::HashMap;

use pqgrams::{Tree, pqgram_distance, pqgram_profile, PQGram};
use cpython::{Python, PyObject, PyResult, ObjectProtocol};

// Replaces "Filler" nodes in returned trees, rather than the more ambiguous "0".
// Chosen by fair die roll.
static FILLER_RANDOM_INT : i64 = 6888428148507855167;

// Recursive tree-builder from an LXML-like Python object
fn tree_build(maybe_tree: Option<Tree<i64>>, py: Python, pytree: &PyObject) -> PyResult<Tree<i64>> {
    let mut tree = if let Some(t) = maybe_tree {
        t
    } else {
        let tag = pytree.getattr(py, "tag")?.hash(py)?;
        Tree::new(tag as i64)
    };
    for child in pytree.iter(py)?.into_iter() {
        let subtree = tree_build(None, py, &child?);
        tree = tree.add_node(subtree?);
    };
    Ok(tree)
}

fn _profile_trees(py: Python, p: usize, q: usize, pytrees: &PyObject) -> PyResult<Vec<Vec<PQGram<i64>>>> {
    let mut profiles = vec![];
    for pytree in pytrees.iter(py)?.into_iter() {
        let tree = tree_build(None, py, &pytree?)?;
        profiles.push(pqgram_profile(tree, p, q, false));
    };
    Ok(profiles)
}

/// profile_trees returns the flattened PQGrams for each tree provided.
/// "Filler" nodes from the extended tree will be represented by
/// the FILLER_RANDOM_INT value, rather than zero, to avoid bugs caused
/// by zero-hashing Python items like the empty string or the zero int.
pub fn profile_trees(py: Python, p: usize, q: usize, pytrees: &PyObject) -> PyResult<Vec<Vec<Vec<i64>>>> {
    Ok(_profile_trees(py, p, q, pytrees)?.iter().map(
        |v| v.iter().map(
            |p| p.concat(FILLER_RANDOM_INT)).collect()
        ).collect())
}

/// Given an iterator over trees, this compares all trees in the iterator to all
/// other trees. It is, clearly, very prone to combinatorial explosion; beware!
pub fn compare_matrix(py: Python, p: usize, q: usize, pytrees: &PyObject) -> PyResult<Vec<(usize, usize, f64)>> {
    let profiles = _profile_trees(py, p, q, pytrees)?;
    let matrix : Vec<(usize, usize, f64)> = profiles.iter()
          .enumerate()
          .tuple_combinations()  // Itertools!
          .map(|((n1, profile1), (n2, profile2))|
                    (n1, n2, pqgram_distance::<i64, Tree<i64>>(profile1, profile2, None)))
          .collect();
    Ok(matrix)
}

/// This function takes two iterators of trees, and compares the two sets of profiles.
/// Beware: Combinatorial explosions possible.
pub fn compare_many_to_many(py: Python, p: usize, q: usize, pytrees1: &PyObject, pytrees2: &PyObject) -> PyResult<Vec<(usize, usize, f64)>> {
    let trees1 = _profile_trees(py, p, q, pytrees1)?;
    let trees2 = _profile_trees(py, p, q, pytrees2)?;
    let scores: Vec<(usize, usize, f64)> = trees1.iter().enumerate()
        .cartesian_product(trees2.iter().enumerate())
        .map(|((n1, p1), (n2, p2))| (n1, n2, pqgram_distance::<i64, Tree<i64>>(p1, p2, None)))
        .collect();
    Ok(scores)
}

py_module_initializer!(pqgrams, initpqgrams, PyInit_pqgrams, |py, m| {
    m.add(py, "__doc__", "A CPython module exposing the Rust PQGrams library. You should probably use the Python module that wraps this.")?;
    m.add(py, "profile_trees", py_fn!(py, profile_trees(p: usize, q: usize, pytrees: &PyObject)))?;
    m.add(py, "compare_many_to_many", py_fn!(py, compare_many_to_many(p: usize, q: usize, pytrees1: &PyObject, pytrees2: &PyObject)))?;
    m.add(py, "compare_matrix", py_fn!(py, compare_matrix(p: usize, q: usize, pytrees: &PyObject)))?;
    m.add(py, "FILLER_RANDOM_INT", FILLER_RANDOM_INT)?;
    Ok(())
});
