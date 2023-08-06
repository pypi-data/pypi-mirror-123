import os
import pytest
import miscset


## miscset.dt


def test_dt_now():
    assert type(miscset.dt.now()) == str


## miscset.io

xtxt = miscset.io.read_lines("tests/example.txt")
xyaml = miscset.io.read_yaml("tests/example.yml")
xjson = miscset.io.read_json("tests/example.json")

def test_io_read_lines_type():
    assert type(xtxt) == list

def test_io_read_lines_content():
    assert len(xtxt) == 2

def test_io_read_json_type():
    assert type(xjson) == dict

def test_io_read_json_value_None():
    assert xjson["example_none"] is None

def test_io_read_yaml_type():
    assert type(xyaml) == dict

def test_io_read_yaml_value_None():
    assert xyaml["example_none"] is None

