# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'DearPyGui-Obj'
copyright = '2021, mwerezak'
author = 'mwerezak'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.autosummary',
	'sphinx.ext.napoleon',
	# 'sphinx.ext.autosectionlabel',
	# 'sphinx.ext.todo',
	'sphinx.ext.viewcode',
	'sphinx.ext.extlinks',
	'sphinx.ext.intersphinx',
	'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# html_theme = 'python_docs_theme'
# html_theme = 'alabaster'
# html_theme = 'nature'
# html_theme = 'classic'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension Settings ------------------------------------------------------

autosummary_generate = False


extlinks = {
	'dearpygui' : ('https://github.com/hoffstadt/DearPyGui/wiki/%s', 'dearpygui'),
}

intersphinx_mapping = {
	'python' : ('https://docs.python.org/3.8', None),
	'curio'  : ('https://curio.readthedocs.io/en/latest', None),
}

autodoc_default_options = {
	'member-order' : 'bysource',
	'show-inheritance' : True,
}

autodoc_type_aliases = {
}

# autosectionlabel_prefix_document = True
# autosectionlabel_maxdepth = None

autoclass_content = 'both'
napoleon_numpy_docstring = False


# def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
# 	if what in ('class', 'exception'):
# 		signature = None
# 	return (signature, return_annotation)

# def setup(app):
# 	app.connect('autodoc-process-signature', autodoc_process_signature)
