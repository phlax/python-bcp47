# -*- coding: utf-8 -*-

import os


class BCP47Parser(object):
    parsed = None
    bcp_filename = "iana-bcp47.txt"

    def __init__(self):
        self.bcp = self.parse_bcp()

    @property
    def src_file(self):
        return os.path.join(
            os.path.dirname(__file__),
            self.bcp_filename)

    def open(self):
        with open(self.src_file) as f:
            for line in f.read().split("\n"):
                yield line

    def parse_bcp(self):
        item = None
        items = {}
        key = None
        for line in self.open():
            # python needs switch!
            if line.startswith("%%"):
                item = {}
                continue
            if line is None or item is None:
                continue
            parts = line.split(": ", 1)
            if len(parts) == 1:
                # append to previous key
                if isinstance(item[key], list):
                    item[key][-1] += parts[0]
                else:
                    item[key] += parts[0]
                continue
            key = parts[0]
            value = parts[1]
            if key == "Type":
                # create a key for this type if it
                # doesnt exist
                items[value] = items.get(value, [])
                # add this item to the items/key
                items[value].append(item)
                continue
            if key in ["Description", "Prefix"]:
                # multi value
                item[key] = item.get(key, [])
                item[key].append(value)
                continue
            item[key] = value
        self.parsed = items
