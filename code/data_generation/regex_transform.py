# [Possible Augmentations]
# - redundancy (add remove)
# - or permutation
# - constant content
# - number change
# - ...


import numpy as np
import random


class RegexTransfom(object):
    "Allow multiple transformations to an existing regular expression in NL-RX form"

    def __init__(self) -> None:
        self.candidates = []
        self.final = None

    def transform(self, regex: str, args):
        pass

    def __redundancy(self, regex: str, mode='add') -> str:
        if mode == 'add':
            pass
        elif mode == 'remove':
            pass
        else:
            raise NotImplementedError

    def __permutation(self, regex: str) -> str:
        pass

    def __constant(self, regex: str, mode='terminals') -> str:
        """
        Exchangable: <Mx>, <VOW>, <CAP>, <LOW>, ...
        """
        pass

    def __number(self, regex: str) -> str:
        pass