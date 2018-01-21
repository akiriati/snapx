import os

import pytest
import json





def pytest_runtest_setup(item):
    # called for running each test in 'a' directory
    print ("setting up", item)


def pytest_addoption(parser):
    # type: (Parser) -> None
    parser.addoption(
        '--pysnapx-update',
        dest='pysnapx_update',
        action='store_true',
        default=False,
        help='Add this flag to override the snapshot'
    )




class Snapx():
    def __init__(self, file_name, function_name, update):
        self.file_name = file_name
        self.snapx_file_name = file_name.replace(".py", ".snapx.json")
        self.function_name = function_name
        self.update = update

    def to_match_snapshot(self, snapshot):
        if self.update:
            test_function_found = False
            data = []

            if os.path.isfile(self.snapx_file_name):
                with open(self.snapx_file_name, "r") as data_file:
                    data = json.load(data_file)
                    for tested_function in data:
                        if tested_function["function_name"] == self.function_name:
                            tested_function["snapshot"] = snapshot
                            test_function_found = True

            if not test_function_found:
                data.append({
                    'function_name': self.function_name,
                    'snapshot': snapshot
                })

            with open(self.snapx_file_name, "w+") as data_file:
                data_file.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, data_file, indent=4)
                data_file.truncate()  # remove remaining part
                return True
        else:
            with open(self.snapx_file_name, "r") as data_file:
                data = json.load(data_file)
                for tested_function in data:
                    if tested_function["function_name"] == self.function_name:
                        return tested_function["snapshot"] == snapshot


    def get_snapshot(self):
        pass


@pytest.fixture
def snapx(request):
    print (request.module.__file__, request._pyfuncitem.name, request.config.option.pysnapx_update)
    return Snapx(request.module.__file__,
                 request._pyfuncitem.name,
                 request.config.option.pysnapx_update)
