# Week 1: Fundamentals and Bitcoin

An interactive marimo notebook covering the cryptography behind blockchains (hashes, public-key encryption, signatures, elliptic curves) and how Bitcoin puts them together. It's part of the Blockchain at Berkeley education curriculum and is meant to be worked through on your own.

## Open it in the browser (no install)

**molab link:** https://molab.marimo.io/github/ryansgao/bab-week1/blob/main/week1.py/wasm

The `/wasm` link runs the whole notebook in your browser with Pyodide, so there's nothing to install and no sign-in. The first load takes about 10 seconds while Python downloads.

## Run it locally

You need Python 3.10 or newer.

With [uv](https://docs.astral.sh/uv/) (recommended; the notebook declares its own dependencies):

```bash
uvx marimo run --sandbox week1.py
```

With pip:

```bash
pip install -r requirements.txt
marimo run week1.py
```

`marimo run` opens the lesson as an app with the code hidden. To read or change the code, use `marimo edit week1.py` instead.

Dependencies: `marimo` (tested on 0.25.2), `altair`, `numpy`, `pandas`, and `anywidget` (the dark-mode switch, saved progress and the wallet connection). Everything else is the Python standard library (`hashlib`, `math`, `random`).

## What's in it

All of the Week 1 lesson content in the original section order, with ten interactive experiments and four quick checks:

| Experiment | Section |
| :--- | :--- |
| Break a Caesar cipher (frequency analysis) | Ancient Cryptography |
| Hash lab: avalanche effect and collision hunting | Hash Functions |
| RSA by hand | RSA |
| Factor N like an attacker | RSA |
| Sign, tamper, verify (with a toy forgery search) | Digital Signatures |
| Elliptic curve playground, part 1 (adding points, with a B = −A switch) and part 2 (a finite field, with a find-k challenge) | Elliptic Curve Cryptography |
| Build, tamper, mine a 4-block chain | A Chain of Blocks |
| Merkle proof explorer | A Chain of Blocks |
| Mining work: practice blocks against the expected 2^b tries | Mining and Proof of Work |
| Double-spend race (the simulation), with a watch-one-race mode | Properties of Bitcoin |

Learning objectives are at the top and key takeaways at the end.

## Homework and onchain completion (about 30 minutes)

At the end of the notebook:

1. **Name and wallet.** Enter your name (it stays in your browser) and connect a browser wallet. The notebook has setup steps for MetaMask and free Sepolia test ETH.
2. **Guided coding (15–20 min).** Rebuild Bitcoin block 100,000's Merkle root and block hash: `sha256d`, `merkle_root`, then `serialize_header` and `block_hash`. Each task has starter code, two hints and checks that name the usual mistakes (single SHA-256, byte order, the odd-level duplicate, field order). A bonus task decodes the target from `bits`.
3. **Six questions (5–10 min)** with feedback on every answer.
4. **Record completion.** Once everything passes, one Sepolia transaction calls `recordCompletion(1)` on the shared contract. The notebook shows the confirmation and an Etherscan link.

Progress (name, code, answers) saves in the browser's local storage, so a refresh doesn't lose it; a sent transaction is remembered too, so a reload resumes waiting for it instead of sending a second one. **Start over** clears it.

What is public: the wallet address, the week number and the block time. Names and answers never leave the browser. The checks run locally, so the record is a completion claim, not proof that every answer was right. No real funds, private keys or seed phrases are involved.

## Shared testnet and contract

| | |
| :--- | :--- |
| Network | Ethereum Sepolia testnet (chain ID 11155111), agreed for all six weeks in #baby-edu-fa26 |
| Contract | `BabEduCompletions` at `0xAAbFe9b00f1c6d18367425D454371198A7a0624b` ([Etherscan](https://sepolia.etherscan.io/address/0xAAbFe9b00f1c6d18367425D454371198A7a0624b)) |
| Source | `contracts/BabEduCompletions.sol` (Solidity 0.8.28, optimizer 200 runs) |
| Test completion | HW_TEST_TX_LINK |

See `contracts/README.md` for the interface and how another week plugs in.

## Files

| File | What it is |
| :--- | :--- |
| `week1.py` | The notebook |
| `requirements.txt` | Python dependencies |
| `CONTENT_UPDATES.md` | Every correction and addition made to the original lesson, with sources |
| `SECTION_CHECKLIST.md` | Where each original section is in the notebook |
| `contracts/` | The shared completion contract and its interface |
| `TESTING.md` | Phase 3 testing note: timing, answer checks, progress recovery, transaction retries |
| `CONTRIBUTIONS.md` | Who did what |

There are no other assets: every chart and diagram is generated in the notebook.

## Testing (November 17, 2026)

- Clean run: in a fresh environment (`uv run --isolated --with-requirements requirements.txt`), all 76 cells execute without errors in under a second, `marimo check` passes, and `marimo export html` succeeds.
- Every control in a real browser: a headless Chromium script clicked through every slider, dropdown, text box, switch, button, tab, accordion and quick check, and checked the text each one should produce. No failures under `marimo run` or in the WebAssembly build.
- Checked in light and dark themes, at desktop width and at 390 px (phone width).
- WebAssembly: `marimo export html-wasm week1.py --mode run` was served locally and driven the same way. It boots in about 10 seconds. The slowest actions in the browser take 3 to 4 seconds: 5 practice blocks at 18 bits, 20 collision hunts on a 32-bit hash, and re-running the double-spend simulation at q = 49% with 50,000 races. Mining difficulty stops at 18 bits so that no single action takes longer.
- The double-spend simulation matches Rosenfeld's exact formula (q = 10%, z = 5: 0.176 to 0.185% simulated at 400,000 races, 0.178% exact), and the whitepaper formula reproduces the table in section 11 of the whitepaper (q = 10%, z = 5: 0.0009137).
- **Still to do:** a person outside the group works through it unaided (see `CONTRIBUTIONS.md`), and the molab `/wasm` link is checked once the file is on GitHub.
