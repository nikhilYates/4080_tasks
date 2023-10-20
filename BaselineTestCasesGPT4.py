import gast
import unittest

class python_baseline_tests(unittest.TestCase):

    # def as_tuple(self) : ConversionOptions (from converter)
    # Test python method 1

    def test_as_tuple_default_initialization():
        conversion_options = ConversionOptions()
        result = conversion_options.as_tuple()
        assert result == (False, False, True, frozenset({Feature.ALL})), f"Unexpected result: {result}"

    def test_as_tuple_custom_initialization():
        conversion_options = ConversionOptions(
            recursive=True,
            user_requested=True,
            internal_convert_user_code=False,
            optional_features={Feature.EQUALITY_OPERATORS, Feature.LISTS}
        )
        result = conversion_options.as_tuple()
        expected_features = frozenset({Feature.EQUALITY_OPERATORS, Feature.LISTS})
        assert result == (True, True, False, expected_features), f"Unexpected result: {result}"

    def test_as_tuple_empty_features():
        conversion_options = ConversionOptions(
            recursive=False,
            user_requested=False,
            internal_convert_user_code=True,
            optional_features=None
        )
        result = conversion_options.as_tuple()
        assert result == (False, False, True, frozenset()), f"Unexpected result: {result}"

    #  def __eq__(self, other) : ConversionOptions (from converter)
    # 2

    def test_eq_identical_instances():
        options_1 = ConversionOptions()
        options_2 = ConversionOptions()
        assert options_1 == options_2, "Expected two identical instances to be equal."

    def test_eq_different_attributes():
        options_1 = ConversionOptions(recursive=True)
        options_2 = ConversionOptions(recursive=False)
        assert not (options_1 == options_2), "Expected instances with different attributes to not be equal."

    def test_eq_different_features():
        options_1 = ConversionOptions(optional_features={Feature.EQUALITY_OPERATORS, Feature.LISTS})
        options_2 = ConversionOptions(optional_features={Feature.NAME_SCOPES, Feature.LISTS})
        assert not (options_1 == options_2), "Expected instances with different optional features to not be equal."

    # def uses(self, feature) : ConversionOptions (from converter)
    # 3

    def test_uses_all_feature():
        conversion_options = ConversionOptions(optional_features={Feature.ALL})
        assert conversion_options.uses(Feature.EQUALITY_OPERATORS) is True, "Expected True for EQUALITY_OPERATORS with ALL set"
        assert conversion_options.uses(Feature.LISTS) is True, "Expected True for LISTS with ALL set"

    def test_uses_specific_features():
        conversion_options = ConversionOptions(optional_features={Feature.EQUALITY_OPERATORS, Feature.LISTS})
        assert conversion_options.uses(Feature.EQUALITY_OPERATORS) is True, "Expected True for EQUALITY_OPERATORS"
        assert conversion_options.uses(Feature.LISTS) is True, "Expected True for LISTS"
        assert conversion_options.uses(Feature.NAME_SCOPES) is False, "Expected False for NAME_SCOPES"

    def test_uses_no_features():
        conversion_options = ConversionOptions(optional_features=None)
        assert conversion_options.uses(Feature.EQUALITY_OPERATORS) is False, "Expected False for EQUALITY_OPERATORS with no features set"
        assert conversion_options.uses(Feature.LISTS) is False, "Expected False for LISTS with no features set"

    #  def call_options(self) : ConversionOptions (from converter)
    # 3

    def test_call_options_default_initialization():
        original = ConversionOptions()
        result = original.call_options()

        assert result.recursive == original.recursive, f"Unexpected recursive value: {result.recursive}"
        assert result.user_requested == False, f"Unexpected user_requested value: {result.user_requested}"
        assert result.internal_convert_user_code == original.recursive, f"Unexpected internal_convert_user_code value: {result.internal_convert_user_code}"
        assert result.optional_features == original.optional_features, f"Unexpected optional_features value: {result.optional_features}"

    def test_call_options_recursive_true():
        original = ConversionOptions(recursive=True)
        result = original.call_options()

        assert result.recursive == True, f"Unexpected recursive value: {result.recursive}"
        assert result.user_requested == False, f"Unexpected user_requested value: {result.user_requested}"
        assert result.internal_convert_user_code == True, f"Unexpected internal_convert_user_code value: {result.internal_convert_user_code}"
        assert result.optional_features == original.optional_features, f"Unexpected optional_features value: {result.optional_features}"

    def test_call_options_recursive_false():
        original = ConversionOptions(recursive=False)
        result = original.call_options()

        assert result.recursive == False, f"Unexpected recursive value: {result.recursive}"
        assert result.user_requested == False, f"Unexpected user_requested value: {result.user_requested}"
        assert result.internal_convert_user_code == False, f"Unexpected internal_convert_user_code value: {result.internal_convert_user_code}"
        assert result.optional_features == original.optional_features, f"Unexpected optional_features value: {result.optional_features}"

    # def to_ast(self) : ConversionOptions (from converter)
    # 3

    def test_to_ast_default_initialization():
        import ast
        from tensorflow.python.autograph.pyct import parser

        conversion_options = ConversionOptions()
        result = conversion_options.to_ast()

        expected_code = "ag__.ConversionOptions(recursive=False, user_requested=False, optional_features=frozenset({ag__.Feature.ALL}), internal_convert_user_code=True)"
        expected_ast = parser.parse_expression(expected_code)

        assert ast.dump(result) == ast.dump(expected_ast), f"Unexpected AST result: {ast.dump(result)}"


    def test_to_ast_custom_initialization():
        import ast
        from tensorflow.python.autograph.pyct import parser

        conversion_options = ConversionOptions(
            recursive=True,
            user_requested=True,
            internal_convert_user_code=False,
            optional_features={Feature.EQUALITY_OPERATORS, Feature.LISTS}
        )
        result = conversion_options.to_ast()

        expected_code = "ag__.ConversionOptions(recursive=True, user_requested=True, optional_features=frozenset({ag__.Feature.EQUALITY_OPERATORS, ag__.Feature.LISTS}), internal_convert_user_code=False)"
        expected_ast = parser.parse_expression(expected_code)

        assert ast.dump(result) == ast.dump(expected_ast), f"Unexpected AST result: {ast.dump(result)}"


    def test_to_ast_empty_features():
        import ast
        from tensorflow.python.autograph.pyct import parser

        conversion_options = ConversionOptions(
            recursive=False,
            user_requested=False,
            internal_convert_user_code=True,
            optional_features=None
        )
        result = conversion_options.to_ast()

        expected_code = "ag__.ConversionOptions(recursive=False, user_requested=False, optional_features=frozenset(), internal_convert_user_code=True)"
        expected_ast = parser.parse_expression(expected_code)

        assert ast.dump(result) == ast.dump(expected_ast), f"Unexpected AST result: {ast.dump(result)}"

    # def of(self, node, default=None) : NoValue (from anno.py)

    def test_no_value_of_existing_annotation():
        node = gast.Name(id='x', ctx=gast.Load(), annotation=None, type_comment=None)
        key = Basic.QN
        value = "x_var"
        setanno(node, key, value)

        result = key.of(node)

        assert result == value, f"Expected {value}, but got {result}"

    def test_no_value_of_non_existing_annotation_with_default():
        node = gast.Name(id='y', ctx=gast.Load(), annotation=None, type_comment=None)
        key = Basic.QN
        default_value = "default_name"

        result = key.of(node, default=default_value)

        assert result == default_value, f"Expected {default_value}, but got {result}"

    def test_no_value_of_non_existing_annotation_without_default():
        node = gast.Name(id='z', ctx=gast.Load(), annotation=None, type_comment=None)
        key = Basic.QN

        try:
            result = key.of(node)
            assert False, "Expected exception but none occurred"
        except KeyError:
            pass

    # def exists(self, node) : NoValue (from anno.py)
    # 4

    def test_exists_anno_set():
        node = gast.Name(id='x', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.QN.add_to(node, "my_qn_value")

        assert Basic.QN.exists(node), "Annotation should be recognized as existing."


    def test_exists_anno_not_set():
        node = gast.Name(id='y', ctx=gast.Load(), annotation=None, type_comment=None)

        assert not Basic.ORIGIN.exists(node), "Annotation should not be recognized as existing."


    def test_exists_anno_after_removal():
        node = gast.Name(id='z', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.DIRECTIVES.add_to(node, "my_directive_value")
        delanno(node, Basic.DIRECTIVES)

        assert not Basic.DIRECTIVES.exists(node), "Annotation should not be recognized as existing after removal."

    # def __repr__(self) : NoValue (from anno.py)
    # 5

    def test_repr_basic_qn():
        repr_value = repr(Basic.QN)
        assert repr_value == "QN", f"Expected 'QN', but got {repr_value}"

    def test_repr_static_is_param():
        repr_value = repr(Static.IS_PARAM)
        assert repr_value == "IS_PARAM", f"Expected 'IS_PARAM', but got {repr_value}"

    class MockEnum(NoValue):
        MOCK_KEY = "This is just a mock key for testing purposes."


    # def keys(node, field_name='___pyct_anno') : (from anno.py)
    # 6

    def test_keys_multiple_annotations():
        node = gast.Name(id='a', ctx=gast.Load(), annotation=None, type_comment=None)
        Static.IS_PARAM.add_to(node, True)
        Static.SCOPE.add_to(node, "scope_value")

        annotation_keys = keys(node)
        assert Static.IS_PARAM in annotation_keys, "IS_PARAM key should be in the returned set."
        assert Static.SCOPE in annotation_keys, "SCOPE key should be in the returned set."


    def test_keys_no_annotations():
        node = gast.Name(id='b', ctx=gast.Load(), annotation=None, type_comment=None)

        annotation_keys = keys(node)
        assert not annotation_keys, "Returned set should be empty as no annotations are set."


    def test_keys_after_annotation_removal():
        node = gast.Name(id='c', ctx=gast.Load(), annotation=None, type_comment=None)
        Static.TYPES.add_to(node, "type_info")
        delanno(node, Static.TYPES)

        annotation_keys = keys(node)
        assert not annotation_keys, "Returned set should be empty after removing the annotation."

    # def getanno(node, key, default=FAIL, field_name='___pyct_anno') : (from anno.py)
    # 7

    def test_getanno_retrieve_set_annotation():
        node = gast.Name(id='a', ctx=gast.Load(), annotation=None, type_comment=None)
        expected_value = "function_param"
        Static.IS_PARAM.add_to(node, expected_value)

        value = Static.IS_PARAM.of(node)
        assert value == expected_value, f"Expected '{expected_value}', got '{value}'"

    def test_getanno_retrieve_default():
        node = gast.Name(id='b', ctx=gast.Load(), annotation=None, type_comment=None)
        default_value = "default_scope"

        value = Static.SCOPE.of(node, default=default_value)
        assert value == default_value, f"Expected default '{default_value}', got '{value}'"


    def test_getanno_retrieve_no_default():
        node = gast.Name(id='c', ctx=gast.Load(), annotation=None, type_comment=None)

        value = Static.TYPES.of(node)
        assert value is FAIL, "Expected 'FAIL' when no annotation set and no default provided"

    # def hasanno(node, key, field_name='___pyct_anno') : (from anno.py)
    # 8

    def test_hasanno_static_annotation_set():
        node = gast.Name(id='x', ctx=gast.Load(), annotation=None, type_comment=None)
        setanno(node, Static.IS_PARAM, True)

        assert hasanno(node, Static.IS_PARAM), "Static.IS_PARAM annotation should be recognized as existing."


    def test_hasanno_static_annotation_not_set():
        node = gast.Name(id='y', ctx=gast.Load(), annotation=None, type_comment=None)

        assert not hasanno(node, Static.SCOPE), "Static.SCOPE annotation should not be recognized as existing."


    def test_hasanno_static_annotation_after_removal():
        node = gast.Name(id='z', ctx=gast.Load(), annotation=None, type_comment=None)
        setanno(node, Static.LIVE_VARS_OUT, ["var_a", "var_b"])
        delanno(node, Static.LIVE_VARS_OUT)

        assert not hasanno(node,
                           Static.LIVE_VARS_OUT), "Static.LIVE_VARS_OUT annotation should not be recognized as existing after removal."

    # def dup(node, copy_map, field_name='___pyct_anno') : anno.py
    # 9

    def test_dup_basic_annotation():
        node = gast.Name(id='x', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.QN.add_to(node, "original_qn_value")

        # Copy QN to ORIGIN
        dup(node, {Basic.QN: Basic.ORIGIN})

        assert Basic.ORIGIN.exists(node), "Annotation should be copied."
        assert Basic.ORIGIN.of(node) == "original_qn_value", "The copied value should match the original."

    def test_dup_static_annotation():
        node = gast.Name(id='y', ctx=gast.Load(), annotation=None, type_comment=None)
        Static.LIVE_VARS_IN.add_to(node, ["var1", "var2"])

        # Copy LIVE_VARS_IN to LIVE_VARS_OUT
        dup(node, {Static.LIVE_VARS_IN: Static.LIVE_VARS_OUT})

        assert Static.LIVE_VARS_OUT.exists(node), "Static annotation should be copied."
        assert Static.LIVE_VARS_OUT.of(node) == ["var1", "var2"], "The copied value should match the original."

    def test_dup_multiple_annotations():
        node = gast.Name(id='z', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.QN.add_to(node, "original_qn_value")
        Static.TYPES.add_to(node, "int")

        # Copy QN to ORIGIN and TYPES to CLOSURE_TYPES
        dup(node, {Basic.QN: Basic.ORIGIN, Static.TYPES: Static.CLOSURE_TYPES})

        assert Basic.ORIGIN.exists(node) and Basic.ORIGIN.of(node) == "original_qn_value", "QN should be copied to ORIGIN."
        assert Static.CLOSURE_TYPES.exists(node) and Static.CLOSURE_TYPES.of(node) == "int", "TYPES should be copied to CLOSURE_TYPES."

    # def copyanno(from_node, to_node, key, field_name='___pyct_anno') : anno.py
    # 10

    def test_copy_existing_anno():
        source_node = gast.Name(id='a', ctx=gast.Load(), annotation=None, type_comment=None)
        dest_node = gast.Name(id='b', ctx=gast.Load(), annotation=None, type_comment=None)

        Basic.QN.add_to(source_node, "source_qn_value")
        copyanno(source_node, dest_node, Basic.QN)

        assert Basic.QN.exists(dest_node), "Annotation should exist in destination node after copy."
        assert Basic.QN.of(dest_node) == "source_qn_value", "Annotation value should match the source."


    def test_copy_non_existing_anno():
        source_node = gast.Name(id='c', ctx=gast.Load(), annotation=None, type_comment=None)
        dest_node = gast.Name(id='d', ctx=gast.Load(), annotation=None, type_comment=None)

        copyanno(source_node, dest_node, Basic.ORIGIN)

        assert not Basic.ORIGIN.exists(
            dest_node), "Annotation should not exist in destination node if it wasn't in the source."


    def test_overwrite_existing_anno_in_dest():
        source_node = gast.Name(id='e', ctx=gast.Load(), annotation=None, type_comment=None)
        dest_node = gast.Name(id='f', ctx=gast.Load(), annotation=None, type_comment=None)

        Basic.DIRECTIVES.add_to(source_node, "new_directive_value")
        Basic.DIRECTIVES.add_to(dest_node, "old_directive_value")
        copyanno(source_node, dest_node, Basic.DIRECTIVES)

        assert Basic.DIRECTIVES.of(
            dest_node) == "new_directive_value", "Annotation value in destination should be overwritten by the source's value."

    # def delanno(node, key, field_name='___pyct_anno') : anno.py
    # 11

    def test_delanno_existing_annotation():
        node = gast.Name(id='x', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.QN.add_to(node, "my_qn_value")

        delanno(node, Basic.QN)

        assert not Basic.QN.exists(node), "Annotation should have been deleted."


    def test_delanno_non_existing_annotation():
        node = gast.Name(id='y', ctx=gast.Load(), annotation=None, type_comment=None)

        # It shouldn't raise an exception, but it's a good practice to check such behaviors
        try:
            delanno(node, Basic.ORIGIN)
            assert True, "No error should be raised when deleting a non-existing annotation."
        except Exception:
            assert False, "An error was raised when trying to delete a non-existing annotation."


    def test_delanno_field_removal():
        node = gast.Name(id='z', ctx=gast.Load(), annotation=None, type_comment=None)
        Basic.DIRECTIVES.add_to(node, "my_directive_value")

        delanno(node, Basic.DIRECTIVES)

        assert not hasattr(node,
                           '___pyct_anno'), "The ___pyct_anno field should be removed after deleting the last annotation."

    # def copy_clean(node, preserve_annos=None) : ast_util.py
    # 12

    def test_copy_clean_basic():
        import ast

        original = ast.parse("a = 5")
        copy = copy_clean(original)

        assert isinstance(copy, ast.Module)
        assert len(copy.body) == 1
        assert isinstance(copy.body[0], ast.Assign)
        assert copy.body[0].targets[0].id == "a"
        assert copy.body[0].value.n == 5
        assert copy is not original
        assert copy.body[0] is not original.body[0]
        assert copy.body[0].targets[0] is not original.body[0].targets[0]
        assert copy.body[0].value is not original.body[0].value

    test_copy_clean_basic()


    def test_copy_clean_preserve_annotations():
        import ast

        original = ast.parse("a = 5")
        anno.setanno(original.body[0], "test_annotation", "annotation_value")

        copy = copy_clean(original, preserve_annos={"test_annotation"})

        assert anno.getanno(copy.body[0], "test_annotation") == "annotation_value"


    test_copy_clean_preserve_annotations()

    def test_copy_clean_ignore_double_underscore():
        import ast

        class CustomNode(ast.AST):
            __hidden_field = "should not be copied"

        original = CustomNode()
        copy = copy_clean(original)

        assert hasattr(original, "__hidden_field")
        assert not hasattr(copy, "__hidden_field")

    test_copy_clean_ignore_double_underscore()

    # def _process_name_node(self, node) : SymbolRenamer (from ast_util.py)
    # 13

    def test_process_name_node_basic_rename():
        import ast

        tree = ast.parse("a = 5")
        renamer = SymbolRenamer({'a': 'x'})
        transformed_tree = renamer.visit(tree)

        assert isinstance(transformed_tree.body[0].targets[0], ast.Name)
        assert transformed_tree.body[0].targets[0].id == "x"


    test_process_name_node_basic_rename()


    def test_process_name_node_no_rename():
        import ast

        tree = ast.parse("b = 5")
        renamer = SymbolRenamer({'a': 'x'})
        transformed_tree = renamer.visit(tree)

        assert isinstance(transformed_tree.body[0].targets[0], ast.Name)
        assert transformed_tree.body[0].targets[0].id == "b"


    test_process_name_node_no_rename()


    def test_process_name_node_expression_rename():
        import ast

        tree = ast.parse("result = a + b")
        renamer = SymbolRenamer({'a': 'x', 'b': 'y'})
        transformed_tree = renamer.visit(tree)

        assert isinstance(transformed_tree.body[0].value, ast.BinOp)
        assert isinstance(transformed_tree.body[0].value.left, ast.Name)
        assert transformed_tree.body[0].value.left.id == "x"
        assert isinstance(transformed_tree.body[0].value.right, ast.Name)
        assert transformed_tree.body[0].value.right.id == "y"


    test_process_name_node_expression_rename()

    # def _process_list_of_strings(self, names) : SymbolRenamer (from ast_util.py)
    # 14

    def test_process_list_of_strings_basic(self):
        renamer = SymbolRenamer({"old_name": "new_name"})
        names_list = ["old_name", "other_name"]
        result = renamer._process_list_of_strings(names_list)
        self.assertEqual(result, ["new_name", "other_name"])

    def test_process_list_of_strings_multiple_renames(self):
        renamer = SymbolRenamer({"name1": "new1", "name2": "new2"})
        names_list = ["name1", "name2"]
        result = renamer._process_list_of_strings(names_list)
        self.assertEqual(result, ["new1", "new2"])

    def test_process_list_of_strings_no_renames(self):
        renamer = SymbolRenamer({"name1": "new1"})
        names_list = ["name2", "name3"]
        result = renamer._process_list_of_strings(names_list)
        self.assertEqual(result, ["name2", "name3"])

    # def visit_Nonlocal(self, node) : SymbolRenamer (From ast_util.py)
    # 15

    def test_basic_rename_nonlocal(self):
        source = """
    def outer():
        a = 10
        def inner():
            nonlocal a
            a = 5
    """
        # Parse source code into AST.
        node = gast.parse(source)

        # Rename `a` to `b`.
        name_map = {qual_names.QN('a'): 'b'}
        renamer = SymbolRenamer(name_map)
        renamed_node = renamer.visit(node)

        # Convert the transformed AST back to source code.
        transformed_source = gast.dump(renamed_node)

        # Check that `a` has been renamed to `b` in nonlocal statement.
        self.assertIn("nonlocal b", transformed_source)

    def test_no_change_nonlocal(self):
        source = """
    def outer():
    a = 10
    def inner():
        nonlocal a
        a = 5
    """
        # Rename `b` to `c` (but `b` doesn't exist).
        name_map = {qual_names.QN('b'): 'c'}
        renamer = SymbolRenamer(name_map)
        renamed_node = renamer.visit(node)

        transformed_source = gast.dump(renamed_node)

        # `a` should remain unchanged.
        self.assertIn("nonlocal a", transformed_source)

    def test_multiple_variables_nonlocal(self):
        source = """
    def outer():
        a = 10
        b = 20
        def inner():
            nonlocal a, b
            a = 5
            b = 15
    """
        # Rename `a` to `x` and leave `b` unchanged.
        name_map = {qual_names.QN('a'): 'x'}
        renamer = SymbolRenamer(name_map)
        renamed_node = renamer.visit(node)

        transformed_source = gast.dump(renamed_node)

        # `a` should be renamed to `x`, and `b` should remain unchanged.
        self.assertIn("nonlocal x, b", transformed_source)

    # def visit_Attribute(self, node) : SymbolRenamer (from ast_util.py)
    # 16

    def test_rename_attribute_with_anno(self):
        # Set up a node with a qualifying name annotation
        node = gast.Attribute(value=gast.Name(id='obj', ctx=gast.Load()), attr='oldAttr', ctx=gast.Load())
        qn = qual_names.QN('obj.oldAttr')
        anno.setanno(node, anno.Basic.QN, qn)

        # Rename 'obj.oldAttr' to 'newAttr'
        renamer = SymbolRenamer({qn: 'newAttr'})
        result = renamer.visit_Attribute(node)

        self.assertIsInstance(result, gast.Attribute)
        self.assertEqual(result.attr, 'newAttr')

    def test_do_not_rename_attribute_without_anno(self):
        node = gast.Attribute(value=gast.Name(id='obj', ctx=gast.Load()), attr='oldAttr', ctx=gast.Load())

        renamer = SymbolRenamer({})
        result = renamer.visit_Attribute(node)

        self.assertIsInstance(result, gast.Attribute)
        self.assertEqual(result.attr, 'oldAttr')

    def test_do_not_rename_attribute_with_unmapped_anno(self):
        node = gast.Attribute(value=gast.Name(id='obj', ctx=gast.Load()), attr='oldAttr', ctx=gast.Load())
        qn = qual_names.QN('obj.oldAttr')
        anno.setanno(node, anno.Basic.QN, qn)

        renamer = SymbolRenamer({qual_names.QN('obj.someOtherAttr'): 'newAttr'})
        result = renamer.visit_Attribute(node)

        self.assertIsInstance(result, gast.Attribute)
        self.assertEqual(result.attr, 'oldAttr')


    # def visit_FunctionDef(self, node) : SymbolRenamer (ast_util.py)
    # 17

    def test_function_name_renaming(self):
        # Test if the function name is correctly renamed
        node = gast.parse("""
    def original_function():
        pass
            """)
        renamer = SymbolRenamer({"original_function": "renamed_function"})
        new_node = renamer.visit(node)
        self.assertEqual(new_node.body[0].name, "renamed_function")

    def test_function_name_unchanged(self):
        # Test if function name remains unchanged when not in the map
        node = gast.parse("""
    def untouched_function():
        pass
            """)
        renamer = SymbolRenamer({"original_function": "renamed_function"})
        new_node = renamer.visit(node)
        self.assertEqual(new_node.body[0].name, "untouched_function")

    def test_nested_name_processing(self):
        # Test if nested nodes inside the function are processed
        node = gast.parse("""
    def function_with_var():
        original_var = 10
            """)
        renamer = SymbolRenamer({"original_var": "renamed_var"})
        new_node = renamer.visit(node)
        self.assertEqual(new_node.body[0].body[0].targets[0].id, "renamed_var")

    # def rename_symbols(node, name_map) : ast_util.py
    # 18

    def test_rename_local_variable():
        code = """
    def foo():
        bar = 10
        return bar
    """
        node = ast.parse(code)
        gast_node = gast.ast_to_gast(node)

        # Annotate the node with qualified names.
        anno.setanno(gast_node, anno.Basic.QN, qual_names.QN('bar'))

        name_map = {qual_names.QN('bar'): 'renamed_bar'}

        renamed_node = rename_symbols(gast_node, name_map)

        # The variable 'bar' should be renamed to 'renamed_bar' in the output.
        assert "renamed_bar" in gast.dump(renamed_node)
        assert "bar" not in gast.dump(renamed_node)

    def test_rename_global_variable():
        code = """
    bar = 20
    def foo():
        global bar
        bar += 10
    """
        node = ast.parse(code)
        gast_node = gast.ast_to_gast(node)

        # Annotate the node with qualified names.
        anno.setanno(gast_node, anno.Basic.QN, qual_names.QN('bar'))

        name_map = {qual_names.QN('bar'): 'renamed_bar'}

        renamed_node = rename_symbols(gast_node, name_map)

        # The variable 'bar' should be renamed to 'renamed_bar' in the output.
        assert "renamed_bar" in gast.dump(renamed_node)
        assert "bar" not in gast.dump(renamed_node)

    def test_rename_function():
        code = """
    def bar():
        return 10
    """
        node = ast.parse(code)
        gast_node = gast.ast_to_gast(node)

        # Annotate the node with qualified names.
        anno.setanno(gast_node, anno.Basic.QN, qual_names.QN('bar'))

        name_map = {qual_names.QN('bar'): 'renamed_bar'}

        renamed_node = rename_symbols(gast_node, name_map)

        # The function 'bar' should be renamed to 'renamed_bar' in the output.
        assert "renamed_bar" in gast.dump(renamed_node)
        assert "bar" not in gast.dump(renamed_node)

    # def keywords_to_dict(keywords) : ast_util.py
    # 19

    def test_basic_functionality(self):
        # Create a simple keyword list
        keywords = [ast.keyword(arg='a', value=ast.Constant(value=1, kind=None))]

        # Convert the keywords to a gast.Dict
        result = keywords_to_dict(keywords)

        # Expected outcome
        expected = gast.Dict(keys=[gast.Constant(value='a', kind=None)],
                             values=[ast.Constant(value=1, kind=None)])

        # Assert the result
        self.assertEqual(ast.dump(result), ast.dump(expected))

    def test_empty_list(self):
        # Create an empty keyword list
        keywords = []

        # Convert the keywords to a gast.Dict
        result = keywords_to_dict(keywords)

        # Expected outcome
        expected = gast.Dict(keys=[], values=[])

        # Assert the result
        self.assertEqual(ast.dump(result), ast.dump(expected))

    def test_multiple_keywords(self):
        # Create a list with multiple keyword arguments
        keywords = [
            ast.keyword(arg='a', value=ast.Constant(value=1, kind=None)),
            ast.keyword(arg='b', value=ast.Constant(value=2, kind=None)),
            ast.keyword(arg='c', value=ast.Constant(value=3, kind=None))
        ]

        # Convert the keywords to a gast.Dict
        result = keywords_to_dict(keywords)

        # Expected outcome
        expected = gast.Dict(
            keys=[gast.Constant(value='a', kind=None), gast.Constant(value='b', kind=None), gast.Constant(value='c', kind=None)],
            values=[ast.Constant(value=1, kind=None), ast.Constant(value=2, kind=None), ast.Constant(value=3, kind=None)]
        )

        # Assert the result
        self.assertEqual(ast.dump(result), ast.dump(expected))

    # def compare_and_visit(self, node, pattern) : PatternMatcher (from ast_util.py)
    # 20

    def test_basic_matching_nodes(self):
        # Creating two similar nodes
        node = gast.parse("x + y")
        pattern = gast.parse("x + y")

        matcher = PatternMatcher(pattern)
        matcher.compare_and_visit(node, pattern)
        self.assertTrue(matcher.matches)

    def test_mismatching_nodes(self):
        # Creating two different nodes
        node = gast.parse("x + y")
        pattern = gast.parse("x - y")

        matcher = PatternMatcher(pattern)
        matcher.compare_and_visit(node, pattern)
        self.assertFalse(matcher.matches)

    def test_wildcards_in_pattern(self):
        # Creating a node and a pattern with wildcard
        node = gast.parse("x + y")
        pattern = gast.parse("x + _")  # Using wildcard for any right operand

        matcher = PatternMatcher(pattern)
        matcher.compare_and_visit(node, pattern)
        self.assertTrue(matcher.matches)








