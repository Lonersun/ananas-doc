# -*- coding: utf-8 -*-
#
# ananas documentation config
#
import sphinx_rtd_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'm2r'
]
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True
latex_elements = {}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# set document title author

project = u'doc'
copyright = u'2017, doc'
author = u'doc'

# API version
version = u''
release = u''

# language
language = 'zh_CN'

# theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme . get_html_theme_path()]

# static path
html_static_path = ['template/_static']

# index
index_doc_config = {
    'title': "Ananas",
    'content': "Ananas",
    "nav": []
}

# api config
api_doc_config = {
    "if_set_api": True,            # Using YML to generate .md
    "api_dir": "/Users/Song/Desktop/www/untitled/api_schema",             # abs path of your project.
    "leve": 2,                      #
    "title": "fddf",                    # give the title by level start path.
    "schema_template": "lcylln"    # with yml template。 lcylln, default
}

# error code config
errors_doc_config = {
    "if_set_errors": False,
    "module_dir": "/path",
    "module_name": "errors",
    "error_title": "",
}

# doc log
log_doc_config = {
    "if_set_log": False,
    "author": "Ananas",
    "log_title": "",
}
        