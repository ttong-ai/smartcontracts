import json
import os
from solcx import compile_standard

CWD = os.path.dirname(__file__)

with open(os.path.join(CWD, "SimpleStorage.sol"), "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]},
            }
        },
    },
    solc_version="0.8.9",
)

print(compiled_sol)
with open(os.path.join(CWD, "compiled_code.json"), "w") as file:
    json.dump(compiled_sol, file)
