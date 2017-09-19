# -*- coding:utf-8 -*-
import sys, yaml, datetime

reload(sys)
sys.setdefaultencoding("utf-8")


class AnanasLog(object):

    note_cache_file = "template/_version/.note"

    version_cache_file = "template/_version/.version"

    version_yml = "template/_version/version.yml"

    log_md = "docs/log.md"

    note_list = []

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.log_doc_config = kwargs.get('log_doc_config')
        self.note_cache_file = self.path + "/" + self.note_cache_file
        self.version_cache_file = self.path + "/" + self.version_cache_file
        self.version_yml = self.path + "/" + self.version_yml
        self.log_md = self.path + "/" + self.log_md

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
        yml_file = open(self.version_yml, 'r')
        log = yaml.load(yml_file).get('version', None)
        docs = {
            'date': now_date,
            'time': now_time,
            'version': self.version,
            'author': self.log_doc_config.get('author', ''),
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
        yml_file = open(self.version_yml, 'w')
        yaml.dump(_doc, yml_file)
        yml_file.close()
        log_doc = "\n## "
        log_doc += self.log_doc_config.get('log_title') + "\n"
        for _log in log:
            log_doc += "### " + _log['date'] + "\n\n"
            log_doc += "**版本:** " + _log['version'] + "\n\n"
            log_doc += "**作者:** " + _log['author'] + "\n\n"
            log_doc += "**更新于:** " + _log['date'] + " " + _log['time'] + "\n\n"
            log_doc += "**更新内容:** \n\n"
            for v in _log['note']:
                log_doc += "* " + v
            log_doc += "\n"

        f = file(self.log_md, "w+")
        f.write(log_doc)
        f.close()

    def initialize(self):
        """

        :return:
        """
        note_doc = """
# Please enter a submission message to explain the updated content.
#
# Lines starting with '#' will be ignored, and each line represents a title
        """
        note_doc += "\n"
        f = file(self.note_cache_file, "w+")
        f.write(note_doc)
        f.close()
        self.load_version()
        version_doc = """# Write a message for version:
        """
        version_doc += "\n# The latest version is" + str(self.version)
        version_doc += "\n# Lines starting with '#' will be ignored.\n"
        f = file(self.version_cache_file, "w+")
        f.write(version_doc)
        f.close()
