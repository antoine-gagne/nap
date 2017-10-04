# README.MD
=============
Note a problem is a note-taking app baby!

## Installation
To install as a normal package, cd into setup directory and
    `python setup.py install`
    OR
    `python setup.py build` then `pip install .`


##  Example uses:
New/Edit note:
    `nap -n note_name`

New note with keywords:
    `nap -n note_name -k keyword1 keyword2`

List available notes
    `nap -l`

Delete a note
    `nap -d note_name`


## For development
To install the package so it points to the code rather than a static build:
    `pip install -e .`

To build the package for distribution
    `python setup.py bdist_wheel`

To run the tests
    `tox`
