# !usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ConfigParser

from lib.objects import Dictionary


class Config:
    """Config file parser"""

    def __init__(self, cfg=None):
        config = ConfigParser.ConfigParser()

        if cfg:
            config.read(cfg)
        else:
            config.read(os.path.join("{BASE_PATH}",
                                     "conf", "database.conf"))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_calue in config.items(section):
                value = config.get(section, name)
                setattr(getattr(self, section), name, value)

    def get(self, section):
        """Get option"""
        try:
            return getattr(self, section)
        except AttributeError as e:
            raise ("Option {} is not found in config,"
                   "error: {}").format(section, e)
