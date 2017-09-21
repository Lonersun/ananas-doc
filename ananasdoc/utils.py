# -*- coding: utf-8 -*-
import os
import io
import json
from ruamel.yaml import round_trip_dump, round_trip_load, load, dump_all
from bson.json_util import (default as bson_object_default,
                            object_hook as bson_object_hook)

def dump_yaml_file(data, path, round_tripping=False):
    with io.open(path, 'w', encoding='utf-8') as writer:
        if round_tripping:
            round_trip_dump(data, writer, allow_unicode=True, )
        else:
            dump_all([data], writer, allow_unicode=True)


def load_yaml_file(path, round_tripping=False):
    data = None
    with io.open(path, 'r', encoding='utf-8') as reader:
        if round_tripping:
            data = round_trip_load(reader)
        else:
            data = load(reader)
    return data

def mkdir(path):
    """

    :param path:
    :return:
    """
    path = path.strip()
    path = path.rstrip("\\")

    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
    else:
        pass

def json_dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=bson_object_default, indent=4,
                      encoding='utf-8')