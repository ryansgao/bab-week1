# Phase 3 testing note (November 20, 2026)

## Homework timing

- Estimated, not yet measured on a person: about 2 + 8 + 6 minutes for the three coding tasks, 5–10 minutes for the six questions, 2–5 minutes to record (longer the first time, if MetaMask and test ETH are new).
- **Still to do:** time one person outside the group working through it unaided, and cut scope if it runs well past 30 minutes. The bonus task is optional and not counted.

## Answer checks

- Coding checks run the learner's code in the browser against block 100,000's real data, plus one- and three-transaction Merkle cases, and name the mistake when they recognize it. Tested offline against 20 solutions (`tests/homework_checks.py`): the correct ones pass; each of these gets its own message: placeholder left in, single SHA-256, hex string instead of bytes, hashing hex text, syntax error, runtime error with its line, txids not reversed, output not reversed, odd level dropped, integers big-endian, a hash not reversed, a hash added as text, two fields swapped, block hash not reversed, and a wrong bonus answer.
- The block data was checked independently: the four txids reproduce the Merkle root in the header, and the 80-byte header reproduces block 100,000's hash.
- Questions: feedback appears on every answer and explains the likely misconception. The Q5 answer (4 confirmations) is computed with the same exact formula as the double-spend simulation; the whitepaper's table gives the same answer.
- Completion needs: a name, Tasks 1–3 passing, and all six questions right.

## Progress recovery

Tested in the WebAssembly build in headless Chromium (`tests/wallet_flow.py`, 32 checks, 0 failures):

- A typed name survives a reload; a full saved solution restores and all checks pass again without any typing.
- **Start over** clears saved progress (the onchain record is unaffected).

## Transactions and retries

Same test, with a stand-in browser wallet backed by a local Ethereum test chain running the real contract:

- No wallet installed: the notebook says so and the record button stays off.
- Wallet rejects the request: "Nothing was sent", the button works again, no transaction exists.
- Success: confirmation with an Etherscan link; the contract shows the record for week 1 only.
- Reload after success: shows "already recorded" with the same link; nothing is sent again.
- Reload while a transaction is pending: the notebook keeps waiting on the same transaction and confirms it; still one transaction.
- Transaction fails onchain: explained, nothing recorded, retry succeeds.
- A wallet that recorded earlier from another browser: detected from the chain, nothing sent.
- The contract itself: 7 checks on a local EVM (`contracts/test_contract.py`): records once, rejects a repeat and weeks outside 1–6, stores the right week and time, and its calldata matches what the notebook sends.

## Live on Sepolia

- Test completion through the published notebook: HW_TEST_TX_LINK
