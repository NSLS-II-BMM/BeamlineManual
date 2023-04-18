# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
CURDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join('sphinx', 'ext')))
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'BMM Beamline Manual'
copyright = ': none, this document is available as a public service'
author = 'Bruce Ravel'

# The full version, including alpha/beta/rc tags
release = '0.1'

numfig = True

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_math_dollar', 'sphinx.ext.mathjax',
              'sphinx.ext.todo',
]
extensions.extend([#'fix_equation_ref',
                   'subfig', 'numsec', 'figtable',
                   'singlehtml_toc', 'singletext', 'demeterdocs',
])

mathjax3_config = {
    'tex2jax': {
        'inlineMath': [ ["\\(","\\)"] ],
        'displayMath': [["\\[","\\]"] ],
    },
}
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

todo_include_todos = True
rst_prolog = open(os.path.join(CURDIR, 'prolog.rst'),'r').read() 
rst_epilog = open(os.path.join(CURDIR, 'epilog.rst'),'r').read() 

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'prolog.rst', 'epilog.rst', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_url": "https://github.com/NSLS-II-BMM/BeamlineManual",
    "use_edit_page_button": False,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "extra_navbar": '<p><a href=https://wiki-nsls2.bnl.gov/beamline6BM/index.php?Main_Page><img src="./_static/floor_mat.png" style="height: 3cm;" alt="BMM floor tab"><br>Beamline for Materials<br>Measurement</a></p>',
}

#html_sidebars = {
#    "**": ["sidebar-logo.html", "search-field.html", "sbt-sidebar-nav.html", "sbt-sidebar-footer.html"]
#}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
