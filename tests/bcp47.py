
from collections import OrderedDict
from unittest.mock import PropertyMock, patch

from bcp47 import BCP47, BCP47Code, BCP47Parser


class DummyParser(object):
    parsed = 23


class DummyCode(object):

    def __init__(self, bcp47, *args, **kwargs):
        self.bcp47 = bcp47
        self.args = args
        self.kwargs = kwargs


def test_bcp47_creates_parser():
    bcp = BCP47()
    assert bcp._parser is None
    assert bcp.parser_class is BCP47Parser
    # mangle the parser class
    bcp.parser_class = DummyParser
    assert bcp.parsed == 23
    parser = bcp._parser
    assert isinstance(parser, DummyParser)
    # dont parse again
    assert bcp.parsed == 23
    assert bcp._parser is parser


def test_bcp47_constructor():
    bcp = BCP47()
    assert bcp.code_class is BCP47Code
    bcp.code_class = DummyCode
    code = bcp()
    assert code.bcp47 is bcp
    # test args, kwargs passthrough
    assert code.args == ()
    assert code.kwargs == {}
    code = bcp("foo", "bar", "baz")
    assert code.args == ('foo', 'bar', 'baz')
    assert code.kwargs == {}
    code = bcp(foo="foo0", bar="bar0", baz="baz0")
    assert (
        code.kwargs
        == {'foo': 'foo0', 'bar': 'bar0', 'baz': 'baz0'})
    code = bcp("foo", "bar", "baz", foo="foo0", bar="bar0", baz="baz0")
    assert code.args == ('foo', 'bar', 'baz')
    assert (
        code.kwargs
        == {'foo': 'foo0', 'bar': 'bar0', 'baz': 'baz0'})


def test_bcp47_languages():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            language=[
                dict(Subtag="foo", other="foo0"),
                dict(Subtag="bar", other="bar0"),
                dict(Subtag="baz", other="baz0")])
        bcp47 = BCP47()
        languages = bcp47["languages"]
        assert isinstance(languages, OrderedDict)
        assert list(languages.keys()) == ["foo", "bar", "baz"]
        assert list(languages.values()) == m.return_value["language"]


def test_bcp47_extlangs():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            extlang=[
                dict(Subtag="foo", other="foo0"),
                dict(Subtag="bar", other="bar0"),
                dict(Subtag="baz", other="baz0")])
        bcp47 = BCP47()
        extlangs = bcp47["extlangs"]
        assert isinstance(extlangs, OrderedDict)
        assert list(extlangs.keys()) == ["foo", "bar", "baz"]
        assert list(extlangs.values()) == m.return_value["extlang"]


def test_bcp47_scripts():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            script=[
                dict(Subtag="foo", other="foo0"),
                dict(Subtag="bar", other="bar0"),
                dict(Subtag="baz", other="baz0")])
        bcp47 = BCP47()
        scripts = bcp47["scripts"]
        assert isinstance(scripts, OrderedDict)
        assert list(scripts.keys()) == ["foo", "bar", "baz"]
        assert list(scripts.values()) == m.return_value["script"]


def test_bcp47_regions():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            region=[
                dict(Subtag="foo", other="foo0"),
                dict(Subtag="bar", other="bar0"),
                dict(Subtag="baz", other="baz0")])
        bcp47 = BCP47()
        regions = bcp47["regions"]
        assert isinstance(regions, OrderedDict)
        assert list(regions.keys()) == ["foo", "bar", "baz"]
        assert list(regions.values()) == m.return_value["region"]


def test_bcp47_variants():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            variant=[
                dict(Subtag="foo", other="foo0"),
                dict(Subtag="bar", other="bar0"),
                dict(Subtag="baz", other="baz0")])
        bcp47 = BCP47()
        variants = bcp47["variants"]
        assert isinstance(variants, OrderedDict)
        assert list(variants.keys()) == ["foo", "bar", "baz"]
        assert list(variants.values()) == m.return_value["variant"]


def test_bcp47_grandfathereds():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            grandfathered=[
                dict(Tag="foo", other="foo0"),
                dict(Tag="bar", other="bar0"),
                dict(Tag="baz", other="baz0")])
        bcp47 = BCP47()
        grandfathereds = bcp47["grandfathereds"]
        assert isinstance(grandfathereds, OrderedDict)
        assert list(grandfathereds.keys()) == ["foo", "bar", "baz"]
        assert list(grandfathereds.values()) == m.return_value["grandfathered"]


def test_bcp47_redundants():

    with patch('bcp47.BCP47.parsed', new_callable=PropertyMock) as m:
        m.return_value = dict(
            redundant=[
                dict(Tag="foo", other="foo0"),
                dict(Tag="bar", other="bar0"),
                dict(Tag="baz", other="baz0")])
        bcp47 = BCP47()
        redundants = bcp47["redundants"]
        assert isinstance(redundants, OrderedDict)
        assert list(redundants.keys()) == ["foo", "bar", "baz"]
        assert list(redundants.values()) == m.return_value["redundant"]
