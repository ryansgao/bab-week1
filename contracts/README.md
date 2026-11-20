# BabEduCompletions: shared completion record for the six B@B education weeks

One contract on Sepolia records every week's completions, so learners see the same flow in every notebook and the club can read all records in one place. Week 1's notebook uses it; any other week can call it unchanged with its own week number.

| | |
| :--- | :--- |
| Network | Ethereum Sepolia (chain ID 11155111) |
| Address | `0xAAbFe9b00f1c6d18367425D454371198A7a0624b` |
| Explorer | https://sepolia.etherscan.io/address/0xAAbFe9b00f1c6d18367425D454371198A7a0624b |
| Verified source | Sourcify exact match: https://repo.sourcify.dev/11155111/0xAAbFe9b00f1c6d18367425D454371198A7a0624b (also readable on https://eth-sepolia.blockscout.com/address/0xAAbFe9b00f1c6d18367425D454371198A7a0624b?tab=contract) |
| Deployed | November 20, 2026, block 12,173,450, tx `0xaa63258062b2e2f698b7de496abe6c4175c9c1e066faaadfdffabe4783355d17` |
| Compiler | Solidity 0.8.28, optimizer on, 200 runs |

## Interface

Gas: recording costs about 128,000 gas (about 0.00013 Sepolia ETH at November 2026 fees). Sending ETH to a brand-new address on Sepolia now costs about 200,000 gas, not 21,000, so never hard-code 21,000 for a transfer; let the wallet estimate.


```solidity
event Completed(address indexed learner, uint8 indexed week, uint256 timestamp);
function recordCompletion(uint8 week) external;                       // week 1–6; reverts "already recorded" on a repeat
function completedAt(address learner, uint8 week) external view returns (uint256);  // Unix time, 0 if not recorded
```

| Call | Selector | Calldata for week 1 |
| :--- | :--- | :--- |
| `recordCompletion(uint8)` | `0xfd9e6188` | `0xfd9e6188` + 63 zeros + `1` |
| `completedAt(address,uint8)` | `0x607544a3` | selector + address padded to 32 bytes + week padded to 32 bytes |

## The completion format

- **Public, onchain:** the learner's wallet (`msg.sender`), the week number, the block time. Nothing else.
- **Never onchain:** names, answers, scores. Keep them in the notebook (Week 1 keeps them in the browser's local storage).
- **One record per wallet per week.** Check `completedAt` before sending, and show "already recorded" instead of sending again.
- **It is a claim, not a proof.** Notebooks check answers locally, so say so before the learner approves the transaction.

## Using it from another week's notebook

Week 1's wallet widget (the `_HwWallet` anywidget in `week1.py`) needs no libraries: it talks to the learner's wallet through the standard browser wallet interface (EIP-1193 and EIP-6963), switches it to Sepolia, reads `completedAt`, and sends `recordCompletion(week)` with the calldata above. To reuse it, copy that cell and change `HW_WEEK`. It handles a missing wallet, wrong network, no test ETH, a rejected request, a failed transaction with retry, a reload while a transaction is pending, and an already-recorded wallet.

Reading every record: filter the contract's `Completed` events on Etherscan (Events tab), or call `eth_getLogs` with topic 0 = `0xd7fcf929356a08a8cc28839b644a1f85d8aabf80aad83114e4e3c9e43275776f`.
