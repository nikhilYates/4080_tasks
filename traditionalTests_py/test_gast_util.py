# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import gast.gast as module_0
import gast_util as module_1


@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.parse()


def test_case_1():
    none_type_0 = None
    var_0 = module_1.is_literal(none_type_0)
    assert var_0 is False
