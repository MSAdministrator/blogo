"""Sphinx configuration."""
project = "{{title}}"
author = "{{author}}"
copyright = "2022, {{author}}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "{{theme}}"
