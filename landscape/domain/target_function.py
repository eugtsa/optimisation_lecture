from typing import Any
from helpers.exceptions import TargetFunctionCalledOnPointOutOfDomainError
from sympy import diff, Symbol, sympify

from typing import List
import numpy as np
import bisect

def raise_(ex):
    raise ex

def interval_to_nums(s1,s2):
    if s1 == "-inf":
        s1 = np.NINF
    else:
        s1 = np.float64(s1)
    if s2 == "+inf":
        s2 = np.inf
    else:
        s2 = np.float64(s2)
    return s1,s2


class AbstractTargetFunction:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError()
    
    def check_domain(self,x):
        return self._domain_func(x)
    
class TargetFunction(AbstractTargetFunction):
    def __init__(self, func, defined_from="-inf", defined_to="+inf") -> None:
        self._func_str_repr = func
        self._func = None
        self._sympy_func = None
        self._compile_func()

        self.defined_from_repr = defined_from
        self.defined_to_repr = defined_to
        self._domain_func = None
        self._define_domain()

    def _compile_func(self):
        self._sympy_func = sympify(self._func_str_repr)
        self._sympy_dfunc = diff(self._sympy_func)
        self._sympy_ddfunc = diff(self._sympy_dfunc)
        
        self._func = lambda x: self._sympy_func.evalf(subs={Symbol('x'): x})
        self._dfunc = lambda x: self._sympy_dfunc.evalf(subs={Symbol('x'): x})
        self._ddfunc = lambda x: self._sympy_ddfunc.evalf(subs={Symbol('x'): x})

    def _define_domain(self):
        left_bound = lambda x:x
        right_bound = lambda x:x
        if self.defined_from_repr != "-inf":
            left_bound = lambda x: \
                raise_(TargetFunctionCalledOnPointOutOfDomainError()) if x<float(self.defined_from_repr) else x
        if self.defined_to_repr != "+inf":
            right_bound = lambda x: \
                raise_(TargetFunctionCalledOnPointOutOfDomainError()) if x>float(self.defined_to_repr) else x
        self._domain_func = lambda x: left_bound(right_bound(x))

    def check_domain(self, x):
        return self._domain_func(x)
    
    def deriv(self, x):
        self.check_domain(x)
        return self._dfunc(x)

    def dderiv(self, x):
        self.check_domain(x)
        return self._ddfunc(x)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.check_domain(*args)
        return self._func(*args)

class CompoundTargetFunction(AbstractTargetFunction):
    def populate_intervals(self, intervals_list):
        intervals = sorted([interval_to_nums(*i) for i in intervals_list],key=lambda x:x[0])
        self._l_sides = [i[0] for i in intervals]
        self._r_sides = [i[1] for i in intervals]

    def check_domain(self, x):
        left_index = bisect.bisect_left(self._l_sides, x)
        right_index = bisect.bisect_left(self._r_sides, x)
        if left_index - right_index == 1:
            if hasattr(self,'_tfs'):
                self._func_to_call = self._tfs[right_index]
            return x
        raise TargetFunctionCalledOnPointOutOfDomainError

    def combine_tfs(self, *tfs):
        self.populate_intervals([(tf.defined_from_repr,tf.defined_to_repr) for tf in tfs])

        self._tfs = tfs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.check_domain(*args)
        return self._func_to_call(*args)
    
    def deriv(self, *args: Any, **kwds: Any) -> Any:
        self.check_domain(*args)
        return self._func_to_call.deriv(*args)
    
    def dderiv(self, *args: Any, **kwds: Any) -> Any:
        self.check_domain(*args)
        return self._func_to_call.dderiv(*args)

    