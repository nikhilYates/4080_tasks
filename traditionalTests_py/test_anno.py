# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import anno as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    var_0 = module_0.keys(none_type_0)
    var_0.visit_withitem(none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    basic_0 = module_0.Basic.EXTRA_LOOP_TEST
    module_0.getanno(basic_0, basic_0)


def test_case_2():
    none_type_0 = None
    var_0 = module_0.getanno(none_type_0, none_type_0, none_type_0)
    var_1 = module_0.copyanno(none_type_0, none_type_0, none_type_0)


def test_case_3():
    none_type_0 = None
    var_0 = module_0.copyanno(none_type_0, none_type_0, none_type_0)
