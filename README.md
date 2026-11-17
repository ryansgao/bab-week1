# Week 1: Fundamentals and Bitcoin

An interactive marimo notebook covering the cryptography behind blockchains (hashes, public-key encryption, signatures, elliptic curves) and how Bitcoin puts them together. It's part of the Blockchain at Berkeley education curriculum and is meant to be worked through on your own.

## Open it in the browser (no install)

**Open in your browser (no install, no account):** https://molab.marimo.io/github/ryansgao/bab-week1-fundamentals-notebook/blob/main/week1.py/wasm

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

Dependencies: `marimo` (tested on 0.25.2), `altair`, `numpy`, `pandas`. Everything else is the Python standard library (`hashlib`, `math`, `random`).

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

Learning objectives are at the top and key takeaways at the end. The homework and onchain completion step come in the next update.

## Files

| File | What it is |
| :--- | :--- |
| `week1.py` | The notebook |
| `requirements.txt` | Python dependencies |
| `CONTENT_UPDATES.md` | Every correction and addition made to the original lesson, with sources |
| `SECTION_CHECKLIST.md` | Where each original section is in the notebook |

There are no other assets: every chart and diagram is generated in the notebook.

## Testing (November 17, 2026)

- Clean run: in a fresh environment (`uv run --isolated --with-requirements requirements.txt`), all 76 cells execute without errors in under a second, `marimo check` passes, and `marimo export html` succeeds.
- Every control in a real browser: a headless Chromium script clicked through every slider, dropdown, text box, switch, button, tab, accordion and quick check, and checked the text each one should produce. No failures under `marimo run` or in the WebAssembly build.
- Checked in light and dark themes, at desktop width and at 390 px (phone width).
- WebAssembly: `marimo export html-wasm week1.py --mode run` was served locally and driven the same way. It boots in about 10 seconds. The slowest actions in the browser take 3 to 4 seconds: 5 practice blocks at 18 bits, 20 collision hunts on a 32-bit hash, and re-running the double-spend simulation at q = 49% with 50,000 races. Mining difficulty stops at 18 bits so that no single action takes longer.
- The double-spend simulation matches Rosenfeld's exact formula (q = 10%, z = 5: 0.176 to 0.185% simulated at 400,000 races, 0.178% exact), and the whitepaper formula reproduces the table in section 11 of the whitepaper (q = 10%, z = 5: 0.0009137).
- **Still to do:** a person outside the group works through it unaided .
