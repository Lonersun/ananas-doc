# -*- coding:utf-8 -*-
import sys, yaml, datetime

from conf import log_doc_config

reload(sys)
sys.setdefaultencoding("utf-8")


class DocLog(object):

    note_cache_file = "template/_version/note"

    version_cache_file = "template/_version/version"

    note_list = []

    def __init__(self):
        pass

    def load_note(self):
        """

        :return:
        """
        note = ""
        f = file(self.note_cache_file, "r")
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] == "#":
                continue
            note += "* " + str(line)
            self.note_list.append(line)
        f.close()
        self.note = note

    def load_version(self):
        """

        :return:
        """
        f = file(self.version_cache_file, "r")
        while True:
            line = f.readline()
            line.strip()
            if not line:
                break
            if line[0] == "#":
                continue
            self.version = line.strip()
            break
        f.close()

    def set_md(self):
        """

        :return:
        """
        self.load_version()
        self.load_note()
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.datetime.now().strftime('%H:%M')
        yml_file = open("template/_version/version.yml", 'r')
        log = yaml.load(yml_file).get('version', None)
        docs = {
            'date': now_date,
            'time': now_time,
            'version': self.version,
            'author': log_doc_config.get('author', ''),
            'note': self.note_list
        }
        if log:
            new_v = log[0]
            if new_v['version'] == self.version:
                log[0] = docs
            else:
                log.insert(0, docs)
        else:
            log = [docs]
        _doc = {
            'version': log
        }
        yml_file.close()
        yml_file = open("template/_version/version.yml", 'w')
        yaml.dump(_doc, yml_file)
        yml_file.close()
        log_doc = "\n## "
        log_doc += log_doc_config.get('log_title') + "\n"
        for _log in log:
            log_doc += "### " + _log['date'] + "\n\n"
            log_doc += "**版本:** " + _log['version'] + "\n\n"
            log_doc += "**作者:** " + _log['author'] + "\n\n"
            log_doc += "**更新于:** " + _log['date'] + " " + _log['time'] + "\n\n"
            log_doc += "**更新内容:** \n\n"
            for v in _log['note']:
                log_doc += "* " + v
            log_doc += "\n"

        f = file("ananas/docs/log_doc.md", "w+")
        f.write(log_doc)
        f.close()

    def initialize(self):
        """

        :return:
        """
        note_doc = "# 请输入本次升级内容，一行为一条，请不要输入空行\n#\n"
        f = file(self.note_cache_file, "w+")
        f.write(note_doc)
        f.close()
        self.load_version()
        version_doc = "# 请输入本次升级文档版本号\n\n"
        version_doc += "# 当前最新版本为" + str(self.version)
        f = file(self.version_cache_file, "w+")
        f.write(version_doc)
        f.close()

if __name__ == '__main__':
    if not log_doc_config.get('if_set_log'):
        pass
    else:
        cmd = sys.argv[1]
        server = DocLog()
        if cmd == "set_markdown":
            server.set_md()
            print "doc log set_markdown success!"
        elif cmd == "initialize":
            server.initialize()
            print "doc log initialize success!"


