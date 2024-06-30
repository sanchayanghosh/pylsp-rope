from pylsp_rope import commands, plugin, typing
from pylsp_rope.text import Range
from test.conftest import create_document, set_import_path
from test.helpers import (
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
    assert_text_edits,
)

import sys
import os
import unittest
import pylsp_rope
import ast
import pytest
import time
import rope


def create_dummy_relational_files(function_name: str, file_name: str, workspace):
    
    MODULE_NAME = "ModuleMoveFunction2"
    IMPORTED_MODULE = "move_source_function"
    import_node = ast.ImportFrom(module=IMPORTED_MODULE, names=[ast.alias(MODULE_NAME)], level=0)

    base_node = ast.Module(body=[], type_ignores=[])

    base_node.body.append(import_node)

    arguments_node = ast.arguments(posonlyargs=[],kwonlyargs=[], args=[], defaults=[])
    function_node = ast.FunctionDef(name=function_name, args=arguments_node, body=[
        ast.Call(ast.Name(MODULE_NAME), args=[], keywords=[])
        ], decorator_list=[],lineno=6)

    base_node.body.append(function_node)


    with open(os.path.join(workspace.root_path, file_name), mode='w') as f_o:
        f_o.write(ast.unparse(base_node))

    return os.path.join(workspace.root_path, file_name)

@pytest.mark.parametrize("nos", [1])
def test_pylsp_performance_multiple_changes(config, workspace, code_action_context, nos):
    
    set_import_path(module_path=os.path.join(os.path.dirname(__file__), 'fixtures', "lib"))

    document = create_document(workspace, "move_source_function.py")

    Nos = nos

    document_name_list = [(f"dependent{nos}.py", f"function{nos}") for nos in range(1, Nos)]

    document_path_list = [create_dummy_relational_files(function_name=each_deps[1], file_name=each_deps[0], workspace=workspace) for each_deps in document_name_list]

    


    source_name = "move_source_function.py"
    destination_document = create_document(workspace, "move_destination_function.py")
    dest_name = "move_destination_function.py"
    line = 9

    offset_range = sum([len(document.lines[each_line]) for each_line in range(line)])
    start_col = offset_range + document.lines[line].index("ModuleMoveFunction2")
    d_range = Range((line, start_col), (line, start_col+1)) 
    
    command = commands.COMMAND_MOVE
    
    response = plugin.pylsp_code_actions(config=config, context=code_action_context, range=d_range, document=document, workspace=workspace)


    arguments = [{
            "destination_document": dest_name
            }]
    
    time_of_start = time.time()


    
    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    print(f"Total time taken is {time.time() - time_of_start}")
    invalid_file_tuple = []
    for each_file_path in document_path_list:

        with open(each_file_path, mode='r') as f_o:
            file_contents = f_o.read()
            if "source_function" in file_contents:
                invalid_file_tuple.append((each_file_path, file_contents.index("source_function")))

    if len(invalid_file_tuple) > 0:
        print(",".join([f"File {each_file[0]} not processed at position {each_file[1]}" for each_file in invalid_file_tuple]))

        assert False
    

    


