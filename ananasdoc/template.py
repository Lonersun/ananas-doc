# -*- coding:utf-8 -*-
import os
import sys
import error
import log
import table

from importlib import import_module


class AnanasTemplate(object):

    def __init__(self, path):
        self.path = path

    def run(self):
        """

        :return:
        """
        sys.path.append(self.path)
        config = import_module("conf")
        errors_doc_config = config.errors_doc_config
        log_doc_config = config.log_doc_config
        index_doc_config = config.index_doc_config

        # make version
        if log_doc_config.get('if_set_log') is True:
            os.system("vim " + path + "/template/_version/.note")
            os.system("vim " + path + "/template/_version/.version")

        # make markdown
        self.make_markdown(errors_doc_config=errors_doc_config,
                           log_doc_config=log_doc_config,
                           index_doc_config=index_doc_config)
        # make html
        os.system("python -msphinx -M html " + self.path + " " + self.path + "/build")

    def make_markdown(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        # load config
        errors_doc_config = kwargs.get('errors_doc_config')
        log_doc_config = kwargs.get('log_doc_config')
        index_doc_config = kwargs.get('index_doc_config')
        # try:
        # make error md
        if errors_doc_config.get('if_set_errors') is True:
            error_server = error.AnanasError(path=self.path, **errors_doc_config)
            error_server.set_md()
            print "Error document was generated successfully！"

        # make log md
        if log_doc_config.get('if_set_log') is True:
            log_server = log.AnanasLog(path=self.path,
                                       log_doc_config=log_doc_config)
            log_server.set_md()
            print "Log document was generated successfully！"

        # make index
        table_server = table.AnanasTable(path=path,
                                         index_doc_config=index_doc_config)
        table_server.set_index()
        print "Index document was generated successfully！"

        # init log
        if log_doc_config.get('if_set_log') is True:
            log_server.initialize()
        # except Exception, e:
        #     print "MakeDocError:[%s]", e
        #     print "Make Doc Failed!!!"
        #     exit()




if __name__ == "__main__":
    path = sys.argv[1]
    AnanasTemplate(path).run()
