from __future__ import annotations

import builtins
import dis
import importlib
import inspect
import types
import unittest


SPLIT_MODULES = (
    "gmc_bridge.history_models",
    "gmc_bridge.report_periods",
    "gmc_bridge.service_metrology",
    "gmc_bridge.report_web_status",
    "gmc_bridge.report_web_devices",
)


def _nested_code_objects(code: types.CodeType):
    yield code
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            yield from _nested_code_objects(value)


class SplitModuleGlobalTests(unittest.TestCase):
    def test_source_defined_functions_have_resolvable_globals(self) -> None:
        missing: list[str] = []
        for module_name in SPLIT_MODULES:
            module = importlib.import_module(module_name)
            source_file = str(module.__file__)
            functions = []
            for value in vars(module).values():
                if inspect.isfunction(value) and value.__module__ == module_name:
                    functions.append(value)
                elif inspect.isclass(value) and value.__module__ == module_name:
                    functions.extend(
                        member
                        for member in vars(value).values()
                        if inspect.isfunction(member)
                        and member.__module__ == module_name
                        and member.__code__.co_filename == source_file
                    )
            for function in functions:
                if function.__code__.co_filename != source_file:
                    continue
                for code in _nested_code_objects(function.__code__):
                    for instruction in dis.get_instructions(code):
                        if instruction.opname != "LOAD_GLOBAL":
                            continue
                        name = str(instruction.argval)
                        if name not in module.__dict__ and not hasattr(builtins, name):
                            missing.append(f"{module_name}.{function.__qualname__}: {name}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
