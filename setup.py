from setuptools import setup, find_packages
from setuptools_rust import RustExtension
import textwrap

setup(name='pyqgrams',
      version='0.0.5',
      description="Bindings to the Rust PQGrams crate for Python.",
      long_description=textwrap.dedent("""\
        # Building Note
        PyQGrams is a module based on a Rust crate, PQGrams.
        Therefore, it requires a Rust toolchain to build.
        It also uses setuptools_rust to manage the Python build/install process,
        but this must be installed before calling `setup.py`.

        # Usage
        PyQGrams exposes a similar API to PQGrams; any tree-like object
        that implements a "label" and "child" method on each node can be
        processed.

        Labels must be hashable; their hash value is used to build label-trees
        internally, so the hashes should be well-distributed but deterministic.
        This is true of most Python value-type built-ins including string and
        int values, but it is not true of dicts and lists, and will usually not
        be true of custom classes that don't implement a sane __hash__ method.
      """).strip(),
      author="Cathal Garvey",
      author_email="cathalgarvey@cathalgarvey.me",
      url='https://github.com/cathalgarvey/pyqgrams',
      license='MIT',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['lxml'],
      rust_extensions=[RustExtension("pyqgrams.pqgrams", "pqgram-pybindings/Cargo.toml")],
      zip_safe=False
)
