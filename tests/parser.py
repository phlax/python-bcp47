
from unittest.mock import PropertyMock, patch

import bcp47
from bcp47 import BCP47Parser


@patch('bcp47.BCP47Parser.parse_bcp')
def test_parser(m):
    BCP47Parser()
    assert m.called


@patch('bcp47.BCP47Parser.parse_bcp')
@patch('os.path.join')
@patch('os.path.dirname')
def test_parser_src_file(m_dirname, m_join, m):
    m_join.return_value = "FILEPATH"
    m_dirname.return_value = "DIRPATH"
    parser = BCP47Parser()
    assert parser.src_file == "FILEPATH"
    assert (
        list(m_join.call_args)
        == [('DIRPATH', parser.bcp_filename), {}])
    assert (
        list(m_dirname.call_args)
        == [(bcp47.parser.__file__, ), {}])


@patch('bcp47.BCP47Parser.parse_bcp')
@patch('bcp47.BCP47Parser.src_file', new_callable=PropertyMock)
@patch('bcp47.parser.open')
def test_parser_open(m_open, m_src, m):
    m_src.return_value = "SRC FILE"
    m_file = m_open.return_value.__enter__.return_value
    m_file.read.return_value = "\n".join(["1", "2", "3"])
    parser = BCP47Parser()
    result = list(parser.open())
    assert (
        list(m_open.call_args)
        == [('SRC FILE',), {}])
    assert m_open.return_value.__enter__.return_value.read.called
    assert result == ['1', '2', '3']


markup_simple = """
%%
Type: language
Subtag: aa
Description: Afar
Added: 2005-10-16
%%
Type: language
Subtag: ab
Description: Abkhazian
Added: 2005-10-16
Suppress-Script: Cyrl
"""


def test_simple_parse():
    pass
