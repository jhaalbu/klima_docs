
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AV-Klima'
copyright = '2023'
author = 'Jan Helge Aalbu'

import os
import sys
sys.path.insert(0, os.path.abspath('..\..'))
#sys.path.insert(0, os.path.abspath('..\..\klimadata'))
#sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']

templates_path = ['..\_templates']
exclude_patterns = ['..\_build', 'Thumbs.db', '.DS_Store']

language = 'nb_NO'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['..\_static']

autodoc_mock_imports = ["folium",
    "matplotlib",
    "numba",
    "numdifftools",
    "numpy",
    "pandas",
    "pyextremes",
    "pyproj",
    "requests",
    "scipy",
    "streamlit",
    "streamlit_folium",
    "windrose"
]