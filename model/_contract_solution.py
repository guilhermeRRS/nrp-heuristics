# coding=utf-8
from typing import List, NewType

ThreeDimInt = NewType("ThreeDimInt", List[List[List[int]]]);

class Solution:
    solution: ThreeDimInt

    def __init__(self, solution: ThreeDimInt):
        self.solution = solution

    