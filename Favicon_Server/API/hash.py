# -*- coding: utf-8 -*-
# @Time  : 2021-02-08 23:34
from hashlib import sha1


def get_sha1(content):
    hash_ = sha1()
    hash_.update(content.encode('utf-8'))
    return hash_.hexdigest()
