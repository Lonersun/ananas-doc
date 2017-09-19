# -*- coding: utf-8 -*-
import os


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

