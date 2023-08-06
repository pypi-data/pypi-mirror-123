import os
import pathlib
import sys

# -- Project information -----------------------------------------------------
project = "installer"

copyright = "2020, Pradyun Gedam"
author = "Pradyun Gedam"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "myst_parser",
]

# -- Options for Autodoc -----------------------------------------------------

autodoc_member_order = "bysource"

# Automatically extract typehints when not specified and add them to
# descriptions of the relevant function/methods.
autodoc_typehints = "description"

if "READTHEDOCS" in os.environ:
    src_folder = pathlib.Path(__file__).resolve().parent.parent / "src"
    sys.path.append(str(src_folder))

    print("Detected running on ReadTheDocs")
    print(f"Added {src_folder} to sys.path")
    __import__("installer")

# -- Options for intersphinx ----------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pypug": ("https://packaging.python.org", None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = project

#
# -- Options for Markdown files ----------------------------------------------
#
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3
