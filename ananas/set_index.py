# -*- coding:utf-8 -*-
import sys, yaml, datetime

from conf import log_doc_config, errors_doc_config, index_doc_config

reload(sys)
sys.setdefaultencoding("utf-8")


class DocIndex(object):

    def __init__(self):
        pass

    def set_index(self):
        """

        :return:
        """
        title = index_doc_config.get('title')
        navs = index_doc_config.get('nav')
        content = ".. Aoao documentation\n\n"
        content += title + "\n" + len(title) * 2 * "=" + "\n\n"
        content += index_doc_config.get('content') + "\n\n"
        content += "目录: \n\n"
        content += ".. toctree::\n   :maxdepth: 2\n\n"
        for nav in navs:
            content += "   docs/" + nav + ".md\n"
        content += "\n\n"
        f = file('ananas/index.rst', "w+")
        f.write(content)
        f.close()
        print "index set success!"

if __name__ == '__main__':
    server = DocIndex()
    server.set_index()

