
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from bcp47 import BCP47, BCP47Code


def test_bcp47_code_construct_args_and_kwargs():
    bcp = BCP47()
    with pytest.raises(Exception) as e:
        BCP47Code(bcp, "foo", "bar", "baz", foo="foo0")
    assert e.value.args[0].startswith("Mixture of args and kwargs")


def test_bcp47_code_construct_no_args_or_kwargs():
    bcp = BCP47()
    with pytest.raises(Exception) as e:
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
        with pytest.raises(Exception) as e:
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
