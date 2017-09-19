# -*- coding: utf-8 -*-
class Config(object):

    config_dict = dict(
        extensions = [
            'sphinx.ext.autodoc',
            'sphinx.ext.doctest',
            'sphinx.ext.intersphinx',
            'sphinx.ext.todo',
            'sphinx.ext.coverage',
            'm2r'
        ],
        templates_path = ['_templates'],
        source_suffix = ['.rst', '.md'],
        master_doc = 'index',
        exclude_patterns = [],
        pygments_style = 'sphinx',
        todo_include_todos = True,
        latex_elements = {},
        html_sidebars = {
            '**': [
                'about.html',
                'navigation.html',
                'relations.html',
                'searchbox.html',
                'donate.html',
            ]
        },
        project = u'Ananas',
        copyright = u'2017, Ananas',
        author = u'Ananas',
        version = u'',
        release = u'',
        language = 'zh_CN',
        html_theme = 'sphinx_rtd_theme',
        html_static_path = ['template/_static'],
        index_doc_config = {
            'title': "Ananas",
            'content': "Ananas",
            "nav": []
        },
        errors_doc_config = {
            "if_set_errors": False,
            "module_dir": "/path",
            "module_name": "errors",
            "error_title": "",
        },
        log_doc_config = {
            "if_set_log": False,
            "author": "Ananas",
            "log_title": "",
        }
    )

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')

    def mk_conf(self):
        """

        :return:
        """
        conf_str = ""
        conf_str += """
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
"""
        conf_str += "\n"
        conf_str += "project = u'" + self.config_dict['project'] + "'"
        conf_str += "\n"
        conf_str += "copyright = u'" + self.config_dict['copyright'] + "'"
        conf_str += "\n"
        conf_str += "author = u'" + self.config_dict['author'] + "'"
        conf_str += "\n"
        conf_str += """
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
        """
        f = file(self.path + "/conf.py", "w+")
        f.write(conf_str)
        f.close()

