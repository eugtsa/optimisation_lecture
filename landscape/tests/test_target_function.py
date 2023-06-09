from domain.target_function import TargetFunction,CompoundTargetFunction
from helpers.exceptions import TargetFunctionCalledOnPointOutOfDomainError
import pytest

def test_create_target_function():
    constant_tf = TargetFunction(func="2.0")
    assert constant_tf(0) == 2.0
    assert constant_tf(1) == 2.0

def test_quad_target_function_deriv():
    quad_tf = TargetFunction(func="x**2")
    assert quad_tf.deriv(0) == 0.0
    assert quad_tf.deriv(3) == 6.0
    assert quad_tf.dderiv(1) == 2
    
def test_target_function_domain_left():
    constant_tf = TargetFunction(func="2.0",defined_from="2.0")
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        assert constant_tf(0) == 2.0

def test_target_function_domain_right():
    constant_tf = TargetFunction(func="2.0",defined_to="2.0")
    assert constant_tf(0) == 2.0
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        assert constant_tf(5) == 2.0

def test_nonconstant_target_function_no_domain():
    tf = TargetFunction(func="x**2")
    assert tf(0) == 0.0
    assert tf(2.0) == 4.0
    
def test_domain_inf_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.populate_intervals(intervals_list=[("-inf","+inf"),])
    compound_tf.check_domain(2.0)

def test_domain_left_out_of_domain_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.populate_intervals(intervals_list=[("0.0","+inf"),])
    compound_tf.check_domain(2.0)
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        compound_tf.check_domain(-2.0)


def test_domain_right_out_of_domain_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.populate_intervals(intervals_list=[("-inf","0.0"),])
    compound_tf.check_domain(-2.0)
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        compound_tf.check_domain(2.0)

def test_domain_with_hole_domain_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.populate_intervals(intervals_list=[("-inf","0.0"),("2.0","5.0")])
    compound_tf.check_domain(-2.0)
    compound_tf.check_domain(3.0)
    compound_tf.check_domain(4.0)
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        compound_tf.check_domain(1.0)


def test_domain_with_hole2_domain_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.populate_intervals(intervals_list=[("-inf","0.0"),("2.0","5.0")])
    compound_tf.check_domain(-2.0)
    compound_tf.check_domain(3.0)
    compound_tf.check_domain(4.0)
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        compound_tf.check_domain(6.0)

def test_hole2_compound_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.combine_tfs(
        TargetFunction("x","-inf","0.0"),
        TargetFunction("-x","2.0","5.0"),
    )
    
    assert compound_tf(-2.0) == -2.0
    assert compound_tf(3.0) == -3.0
    assert compound_tf(4.0) == -4.0
    with pytest.raises(TargetFunctionCalledOnPointOutOfDomainError):
        compound_tf(6.0)

def test_hole2_compound_deriv_dderiv_target_function():
    compound_tf = CompoundTargetFunction()
    compound_tf.combine_tfs(
        TargetFunction("x**2","-inf","0.0"),
        TargetFunction("-x","2.0","5.0"),
    )
    
    assert compound_tf(-2.0) == 4.0
    assert compound_tf.deriv(-1) == -2.0

