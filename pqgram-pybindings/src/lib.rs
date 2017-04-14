/// This module expects that certain objects passed to it will fulfil
/// an API that facilitates tree building; this is enforced in the Python
/// code of the module, so don't bypass that and things should be just fine. :)

#[macro_use] extern crate cpython;
extern crate pqgrams;
extern crate itertools;
use itertools::Itertools;

use pqgrams::{Tree, pqgram_distance, pqgram_profile, PQGram};
use cpython::{Python, PyObject, PyResult, ObjectProtocol};

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

fn profile_trees(py: Python, p: usize, q: usize, pytrees: &PyObject) -> PyResult<Vec<Vec<Vec<i64>>>> {
    Ok(_profile_trees(py, p, q, pytrees)?.iter().map(
        |v| v.iter().map(|p| p.concat(0)).collect()
    ).collect())
}

/// Given an iterator over trees and a callback for pairwise scores, this sends
/// the scores for each tree pairing back via callback.
fn compare_matrix(py: Python, p: usize, q: usize, pytrees: &PyObject) -> PyResult<Vec<(usize, usize, f64)>> {
    let profiles = _profile_trees(py, p, q, pytrees)?;
    let matrix : Vec<(usize, usize, f64)> = profiles.iter()
          .enumerate()
          .tuple_combinations()  // Itertools!
          .map(|((n1, profile1), (n2, profile2))|
                    (n1, n2, pqgram_distance::<i64, Tree<i64>>(profile1, profile2, None)))
          .collect();
    Ok(matrix)
}

fn compare_one_to_many(py: Python, p: usize, q: usize, onepytree: &PyObject, otherpytrees: &PyObject) -> PyResult<Vec<(usize, f64)>> {
    let onetree = tree_build(None, py, onepytree)?;
    let oneprofile = pqgram_profile(onetree, p, q, false);
    let othertrees = _profile_trees(py, p, q, otherpytrees)?;
    let scores : Vec<(usize, f64)> = vec![oneprofile].iter()
        .cartesian_product(othertrees.iter().enumerate())
        .map(|(onep, (n, otherp))| (n, pqgram_distance::<i64, Tree<i64>>(onep, otherp, None)))
        .collect();
    Ok(scores)
}

py_module_initializer!(pqgrams, initpqgrams, PyInit_pqgrams, |py, m| {
    m.add(py, "__doc__", "A CPython module exposing the Rust PQGrams library. You should probably use the Python module that wraps this.")?;
    m.add(py, "profile_trees", py_fn!(py, profile_trees(p: usize, q: usize, pytrees: &PyObject)))?;
    m.add(py, "compare_one_to_many", py_fn!(py, compare_one_to_many(p: usize, q: usize, onepytree: &PyObject, otherpytrees: &PyObject)))?;
    m.add(py, "compare_matrix", py_fn!(py, compare_matrix(p: usize, q: usize, pytrees: &PyObject)))?;
    Ok(())
});
