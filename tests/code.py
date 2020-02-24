
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from bcp47 import BCP47, BCP47Code, BCP47Exception


def test_bcp47_code_construct_args_and_kwargs():
    bcp = BCP47()
    with pytest.raises(BCP47Exception) as e:
        BCP47Code(bcp, "foo", "bar", "baz", foo="foo0")
    assert e.value.args[0].startswith("Mixture of args and kwargs")


def test_bcp47_code_construct_no_args_or_kwargs():
    bcp = BCP47()
    with pytest.raises(BCP47Exception) as e:
        BCP47Code(bcp)
    assert e.value.args[0].startswith("No arguments provided")


def test_bcp47_code_construct_args():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct_from_args') as construct_m:
        BCP47Code(bcp, "foo", "bar")
        assert (
            list(construct_m.call_args)
            == [('foo', 'bar'), {}])


def test_bcp47_code_construct_kwargs():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct_from_kwargs') as construct_m:
        BCP47Code(bcp, foo="foo0", bar="bar0")
        assert (
            list(construct_m.call_args)
            == [(), {'foo': 'foo0', 'bar': 'bar0'}])


def test_bcp47_code_args():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct') as m:
        BCP47Code(bcp, "foo", "bar", "baz")
        assert (
            list(m.call_args)
            == [('foo', 'bar', 'baz'), {}])


def test_bcp47_code_kwargs():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct') as m:
        BCP47Code(bcp, foo="foo0", bar="bar0", baz="baz0")
        assert (
            list(m.call_args)
            == [(), {'foo': 'foo0', 'bar': 'bar0', 'baz': 'baz0'}])


def test_bcp47_code_string():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct') as m:
        lang_code = 'bcp47.BCP47Code.lang_code'
        with patch(lang_code, new_callable=PropertyMock) as m:
            m.return_value = "LANG CODE"
            code = BCP47Code(bcp, "foo", "bar", "baz")
            assert str(code) == "LANG CODE"
            assert (
                repr(code)
                == ("<%s.%s '%s' />"
                    % (code.__module__,
                       code.__class__.__name__,
                       code.lang_code)))


def test_bcp47_code_construct_from_kwargs():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_part') as m_add:
            m_add.side_effect = lambda parts, t, n: (
                parts.append(n) if n else None)
            code = BCP47Code(bcp)
            code.construct_from_kwargs(language="en", region="GB")
            assert (
                list(list(c[0][1:]) for c in m_add.call_args_list)
                == [['language', 'en'],
                    ['extlang', None],
                    ['script', None],
                    ['region', 'GB'],
                    ['variant', None]])
            assert (
                code.kwargs
                == {'language': 'en', 'region': 'GB'})
            assert code._lang_code == "en-GB"


def test_bcp47_code_props():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct'):
        code = BCP47Code(bcp)
        code._lang_code = "LANG CODE"
        code.kwargs = {
            "grandfathered": "GRANDFATHERED",
            "language": "LANG",
            "extlang": "EXTLANG",
            "script": "SCRIPT",
            "region": "REGION",
            "variant": "VARIANT"}
        assert code.language == "LANG"
        assert code.extlang == "EXTLANG"
        assert code.script == "SCRIPT"
        assert code.region == "REGION"
        assert code.variant == "VARIANT"
        assert code.lang_code == "LANG CODE"
        assert code.grandfathered == "GRANDFATHERED"


def test_bcp47_add_part():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        code = BCP47Code(bcp)
        m_parts = MagicMock()
        result = code._add_part(m_parts, "PART TYPE", None)
        assert result is None
        assert not bcp.__getitem__.called
        assert not m_parts.append.called

        bcp.__getitem__.return_value.__contains__.return_value = True
        result = code._add_part(m_parts, "PART TYPE", "NAME")
        assert (
            list(bcp.__getitem__.call_args)
            == [('PART TYPEs',), {}])
        assert(
            list(bcp.__getitem__.return_value.__contains__)
            == [])
        assert (
            list(m_parts.append.call_args)
            == [('NAME',), {}])

        m_parts.reset_mock()
        bcp.reset_mock()

        bcp.__getitem__.return_value.__contains__.return_value = False
        with pytest.raises(BCP47Exception) as e:
            code._add_part(m_parts, "PART TYPE", "NAME")
        assert (
            e.value.args[0]
            == "Part type 'NAME' not recognized")
        assert (
            list(bcp.__getitem__.call_args)
            == [('PART TYPEs',), {}])
        assert(
            list(bcp.__getitem__.return_value.__contains__)
            == [])
        assert not m_parts.append.called


def test_bcp47_add_prefix_language():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        bcp.__getitem__.return_value.get.return_value = "LANG"
        code = BCP47Code(bcp)
        parts = MagicMock()
        code._add_prefix(parts, ["lang", "region"])
        assert len(bcp.__getitem__.call_args_list) == 1
        assert (
            list(bcp.__getitem__.call_args)
            == [('languages',), {}])
        assert (
            list(bcp.__getitem__.return_value.get.call_args)
            == [('lang',), {}])
        assert (
            list(parts.append.call_args)
            == [('lang',), {}])
        assert code.kwargs == {'language': 'lang'}


def test_bcp47_add_prefix_grandfathered():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        def lookup(k):
            if k == "languages":
                return {}
            return dict(gf="code")

        bcp.__getitem__.side_effect = lookup
        code = BCP47Code(bcp)
        parts = MagicMock()
        code._add_prefix(parts, ["gf"])
        assert len(bcp.__getitem__.call_args_list) == 2
        assert (
            list(bcp.__getitem__.call_args)
            == [('grandfathereds',), {}])
        assert (
            list(parts.append.call_args)
            == [('gf',), {}])
        assert code.kwargs == {'grandfathered': 'gf'}


def test_bcp47_add_prefix_nomatch():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        bcp.__getitem__.return_value = {}
        code = BCP47Code(bcp)
        parts = MagicMock()

        with pytest.raises(BCP47Exception) as e:
            code._add_prefix(parts, ["NOMATCH"])
        assert (
            e.value.args[0]
            == "Language 'NOMATCH' not recognized")
        assert (
            list(list(c) for c in bcp.__getitem__.call_args_list)
            == [[('languages',), {}], [('grandfathereds',), {}]])
        assert not parts.append.called
        assert code.kwargs == {}


def test_bcp47_add_prefix_grandfathered_args():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        def lookup(k):
            if k == "languages":
                return {}
            return dict(gf="code")

        bcp.__getitem__.side_effect = lookup
        code = BCP47Code(bcp)
        parts = MagicMock()
        with pytest.raises(BCP47Exception) as e:
            code._add_prefix(parts, ["gf", "foo", "bar"])
        assert (
            e.value.args[0]
            == ("Grandfathered tags cannot have further extensions "
                "- found '['foo', 'bar']'"))
        assert (
            list(list(c) for c in bcp.__getitem__.call_args_list)
            == [[('languages',), {}], [('grandfathereds',), {}]])
        assert not parts.append.called
        assert code.kwargs == {}


def test_bcp47_maybe_add_part():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):

        def lookup(k):
            if k == "foos":
                return {}
            return dict(PART="info")

        bcp.__getitem__.side_effect = lookup
        code = BCP47Code(bcp)
        parts = MagicMock()
        tag_types = ["foo", "bar", "baz"]
        result = code._maybe_add_part(parts, tag_types, "PART")
        assert result == ('info', ['baz'])
        assert (
            list(list(c) for c in bcp.__getitem__.call_args_list)
            == [[('foos',), {}], [('bars',), {}]])
        assert code.kwargs == {'bar': 'PART'}
        assert (
            list(list(c) for c in parts.append.call_args_list)
            == [[('PART',), {}]])


def test_bcp47_maybe_dont_add_part():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        bcp.__getitem__.return_value = {}
        code = BCP47Code(bcp)
        parts = MagicMock()
        tag_types = ["foo", "bar", "baz"]
        result = code._maybe_add_part(parts, tag_types, "PART")
        assert result == (None, [])
        assert (
            list(list(c) for c in bcp.__getitem__.call_args_list)
            == [[('foos',), {}], [('bars',), {}], [('bazs',), {}]])
        assert code.kwargs == {}
        assert not parts.append.called


def test_bcp47_code_construct_from_kwargs_gf_and_lang():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_part') as m_add:
            m_add.side_effect = lambda parts, t, n: (
                parts.append(n) if n else None)
            code = BCP47Code(bcp)
            with pytest.raises(BCP47Exception) as e:
                code.construct_from_kwargs(
                    language="en", grandfathered="some-gf-tag")
            assert e.value.args[0].startswith("You can only specify either")
            assert not m_add.called
            assert (
                code.kwargs
                == {})
            assert code._lang_code is None


def test_bcp47_code_construct_from_kwargs_no_gf_or_lang():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_part') as m_add:
            m_add.side_effect = lambda parts, t, n: (
                parts.append(n) if n else None)
            code = BCP47Code(bcp)
            with pytest.raises(BCP47Exception) as e:
                code.construct_from_kwargs(region="GB", variant="foo")
            assert e.value.args[0].startswith("Please specify")
            assert not m_add.called
            assert (
                code.kwargs
                == {})
            assert code._lang_code is None


def test_bcp47_code_construct_from_kwargs_grandfathered():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_part') as m_add:
            m_add.side_effect = lambda parts, t, n: (
                parts.append(n) if n else None)
            code = BCP47Code(bcp)
            code.construct_from_kwargs(grandfathered="some-gf")
            assert(
                list(list(c) for c in m_add.call_args_list)
                == [[(['some-gf'], 'grandfathered', 'some-gf'), {}]])
            assert (
                code.kwargs
                == {'grandfathered': 'some-gf'})
            assert code._lang_code == "some-gf"


def test_bcp47_code_construct_from_args_language():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_prefix') as m_prefix:
            with patch('bcp47.BCP47Code._maybe_add_part') as m_add:
                m_prefix.side_effect = (
                    lambda parts, args: parts.append(args[0]))
                code = BCP47Code(bcp)
                code.construct_from_args("foo")
                assert code._lang_code == "foo"
                assert not m_add.called


def test_bcp47_code_construct_from_args_language_region():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_prefix') as m_prefix:
            with patch('bcp47.BCP47Code._maybe_add_part') as m_add:
                m_prefix.side_effect = (
                    lambda parts, args: parts.append(args[0]))

                def _maybe_add(parts, tag_types, part):
                    parts.append(part)
                    code.kwargs["region"] = part
                    return "region", ["variant"]

                m_add.side_effect = _maybe_add
                code = BCP47Code(bcp)
                code.construct_from_args("LANG", "REGION")
                assert code._lang_code == "LANG-REGION"


def test_bcp47_code_construct_from_args_language_script_variant():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_prefix') as m_prefix:
            with patch('bcp47.BCP47Code._maybe_add_part') as m_add:
                m_prefix.side_effect = (
                    lambda parts, args: parts.append(args[0]))

                def _maybe_add(parts, tag_types, part):
                    parts.append(part)
                    return part, tag_types[tag_types.index(part.lower()) + 1:]

                m_add.side_effect = _maybe_add
                code = BCP47Code(bcp)
                code.construct_from_args("LANG", "SCRIPT", "VARIANT")
                assert code._lang_code == "LANG-SCRIPT-VARIANT"
                assert (
                    list(list(c) for c in m_add.call_args_list)
                    == [[(['LANG', 'SCRIPT', 'VARIANT'],
                          ('extlang', 'script', 'region', 'variant'),
                          'SCRIPT'), {}],
                        [(['LANG', 'SCRIPT', 'VARIANT'],
                          ('region', 'variant'),
                          'VARIANT'), {}]])


def test_bcp47_code_construct_from_args_language_script_unrecognized():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_prefix') as m_prefix:
            with patch('bcp47.BCP47Code._maybe_add_part') as m_add:
                m_prefix.side_effect = (
                    lambda parts, args: parts.append(args[0]))

                def _maybe_add(parts, tag_types, part):
                    if part.lower() not in tag_types:
                        return None, tag_types
                    parts.append(part)
                    return part, tag_types[tag_types.index(part.lower()) + 1:]

                m_add.side_effect = _maybe_add
                code = BCP47Code(bcp)
                with pytest.raises(BCP47Exception) as e:
                    code.construct_from_args("LANG", "SCRIPT", "NOTRECOGNIZED")
                assert (
                    e.value.args[0]
                    == "Unrecognized tag part 'NOTRECOGNIZED'")
                assert (
                    list(list(c) for c in m_add.call_args_list)
                    == [[(['LANG', 'SCRIPT'],
                          ('extlang', 'script', 'region', 'variant'),
                          'SCRIPT'), {}],
                        [(['LANG', 'SCRIPT'],
                          ('region', 'variant'),
                          'NOTRECOGNIZED'), {}]])
                assert code._lang_code is None


def test_bcp47_code_construct_from_args_language_variant_unrecognized():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_prefix') as m_prefix:
            with patch('bcp47.BCP47Code._maybe_add_part') as m_add:
                m_prefix.side_effect = (
                    lambda parts, args: parts.append(args[0]))

                def _maybe_add(parts, tag_types, part):
                    parts.append(part)
                    return part, tag_types[tag_types.index(part.lower()) + 1:]

                m_add.side_effect = _maybe_add
                code = BCP47Code(bcp)
                with pytest.raises(BCP47Exception) as e:
                    code.construct_from_args(
                        "LANG", "VARIANT", "NOTRECOGNIZED")
                assert (
                    e.value.args[0]
                    == "Unrecognized tag part 'NOTRECOGNIZED'")
                assert (
                    list(list(c) for c in m_add.call_args_list)
                    == [[(['LANG', 'VARIANT'],
                          ('extlang', 'script', 'region', 'variant'),
                          'VARIANT'), {}]])
                assert code._lang_code is None
