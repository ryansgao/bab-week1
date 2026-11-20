"""Local EVM test of BabEduCompletions (eth-tester / py-evm). usage: python test_contract.py"""
import json
from web3 import Web3, EthereumTesterProvider
c = json.load(open("BabEduCompletions.json"))
w3 = Web3(EthereumTesterProvider())
a, b = w3.eth.accounts[:2]
tx = w3.eth.contract(abi=c["abi"], bytecode=c["bytecode"]).constructor().transact({"from": a})
addr = w3.eth.get_transaction_receipt(tx).contractAddress
k = w3.eth.contract(address=addr, abi=c["abi"])
assert k.functions.completedAt(a, 1).call() == 0
r = w3.eth.get_transaction_receipt(k.functions.recordCompletion(1).transact({"from": a}))
assert r.status == 1
ev = k.events.Completed().process_receipt(r)[0].args
assert ev.learner == a and ev.week == 1 and ev.timestamp > 0
assert k.functions.completedAt(a, 1).call() == ev.timestamp
assert k.functions.completedAt(b, 1).call() == 0 and k.functions.completedAt(a, 2).call() == 0
for bad, who in [(1, a), (0, b), (7, b)]:
    try:
        k.functions.recordCompletion(bad).transact({"from": who}); raise SystemExit(f"no revert for week {bad}")
    except Exception as e:
        assert "already recorded" in str(e) or "week must be 1-6" in str(e), e
# raw calldata the notebook sends must match the ABI encoding
assert k.encode_abi("recordCompletion", [1]) == "0xfd9e6188" + "0"*63 + "1"
print("contract: 7 checks passed")
