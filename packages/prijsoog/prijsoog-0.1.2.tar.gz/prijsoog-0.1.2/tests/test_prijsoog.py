#!/usr/bin/env python

"""Tests for `prijsoog` package."""

import pytest

import re
from prijsoog import AhWatcher, JumboWatcher


def test_ah_watcher():
    """Test Albert Heijn price watcher"""
    AH = AhWatcher()
    products = AH.search("kiwi")

    # Test if there are no html tags in product name
    prod_name = list(products.keys())[0]
    tag_expr = re.compile(r'<.*?>')
    stripped_prod_name = tag_expr.sub('', prod_name) 
    assert prod_name == stripped_prod_name

    # Test if product price has the correct format
    prod_price = list(products.values())[0]
    str_prod_price = str(prod_price)
    assert len(str_prod_price.split('.')) == 2

def test_jumbo_watcher():
    """Test Jumbo price watcher"""
    Jumbo = JumboWatcher()
    products = Jumbo.search("kiwi")

    # Test if there are no html tags in product name
    prod_name = list(products.keys())[0]
    tag_expr = re.compile(r'<.*?>')
    stripped_prod_name = tag_expr.sub('', prod_name) 
    assert prod_name == stripped_prod_name

    # Test if product price has the correct format
    prod_price = list(products.values())[0]
    str_prod_price = str(prod_price)
    assert len(str_prod_price.split('.')) == 2