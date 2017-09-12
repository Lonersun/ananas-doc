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

# 设置文档标题、版权、作者.
project = u'Ananas文档生成工具'
copyright = u'2017, Lonersun'
author = u'Lonersun'

# 版本
version = u''
release = u''

# 语言
language = 'zh_CN'

# 主题
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme . get_html_theme_path()]

# 静态文件目录
html_static_path = ['../template/_static']

# 目录
index_doc_config = {
    # 标题
    'title': "Ananas 使用文档",

    # content
    'content': "基于Sphinx的文档生成工具",

    # 导航<需要加载的MarkDown文件>
    "nav": ['summary_doc', 'install_doc', 'use_doc', 'log_doc']
}


# 错误码文档生成配置
errors_doc_config = {
    # 是否要生成错误码文档
    "if_set_errors": False,

    # 错误码所在模块路径
    "module_dir": "/path",

    # 错误码所在模块名称
    "module_name": "errors",

    # 错误码文档生成标题
    "error_title": "三、错误对照表",
}

# 文档更新日志
log_doc_config = {
    # 是否要生成日志
    "if_set_log": True,

    # 更新作者
    "author": "Lonersun",

    # 日志标题
    "log_title": "四、更新日志",
}


