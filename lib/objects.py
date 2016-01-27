# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Dictionary(dict):
    """Custom dict"""
    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delsttr__ = dict.__delitem__
