# -*- coding: utf-8 -*-

from collections import OrderedDict

from .parser import BCP47Parser
from .code import BCP47Code


class BCP47(object):
    _parser = None
    parser_class = BCP47Parser
    code_class = BCP47Code

    def __init__(self):
        self.mapping = dict(
            languages=("language", ),
            extlangs=("extlang", ),
            scripts=("script", ),
            regions=("region", ),
            variants=("variant", ),
            grandfathereds=("grandfathered", "Tag"),
            redundants=("redundant", "Tag"))

    def __getitem__(self, k):
        return self._parsed_tags(*self.mapping[k])

    def __call__(self, *args, **kwargs):
        return self.code_class(self, *args, **kwargs)

    @property
    def parsed(self):
        if self._parser is None:
            self._parser = self.parser_class()
        return self._parser.parsed

    def _parsed_tags(self, tag, key="Subtag"):
        return OrderedDict(
            [(x[key], x)
             for x
             in self.parsed[tag]])


bcp47 = BCP47()
