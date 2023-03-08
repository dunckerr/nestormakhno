import pytest
import re
from nestormakhno import app

def test_genmask():
    assert app.genmask("", "", "a") == "[^a]"
    assert app.genmask("", "", "") == "."
    assert app.genmask("", "d", "a") == "[^da]"
    assert app.genmask("", "d", "") == "[^d]"
    assert app.genmask("p", "", "a") == "p"
    assert app.genmask("p", "", "") == "p"
    assert app.genmask("p", "d", "a") == "p"
    assert app.genmask("p", "d", "") == "p"
    assert app.genmask("pq", "d", "") == "p"
    assert app.genmask("", "dw", "") == "[^d]"
    assert app.genmask("", "dw", "fg") == "[^dfg]"
    assert app.genmask("", "", "asdg") == "[^asdg]"
    assert app.genmask("", "", "aaaa") == "[^aaaa]"

def test_gen_possibles_extra():

    ret = app.gen_possibles_extra("","","","","","","","","","","")
    assert len(ret) == 50
    ret = app.gen_possibles_extra("a","","","","","","","","","","wqerpoiru")
    assert len(ret) == 50

    # TODO this is broken we need to test for duplicates and
    # chars in g y and nots


def test_contains_all():

    # teststring charset
    assert app.containsAll("dunc", "c") == True
    assert app.containsAll("dunc", "") == True
    assert app.containsAll("dunc", "duncx") == False
    assert app.containsAll("", "d") == False
    assert app.containsAll("x", "x") == True
    assert app.containsAll("x", "") == True
    assert app.containsAll("dunc", "dc") == True
    assert app.containsAll("block", "u") == False

def test_new_gen():
    ds = [
        ['c', '', '', '', '',  '', '', '', 'a', ''],
        ['', 'a', '', '', '',  '', '', '', '', 'r'],
        ['', '', 'r', '', '',  '', 'c', '', '', ''],
        ['', '', '', '', '',   '', '', '', '', ''],
        ['', '', '', '', '',   '', '', '', '', ''],
    ]
    words, mask = app.new_gen(ds,'bnjkl')
    assert len(words) == 8


def test_regex():

    mask = 'a....'
    r = re.compile('^'+mask+'$')
    fp = open('lower-only', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))
    assert len(word5) == 2

