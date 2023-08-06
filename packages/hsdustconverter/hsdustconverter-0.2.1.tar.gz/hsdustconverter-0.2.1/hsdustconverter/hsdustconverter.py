"""Main module."""

VALUE_OF_COMMON = 5
VALUE_OF_RARE = 20
VALUE_OF_EPIC = 100
VALUE_OF_LEGENDARY = 400


def convertCommons(x):
    return x * VALUE_OF_COMMON


def convertRares(x):
    return x * VALUE_OF_RARE


def convertEpics(x):
    return x * VALUE_OF_EPIC


def convertLegendaries(x):
    return x * VALUE_OF_LEGENDARY
