#!/usr/bin/env python

"""Tests for `hsdustconverter` package."""

import pytest


from hsdustconverter import hsdustconverter


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    
    expectedCommons = 100
    expectedRares = 200
    expectedEpics = 300
    expectedLegendaries = 400
    observedCommons = hsdustconverter.convertCommons(20)
    observedRares = hsdustconverter.convertRares(10)
    observedEpics = hsdustconverter.convertEpics(3)
    observedLegendaries = hsdustconverter.convertLegendaries(1)
    
    assert expectedCommons == observedCommons
    assert expectedRares == observedRares
    assert expectedEpics == observedEpics
    assert expectedLegendaries == observedLegendaries
