'''Python 2 had a package on the PYPI called Equation that did something like
safe_compute. This is a revival of that.
The Equation class is more or less a wrapper around safe_compute with
some extra math functions thrown in.
Every single-variable function in Python's built-in "math" module 
is available for use here.
'''
from math_eval import *
import math

safe_ufunctions.update({
    'acos': math.acos,
    'acosh': math.acosh,
    'asin': math.asin,
    'asinh': math.asinh,
    'atan': math.atan,
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'erf': math.erf,
    'erfc': math.erfc,
    'exp': math.exp,
    'expm1': math.expm1,
    'fabs': math.fabs,
    'factorial': math.factorial,
    'floor': math.floor,
    'frexp': math.frexp,
    'gamma': math.gamma,
    'gcd': math.gcd,
    'hypot': math.hypot,
    'isfinite': math.isfinite,
    'isinf': math.isinf,
    'isnan': math.isnan,
    'isqrt': math.isqrt,
    'lcm': math.lcm,
    'lgamma': math.lgamma,
    'log': math.log,
    'log10': math.log10,
    'log1p': math.log1p,
    'log2': math.log2,
    'modf': math.modf,
    'perm': math.perm,
    'radians': math.radians,
    'sin': math.sin,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh,
    'trunc': math.trunc,
    'ulp': math.ulp,
})
ufunctions |= safe_ufunctions

class Equation:
    def __init__(self, eqn):
        self.eqn = eqn
        self.expr = compute(eqn, safe = True)
        self.varnames = get_varnames(tokenize(eqn), safe = True)
        
    def __call__(self, *args):
        return self.expr(*args)
        
    def __repr__(self):
        return f"Equation({self.eqn})"
    __str__ = __repr__