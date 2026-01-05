# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))



# -- Project information -----------------------------------------------------

project = 'AudioReach Documentation'
copyright = '2024, AudioReach'
author = 'Patrick Lai'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [ "breathe", 'sphinx_rtd_theme', 'sphinx.ext.autosectionlabel' ]
breathe_projects = {
          "args_osal":"../doxygen/xml",
          "args_gsl":"../doxygen/xml",
          "args_gpr":"../doxygen/xml",
          "arspf_capi":"../doxygen/xml",
          "arspf_posal": "../doxygen/xml"
        }
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme
import os
html_theme = "sphinx_rtd_theme"

#html_logo = "images/icon.png"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

# While generating Sphinx output from XML files, <ndash/> tag is getting
# converted to &amp;#8212; (i.e. & character is represented as &amp;) which
# is converted to &#8212; in html output instead of "—" character.
# Use function to process generated html files and replace &amp;#8212; with
# &#8212; symbol to get ndash character(—) in HTML output.
def process_html(app, exception):
    if exception is None:  # Proceed only if there were no build errors
        output_dir = app.outdir
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = content.replace('&amp;#8212;', '&#8212;')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

def setup(app):
    app.add_css_file("audioreach.css")
    app.connect('build-finished', process_html)

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth=3
