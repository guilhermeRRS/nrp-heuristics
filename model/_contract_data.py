# coding=utf-8
from typing import List, NewType

OneDimInt = NewType("OneDimInt", List[int]);
TwoDimInt = NewType("TwoDimInt", List[List[int]]);
ThreeDimInt = NewType("ThreeDimInt", List[List[List[int]]]);

class Sets:
    D:  OneDimInt;
    W:  OneDimInt;
    I:  OneDimInt;
    T:  OneDimInt;
    R_t: TwoDimInt;
    N_i: TwoDimInt;
    
    def __init__(self, D: OneDimInt, W: OneDimInt, I: OneDimInt, T: OneDimInt, R_t: TwoDimInt, N_i: TwoDimInt):
        self.D = D
        self.W = W
        self.I = I
        self.T = T
        self.R_t = R_t
        self.N_i = N_i

class Parameters:
    l_t:  OneDimInt;
    m_max: TwoDimInt;
    b_min:  OneDimInt;
    b_max:  OneDimInt;
    c_min:  OneDimInt;
    c_max:  OneDimInt;
    o_min:  OneDimInt;
    a_max:  OneDimInt;
    q: ThreeDimInt;
    p: ThreeDimInt;
    u: TwoDimInt;
    w_min: TwoDimInt;
    w_max: TwoDimInt;

    def __init__(self, l_t:  OneDimInt, m_max: TwoDimInt, b_min:  OneDimInt, b_max:  OneDimInt, c_min:  OneDimInt, c_max:  OneDimInt, o_min:  OneDimInt, a_max:  OneDimInt, q: ThreeDimInt, p: ThreeDimInt, u: TwoDimInt, w_min: TwoDimInt, w_max: TwoDimInt):
        
        self.l_t = l_t
        self.m_max = m_max
        self.b_min = b_min
        self.b_max = b_max
        self.c_min = c_min
        self.c_max = c_max
        self.o_min = o_min
        self.a_max = a_max
        self.q = q
        self.p = p
        self.u = u
        self.w_min = w_min
        self.w_max = w_max

class Data:

    sets: Sets
    parameters: Parameters

    def __init__(self, D:  OneDimInt, W:  OneDimInt, I: OneDimInt,T:  OneDimInt, R_t: TwoDimInt, N_i: TwoDimInt, l_t:  OneDimInt, m_max: TwoDimInt, b_min:  OneDimInt, b_max:  OneDimInt, c_min:  OneDimInt, c_max:  OneDimInt, o_min:  OneDimInt, a_max:  OneDimInt, q: ThreeDimInt, p: ThreeDimInt, u: TwoDimInt, w_min: TwoDimInt, w_max: TwoDimInt):
        
        self.sets = Sets(D = D, W = W, I = I, T = T, R_t = R_t, N_i = N_i)
        self.parameters = Parameters(l_t = l_t, m_max = m_max, b_min = b_min, b_max = b_max, c_min = c_min, c_max = c_max, o_min = o_min, a_max = a_max, q = q, p = p, u = u, w_min = w_min, w_max = w_max)