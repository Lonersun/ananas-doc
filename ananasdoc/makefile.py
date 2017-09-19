# -*- coding: utf-8 -*-


class MakeFile(object):

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')

    def set_make_file(self):
        """

        :param make_file_path:
        :return:
        """
        content = """# Minimal makefile for Ananas documentation
#
current_root=`pwd`

doc:
	@python -mananasdoc.template $(current_root)

        """
        f = file(self.path + "/Makefile", "w+")
        f.write(content)
        f.close()

