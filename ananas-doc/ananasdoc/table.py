# -*- coding:utf-8 -*-
import sys, yaml, datetime

reload(sys)
sys.setdefaultencoding("utf-8")


class AnanasTable(object):

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.index_doc_config = kwargs.get('index_doc_config')

    def set_index(self):
        """

        :return:
        """
        title = self.index_doc_config.get('title')
        navs = self.index_doc_config.get('nav')
        content = ".. Ananas documentation\n\n"
        content += title + "\n" + len(title) * 2 * "=" + "\n\n"
        content += self.index_doc_config.get('content') + "\n\n"
        content += "目录: \n\n"
        content += ".. toctree::\n   :maxdepth: 2\n\n"
        for nav in navs:
            content += "   docs/" + nav + ".md\n"
        content += "\n\n"
        f = file(self.path + '/index.rst', "w+")
        f.write(content)
        f.close()


