# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.25",
#     "altair>=5",
#     "numpy>=1.24",
#     "pandas>=2.0",
#     "anywidget>=0.9",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Week 1: Fundamentals and Bitcoin")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import hashlib
    import math
    import random
    import string
    import time
    import numpy as np
    import pandas as pd
    import altair as alt
    return alt, hashlib, math, mo, np, pd, random, string, time


@app.cell(hide_code=True)
def _(hashlib, mo):
    # Shared helpers used by every section.

    _box_style = {
        "border": "1px solid rgba(127,127,127,0.28)",
        "border-radius": "12px",
        "padding": "18px 22px",
        "background": "rgba(127,127,127,0.05)",
    }

    def experience(title, *parts):
        """Wrap an interactive experiment in a labeled box."""
        return mo.vstack(
            [mo.md(f"#### Try it: {title}"), *parts], gap=1
        ).style(_box_style)

    def howto(text):
        return mo.callout(mo.md(text), kind="info")

    def quiz_feedback(choice, answers):
        """answers maps each option label to (is_correct, explanation)."""
        if not choice:
            return mo.md("*Pick an answer to see feedback.*")
        ok, why = answers[choice]
        head = "**Right.** " if ok else "**Not quite.** "
        return mo.callout(mo.md(head + why), kind="success" if ok else "danger")

    def further_reading(links):
        """links: list of (title, url, note)."""
        lines = [f"- [{t}]({u}){(' - ' + n) if n else ''}" for t, u, n in links]
        return mo.accordion({"Further reading": mo.md("\n".join(lines))})

    def sha256_hex(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def sha256d(data: bytes) -> bytes:
        """Bitcoin's double SHA-256."""
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def leading_zero_bits(hex_digest: str) -> int:
        value = int(hex_digest, 16)
        return len(hex_digest) * 4 - value.bit_length()

    def short(h: str, n: int = 10) -> str:
        return h[:n] + "…"

    return (
        experience,
        further_reading,
        howto,
        leading_zero_bits,
        quiz_feedback,
        sha256_hex,
        sha256d,
        short,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md("**Week 1**  \nFundamentals and Bitcoin"),
            mo.nav_menu(
                {
                    "#learning-objectives": "Learning objectives",
                    "#first-lecture-woooo": "First lecture!",
                    "#cryptography-101": "Cryptography 101",
                    "#hash-functions": "Hash functions",
                    "#examples-of-asymmetric-encryption": "Asymmetric encryption",
                    "#digital-signatures": "Digital signatures",
                    "#elliptic-curve-cryptography-ecc": "Elliptic curves",
                    "#bitcoin-an-introduction-to-blockchain": "Bitcoin",
                    "#mining-and-proof-of-work": "Mining",
                    "#from-a-chain-to-a-network": "The network",
                    "#properties-of-bitcoin": "Properties of Bitcoin",
                    "#key-takeaways": "Key takeaways",
                    "#homework": "Homework",
                    "#sources": "Sources",
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Page styling and the dark-mode switch.
    # The CSS lifts marimo's 610 px cap on cell outputs, so long outputs show in
    # full with no inner scroll box. (App(css_file=...) would do the same when run
    # locally, but the molab/marimo.app WebAssembly link never loads that file.)
    # The switch flips marimo's own theme through the data-vscode-theme-kind
    # attribute on <body>, which marimo watches; charts and widgets follow it.
    import anywidget

    _page_css = """
    <style>
    .marimo-cell .output-area,
    .marimo-cell .console-output-area { max-height: none !important; overflow: visible !important; }
    </style>
    """

    class _DarkModeSwitch(anywidget.AnyWidget):
        _esm = """
        function render({ el }) {
          const label = document.createElement("label");
          const input = document.createElement("input");
          input.type = "checkbox";
          input.setAttribute("role", "switch");
          const sync = () => { input.checked = document.body.classList.contains("dark"); };
          sync();
          input.addEventListener("change", () => {
            document.body.dataset.vscodeThemeKind = input.checked ? "vscode-dark" : "vscode-light";
          });
          const watch = new MutationObserver(sync);
          watch.observe(document.body, { attributes: true, attributeFilter: ["class"] });
          label.append(input, document.createTextNode("Dark mode"));
          el.append(label);
          return () => watch.disconnect();
        }
        export default { render };
        """
        _css = """
        label { display: inline-flex; align-items: center; gap: 8px; cursor: pointer;
                font-size: 0.875rem; color: var(--slate-11, #555); user-select: none; }
        input { appearance: none; -webkit-appearance: none; margin: 0; cursor: pointer;
                width: 34px; height: 20px; border-radius: 999px; position: relative;
                background: var(--slate-6, #ccc); transition: background 0.15s; }
        input::after { content: ""; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px;
                       border-radius: 50%; background: #fff; transition: transform 0.15s; }
        input:checked { background: var(--blue-9, #3b82f6); }
        input:checked::after { transform: translateX(14px); }
        input:focus-visible { outline: 2px solid var(--blue-8, #3b82f6); outline-offset: 2px; }
        """

    mo.vstack([mo.Html(_page_css), mo.hstack([_DarkModeSwitch()], justify="end")], gap=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Week 1: Fundamentals and Bitcoin

    - Read top to bottom. Each shaded box is an experiment: answer its question in your head, then change the controls.
    - Collapsed sections are optional extras.
    - You need algebra and a little Python; modular arithmetic is explained when it comes up. You can skip the faded code cells: the lesson reads without them.

    ## Learning objectives

    After this week you can:

    1. Say what a cryptographic hash function guarantees, and explain why a longer output is harder to attack.
    2. Tell symmetric, asymmetric and hybrid encryption apart, and say which protects the data in HTTPS.
    3. Generate an RSA key pair by hand with small primes, encrypt and sign with it, and explain why factoring is the hard part.
    4. Add points on an elliptic curve and explain why multiplying a point by a secret number works as a trapdoor.
    5. List what goes in a Bitcoin block header and explain why editing an old block means redoing the work for every block after it.
    6. Explain how nodes choose between competing chains, and estimate a double-spend's odds from the attacker's share and the confirmations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # First lecture! Woooo

    ### Important discussions that we need to have:

    - **Building your cohort 🤝**
      - Our biggest piece of advice is to connect with the people starting alongside you.
      - You're college students in a college club, so drop the formalities.
      - Introduce yourselves, find out what classes everyone is taking, form study groups, make group chats, and text each other 😴💤 during long meetings.
        - Most of the friendships people take away from this club start in their B@By cohort.
    - **Crypto / blockchain imposter syndrome 👻**
      - Some of you already care a lot about crypto and some of you don't care at all yet. Either is completely fine.
      - Nobody is keeping score of who knew the most coming in. We want everyone to leave with ideas that carry over to any part of tech.
        - A blockchain is an event-based distributed system with financial incentives.
        - So is most of big tech.
      - This club is a bunch of people who can pick up a very niche topic very quickly. You're all curious, and that's the important part.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "**B@B members:** star the Slack channels you actually use. "
            "The channel count grows fast over a semester."
        ),
        kind="neutral",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Cryptography 101

    - Anything you send over the internet passes through machines you don't control, and any of them could read it or change it.
    - **Cryptography** protects information from adversaries like these. It does two separate jobs:
      - **Confidentiality**: keeping a message secret from anyone who isn't supposed to read it.
      - **Integrity and authenticity**: proving the message wasn't altered, and who sent it.
    - "Crypt" means hidden and "graph" means writing (from the Greek *kryptós* and *graphein*).
    - You use both every day: HTTPS, encrypted chats, password logins, software updates, blockchain transactions and zero-knowledge proofs.
      - Bitcoin barely uses the first job. Its signatures prove who authorized a payment, and its hashes show that past blocks haven't been rewritten.

    ## A Brief Overview

    | When | What happened |
    | :--- | :--- |
    | Ancient Greece | The Spartan *scytale* |
    | 1st century BCE | Julius Caesar's substitution cipher |
    | 9th century | Al-Kindi describes frequency analysis, which breaks simple substitution ciphers |
    | 1920s–1945 | Enigma rotor machines; Allied codebreakers at Bletchley Park |
    | 1976–1977 | Diffie–Hellman key exchange; RSA public-key encryption |
    | 1985 | Koblitz and Miller independently propose elliptic curve cryptography |
    | 2001–2002 | NIST publishes AES (2001) and the SHA-2 hash family (2002) |
    | 2008–2009 | Bitcoin whitepaper (Oct 2008); the network launches (Jan 2009) |
    | 2015 | SHA-3 standardized (FIPS 202) |
    | Aug 2024 | NIST publishes its first post-quantum standards |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ### Ancient Cryptography

    These are historical, and none would last a minute against a modern attacker. Two of their ideas stuck: a secret key shared in advance, and attacks that exploit patterns in language.

    - **Scytale (ancient Sparta)**, a transposition cipher
      - Wrap a strip of parchment around a rod, write along the rod, then unwind it. The loose strip looks scrambled.
      - The receiver winds it around a rod of the same diameter, so the diameter is the key.
      - *How it's broken:* only a handful of rod diameters make sense, so you try them all 🙂
    """),
            mo.accordion(
                {
                    "Did the Spartans really use it for secrets?": mo.md(
                        "Possibly not: the detailed accounts of the scytale as a cipher come from writers centuries "
                        "later, such as Plutarch, and historians still debate whether the Spartans used it for secrecy "
                        "at all (Kelly, \"The Myth of the Skytale\", 1998)."
                    )
                }
            ),
            mo.md(r"""
    - **Caesar cipher (1st century BCE)**, a substitution cipher
      - Shift every letter a fixed number of places in the alphabet. The Roman historian Suetonius says Caesar used a shift of 3.
        - With shift 3, A becomes D, so Hello becomes Khoor (case doesn't change). Check it letter by letter.
      - *How it's broken:* there are only 25 useful shifts, so trying all of them takes minutes by hand.
      - Long messages fall even faster to **frequency analysis**.
        - English uses some letters far more than others (E, T and A top the list).
        - A substitution cipher keeps those counts intact, so the most common letter in the ciphertext is probably E.
    """),
            mo.accordion(
                {
                    "Its bigger relative: the Vigenère cipher": mo.md(
                        "Vigenère uses a different shift for each position, following a repeating keyword. That hides "
                        "the letter counts better, but once you work out the keyword's length, every k-th letter is a "
                        "plain Caesar cipher again and frequency analysis breaks it."
                    )
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, string):
    ALPHABET = string.ascii_uppercase
    # Approximate letter frequencies in English text, in percent.
    ENGLISH_FREQ = {
        "A": 8.2, "B": 1.5, "C": 2.8, "D": 4.3, "E": 12.7, "F": 2.2, "G": 2.0,
        "H": 6.1, "I": 7.0, "J": 0.15, "K": 0.8, "L": 4.0, "M": 2.4, "N": 6.7,
        "O": 7.5, "P": 1.9, "Q": 0.1, "R": 6.0, "S": 6.3, "T": 9.1, "U": 2.8,
        "V": 1.0, "W": 2.4, "X": 0.15, "Y": 2.0, "Z": 0.07,
    }

    def caesar_shift(text, k):
        """Shift letters by k places, keeping case and leaving other characters alone."""
        out = []
        for ch in text:
            if "A" <= ch <= "Z":
                out.append(chr((ord(ch) - 65 + k) % 26 + 65))
            elif "a" <= ch <= "z":
                out.append(chr((ord(ch) - 97 + k) % 26 + 97))
            else:
                out.append(ch)
        return "".join(out)

    def letter_freqs(text):
        letters = [c for c in text.upper() if c in ALPHABET]
        total = max(len(letters), 1)
        return {L: 100 * letters.count(L) / total for L in ALPHABET}

    def english_score(text):
        """Chi-squared distance from English letter frequencies. Lower is more English-like."""
        letters = [c for c in text.upper() if c in ALPHABET]
        n = max(len(letters), 1)
        score = 0.0
        for L in ALPHABET:
            expected = n * ENGLISH_FREQ[L] / 100
            score += (letters.count(L) - expected) ** 2 / expected
        return score

    _secret_plain = (
        "Frequency analysis was described by the scholar al-Kindi in the ninth "
        "century. Count the letters in a long enough message and the most common "
        "one very likely stands for E, the next for T, and so on. Guess a few "
        "letters correctly and the rest of the message falls out quickly."
    )
    SECRET_SHIFT = 11
    caesar_secret = caesar_shift(_secret_plain, SECRET_SHIFT)

    caesar_plain = mo.ui.text_area(
        value="Hello, meet me at the Campanile at noon.", label="Your message", full_width=True
    )
    caesar_k = mo.ui.slider(0, 25, value=3, label="Shift", show_value=True)
    crack_k = mo.ui.slider(
        0, 25, value=0, label="Try decrypting with shift", show_value=True, full_width=True
    )
    return (
        ALPHABET,
        ENGLISH_FREQ,
        SECRET_SHIFT,
        caesar_k,
        caesar_plain,
        caesar_secret,
        caesar_shift,
        crack_k,
        english_score,
        letter_freqs,
    )


@app.cell(hide_code=True)
def _(
    ALPHABET,
    ENGLISH_FREQ,
    SECRET_SHIFT,
    alt,
    caesar_k,
    caesar_plain,
    caesar_secret,
    caesar_shift,
    crack_k,
    english_score,
    experience,
    letter_freqs,
    mo,
    pd,
):
    _cipher = caesar_shift(caesar_plain.value, caesar_k.value)
    _attempt = caesar_shift(caesar_secret, -crack_k.value)

    _obs = letter_freqs(_attempt)
    _rows = [
        {"letter": L, "source": "Your decryption", "percent": round(_obs[L], 2)}
        for L in ALPHABET
    ] + [
        {"letter": L, "source": "Typical English", "percent": ENGLISH_FREQ[L]}
        for L in ALPHABET
    ]
    _chart = (
        alt.Chart(pd.DataFrame(_rows))
        .mark_bar()
        .encode(
            x=alt.X("letter:N", sort=list(ALPHABET), title="Letter"),
            xOffset=alt.XOffset("source:N"),
            y=alt.Y("percent:Q", title="Share of letters (%)"),
            color=alt.Color(
                "source:N",
                scale=alt.Scale(domain=["Your decryption", "Typical English"], range=["#4c78a8", "#bab0ac"]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            tooltip=["letter", "source", "percent"],
        )
        .properties(height=220, width="container", title="Letter frequencies")
    )

    if crack_k.value == SECRET_SHIFT:
        _feedback = mo.callout(
            mo.md(
                f"Cracked: the key was a shift of {SECRET_SHIFT}. The blue bars now sit on the grey ones "
                "(tall E and T, almost no Q or Z). With any wrong shift the tall bars land on the wrong "
                "letters, so you can read the key off the chart without trying every shift."
            ),
            kind="success",
        )
    else:
        _feedback = mo.callout(
            mo.md(
                "Not English yet. Find the tallest blue bar: in English that letter is most "
                "likely E. How far is it from E in the alphabet?"
            ),
            kind="neutral",
        )

    _table = sorted(
        (
            {
                "shift": k,
                "first 45 characters": caesar_shift(caesar_secret, -k)[:45],
                "distance from English": round(english_score(caesar_shift(caesar_secret, -k)), 1),
            }
            for k in range(1, 26)
        ),
        key=lambda r: r["distance from English"],
    )

    experience(
        "Break a Caesar cipher",
        mo.md("**1. Encrypt something.** Type a message and pick a shift."),
        mo.hstack([caesar_plain, caesar_k], widths=[3, 1], align="center", wrap=True),
        mo.md(f"Ciphertext: `{_cipher}`"),
        mo.md(
            "**2. Crack a message.** The shift is unknown. Can you guess it from the letter counts in the "
            "chart before trying any? Then move the slider until the text reads as English."
        ),
        mo.md(f"> {caesar_secret}"),
        crack_k,
        mo.md(f"Your decryption: *{_attempt}*"),
        _chart,
        _feedback,
        mo.accordion(
            {
                "Brute force: all 25 shifts, ranked by how English they look": mo.ui.table(
                    _table, selection=None, pagination=False
                )
            }
        ),
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            mo.md(r"""
    - **World War II: the Enigma machine**, a rotor cipher used by Nazi Germany
      - Each keypress sent current through a set of rotors that swapped one letter for another, then turned the rotors.
        - So the swap changed with every letter: press E twice and you get two different letters.
        - That defeats simple frequency analysis, because no single ciphertext letter stands for E.
      - **Bletchley Park** was the Allied codebreaking site in Britain. Alan Turing, Gordon Welchman, Bill Tutte, John Tiltman and others broke Enigma and the Lorenz cipher.
        - To do it they built machines: the electromechanical Bombe for Enigma, and Colossus (1944) for Lorenz, one of the first programmable electronic computers. (Turing's abstract "Turing machine" dates from his 1936 paper.)
      - The 2014 film *The Imitation Game* is about this, and takes liberties with the history.
    """),
            further_reading(
                [
                    ("Exploiting the Tiltman Break (Computerphile)", "https://www.youtube.com/watch?v=-hrNWRtDr7Y", "how Lorenz was broken"),
                    ("Enigma machine (Crypto Museum)", "https://www.cryptomuseum.com/crypto/enigma/", "detailed history and internals"),
                    ("A brief history of cryptography (IBM)", "https://www.ibm.com/think/topics/cryptography-history", ""),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ## Types of Cryptography

    - Say you send your card number to an online store. Anyone between you and the store can read it.
    - **1. Symmetric-key cryptography**
      - You and the store share one secret key and use it to encrypt and decrypt.
      - It's fast: most laptop and phone processors have dedicated instructions for AES, the Advanced Encryption Standard (FIPS 197, 2001).
      - But you and the store need the same key first, and sending it over the internet has the same problem as the card number.
    - **2. Asymmetric-key (public-key) cryptography**
      - There's no shared key. Each person has a key pair: a public key they publish and a private key they never share.
      - Anyone can encrypt to you with your public key, and only your private key decrypts. RSA, elliptic curve cryptography and most post-quantum schemes work this way.
      - But it's much slower, far too slow to encrypt every byte of a connection.
    - **3. Key exchange protocols**
      - Use public-key cryptography once, at the start, to agree on a fresh symmetric key. Then encrypt everything else with that fast key.
      - HTTPS (TLS 1.3) works this way:
        - Your browser and the server run a Diffie–Hellman key exchange to agree on a session key.
        - The server signs the exchange with its certificate's key, so you know you're talking to the real site.
        - Everything after that, including the card number, is encrypted with a symmetric cipher such as AES-GCM.
    """),
            mo.accordion(
                {
                    "What browsers do now (as of November 2026)": mo.md(
                        "Browsers run a classical elliptic-curve exchange and a post-quantum one together, so the session "
                        "key stays safe even if one of the two is broken. Chrome turned this on by default in version 124 "
                        "(April 2024) and moved to the standardized version, X25519MLKEM768, in version 131. Desktop "
                        "Firefox has used it by default since version 132, and Safari since version 26."
                    )
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
    sequenceDiagram
        participant B as Your browser
        participant S as Website
        B->>S: Hello, plus a key share
        S->>B: Its key share, certificate, and a signature over the handshake
        Note over B,S: Both compute the same session key. Nobody watching can.
        B->>S: Card number, encrypted with AES-GCM under the session key
        S->>B: Order confirmation, encrypted the same way
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_types = mo.ui.radio(
        options=[
            "Asymmetric: it's encrypted with the server's public key",
            "Symmetric: it's encrypted with the session key",
            "Neither: HTTPS only proves who the server is",
        ],
        label="Quick check: you upload a 20 MB file over HTTPS. What encrypts the file's bytes?",
    )
    quiz_types
    return (quiz_types,)


@app.cell(hide_code=True)
def _(quiz_feedback, quiz_types):
    quiz_feedback(
        quiz_types.value,
        {
            "Asymmetric: it's encrypted with the server's public key": (
                False,
                "Public-key encryption is only used during the handshake, to agree on a key. "
                "Encrypting 20 MB with it would be far too slow.",
            ),
            "Symmetric: it's encrypted with the session key": (
                True,
                "The handshake uses public-key crypto to agree on a session key, and then "
                "a fast symmetric cipher such as AES-GCM encrypts the data itself.",
            ),
            "Neither: HTTPS only proves who the server is": (
                False,
                "HTTPS does authenticate the server, but it also encrypts everything sent "
                "after the handshake.",
            ),
        },
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md('## Wtf is "post quantum cryptography"'),
            mo.accordion(
                {
                    "Optional: read if you have time": mo.md(r"""
    - **Post-quantum cryptography (PQC) is not the same thing as quantum cryptography.**
      - *Post-quantum cryptography* runs on ordinary computers but is built on math problems we believe even a quantum computer can't solve efficiently.
      - *Quantum cryptography* uses quantum physics itself to protect information. The best-known example is quantum key distribution (QKD), which needs special hardware.
    - Why it's needed: Shor's algorithm, on a large enough fault-tolerant quantum computer, would factor large numbers and solve elliptic-curve discrete logs efficiently. That breaks RSA and elliptic curve cryptography, including Bitcoin's signatures.
      - Symmetric ciphers and hashes are in much better shape. Against them the best quantum attack, Grover's algorithm, only takes a square root: SHA-256's pre-image security drops from about 256 bits to about 128, still far out of reach.
    - So PQC swaps in new trapdoors. In August 2024 NIST published its first three post-quantum standards:

    | Standard | Name | Job | Based on |
    | :--- | :--- | :--- | :--- |
    | FIPS 203 | ML-KEM (formerly CRYSTALS-Kyber) | Key establishment | Module lattices (Module-LWE) |
    | FIPS 204 | ML-DSA (formerly CRYSTALS-Dilithium) | Signatures | Module lattices (Module-LWE and Module-SIS) |
    | FIPS 205 | SLH-DSA (formerly SPHINCS+) | Signatures | Hash functions only |

    - Lattice schemes rest on "learning with errors": the secret hides in linear equations with a little noise added. Without the noise, Gaussian elimination solves them instantly; with it, no known algorithm does much better than an enormous search.
    - In March 2025 NIST picked **HQC**, a code-based backup to ML-KEM. As of October 2026 its standard, and a FALCON-based signature standard (FN-DSA), were still being written.
    - NIST's transition plan (NIST IR 8547, final version October 27, 2026) deprecates quantum-vulnerable public-key algorithms such as RSA, ECDSA and elliptic-curve Diffie–Hellman after 2030, and disallows them under NIST standards after 2035.
    - Nobody has a quantum computer that can break real keys today, but the estimated size of the machine keeps shrinking. In May 2025 Craig Gidney estimated that 2048-bit RSA could be factored in under a week with fewer than one million noisy qubits (down from 20 million in 2019), and a February 2026 preprint claims under 100,000, each under specific hardware assumptions.
    """)
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md('## Wtf is "fully homomorphic encryption" (FHE)'),
            mo.accordion(
                {
                    "Optional: read if you have time": mo.md(r"""
    - Today, a server that works on your data (say, a hospital's records) has to decrypt it first. **Fully homomorphic encryption** lets it compute on the encrypted data directly.
      - You send encrypted numbers, the server adds and multiplies the ciphertexts, and when you decrypt the result you get the answer as if it had worked on the plaintext:

    $$\text{Dec}\big(\text{Enc}(a) \oplus \text{Enc}(b)\big) = a + b \qquad \text{Dec}\big(\text{Enc}(a) \otimes \text{Enc}(b)\big) = a \times b$$

    ($\oplus$ and $\otimes$ are operations on ciphertexts; encryption is randomized, so the results only *decrypt* to the same thing.)

    - Some older schemes are *partially* homomorphic. Textbook RSA, coming up below, lets you multiply ciphertexts but not add them. FHE does both, which is enough to compute any function. Craig Gentry built the first FHE scheme in 2009.
    - Why people care (one example of each is enough):
      - Outside crypto: a hospital analysing patient records it can't see, or banks pooling fraud data without exposing customers.
      - In blockchains: confidential smart contracts, and trading on encrypted orders that front-running bots can't read (front-running is Week 6).
    - FHE is still orders of magnitude slower than computing on plaintext.
    """)
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, sha256_hex):
    _hello = sha256_hex(b"Hello!")
    _hello2 = sha256_hex(b"Hello?")
    mo.vstack(
        [
            mo.md(rf"""
    ## Hash Functions

    - You download a 4 GB file. How do you know nobody changed it on the way?
      - Comparing it byte by byte would need a trusted 4 GB copy, which is exactly what you don't have.
      - So the publisher posts a 64-character fingerprint instead, and you check that the fingerprint of your download matches.
    - A **hash function** $H(x)$ makes that fingerprint. It takes an input of any length (a word, a file, a block of transactions) and produces a fixed-length output called a *hash* or *digest*.
      - SHA-256 always outputs 256 bits, written as 64 hex characters. Bitcoin links its blocks and runs its mining on this function.

    ```
    SHA-256("Hello!") = {_hello}
    SHA-256("Hello?") = {_hello2}
    ```

    One changed character gives a digest that looks unrelated.
    - A *cryptographic* hash function also promises four properties:
      - **Deterministic:** the same input always gives the same output.
      - **Pre-image resistance:** given a hash $h$, it's infeasible to find any input $m$ with $H(m) = h$.
      - **Second pre-image resistance:** given an input $m$, it's infeasible to find a *different* input $n$ with $H(n) = H(m)$. This is what makes the download check work.
      - **Collision resistance:** it's infeasible to find *any* two different inputs with the same hash.
        - This is the strongest of the three resistance properties, because you get to pick both inputs freely and it still has to be hard.
    - **What does this mean?** If all you have is a hash, you can't find the message behind it without trying messages one by one. And if someone else has a message, you can't find a different one with the same hash.
    """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    **A practical example: storing passwords.** Say you're building a website with sign-ups.

    - **Bad:** store each password as-is. Whoever steals the database has every password.
    - **Better, but still weak:** store `hash(password + secret_constant)`. A stolen database now shows random-looking strings, but SHA-256 is built to be fast, so one GPU can test billions of guesses per second. And with one shared constant, two users with the same password get the same stored value.
    - **Best:** give every user their own random *salt* and use a deliberately slow password-hashing function such as Argon2id, scrypt or bcrypt, as OWASP recommends. Identical passwords then produce different stored values, and each guess is expensive. Libraries such as `argon2-cffi` choose the salt and parameters for you.

    **Some well-known hash functions**

    - **MD5 (1992).** Same idea as SHA-256 with a shorter, 128-bit output, and broken: don't use it.
      - Practical collisions were published in 2004, and today two files with the same MD5 can be made on a laptop.
      - Unsalted MD5 password databases also fall to *rainbow tables*, huge precomputed lists of hash and password pairs.
    - **SHA-2 (SHA-256, SHA-512; 2002).** Unbroken and fast. The NSA designed it and NIST published it (today's version is FIPS 180-4).
      - Bitcoin uses SHA-256 throughout. If you need a hash in your own code, use SHA-256.
    - **SHA-3 (2015).** Same job as SHA-2, a completely different inside, and slower in software.
      - It came out of a public NIST competition (the Keccak algorithm). Ethereum uses Keccak-256, a near-twin of SHA3-256.
    - **Poseidon.** Same job, built for zero-knowledge proofs.
      - SHA-2 and SHA-3 are built from bitwise operations (AND, XOR, rotations), which are expensive inside a ZK proof. Poseidon uses arithmetic over a finite field, which is cheap there. More in a later week.

    Quantum computers barely dent SHA-2 or SHA-3 (see the post-quantum section).
    """),
            mo.accordion(
                {
                    "Didn't the NSA backdoor something?": mo.md(
                        "Yes, but not SHA-2: the backdoor story is about a different NSA design, the Dual_EC_DRBG random "
                        "number generator (Cloudflare's write-up is in Further reading below). NIST told people to stop "
                        "using it in 2013 and dropped it from its standard in 2015."
                    )
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            mo.md(r"""
    **How do hash functions work?** Simplified, using SHA-256, which follows the Merkle–Damgård design:

    1. **Padding.** Convert the input to bits. Append a single `1` bit, then `0` bits until the length is 64 bits short of a multiple of 512, then append the original length as a 64-bit number. The padded message is now a whole number of 512-bit blocks.
    2. **Initial value.** Start from eight fixed 32-bit words (from the square roots of the first eight primes, so nobody could hide anything in them).
    3. **Compression.** Feed the blocks in one at a time. A compression function mixes each block into the running state over 64 rounds of additions, rotations and bitwise operations.
    4. **Output.** After the last block, the state *is* the 256-bit hash.

    The rounds mix so thoroughly that flipping one input bit flips about half the output bits. SHA-3 does the same job with a different structure, a "sponge".
    """),
            mo.mermaid(
                """
    graph LR
        M[Message] --> P[Pad to 512-bit blocks]
        P --> B1[Block 1]
        P --> B2[Block 2]
        P --> Bn[Block n]
        IV[Fixed initial value] --> C1((compress))
        B1 --> C1
        C1 --> C2((compress))
        B2 --> C2
        C2 --> Cn((compress))
        Bn --> Cn
        Cn --> H[256-bit hash]
    """
            ),
            further_reading(
                [
                    ("Cryptographic hash function (Wikipedia)", "https://en.wikipedia.org/wiki/Cryptographic_hash_function", "overview of the properties"),
                    ("FIPS 180-4: Secure Hash Standard", "https://csrc.nist.gov/pubs/fips/180-4/upd1/final", "the SHA-2 specification"),
                    ("FIPS 202: SHA-3 Standard", "https://csrc.nist.gov/pubs/fips/202/final", ""),
                    ("SHA-256 step by step (boot.dev)", "https://blog.boot.dev/cryptography/how-sha-2-works-step-by-step-sha-256/", "walks through every round"),
                    ("OWASP Password Storage Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html", "current guidance on salts and slow hashes"),
                    ("How the NSA (may have) put a backdoor in RSA's cryptography (Cloudflare)", "https://blog.cloudflare.com/how-the-nsa-may-have-put-a-backdoor-in-rsas-cryptography-a-technical-primer/", "the Dual_EC_DRBG story"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    hash_algo = mo.ui.dropdown(
        ["SHA-256", "SHA3-256", "MD5"], value="SHA-256", label="Hash"
    )
    hash_msg_a = mo.ui.text(value="Hello!", label="Message A", full_width=True)
    hash_msg_b = mo.ui.text(value="Hello?", label="Message B", full_width=True)
    coll_guess = mo.ui.radio(
        options=["About 4 billion (2³²)", "About 80,000", "About 32"],
        label="Guess before you run it: with a 32-bit hash, about how many random inputs do you hash before two of them collide?",
    )
    coll_bits = mo.ui.slider(8, 32, value=24, step=2, label="Hash size (bits)", show_value=True, debounce=True)
    coll_runs = mo.ui.slider(1, 20, value=8, label="Number of hunts", show_value=True, debounce=True)
    coll_go = mo.ui.run_button(label="Start hunting")
    return coll_bits, coll_go, coll_guess, coll_runs, hash_algo, hash_msg_a, hash_msg_b


@app.cell(hide_code=True)
def _(alt, hash_algo, hash_msg_a, hash_msg_b, hashlib, mo, pd):
    _fn = {"SHA-256": hashlib.sha256, "SHA3-256": hashlib.sha3_256, "MD5": hashlib.md5}[
        hash_algo.value
    ]
    _ha = _fn(hash_msg_a.value.encode()).hexdigest()
    _hb = _fn(hash_msg_b.value.encode()).hexdigest()
    _nbits = len(_ha) * 4
    _ba = bin(int(_ha, 16))[2:].zfill(_nbits)
    _bb = bin(int(_hb, 16))[2:].zfill(_nbits)
    _flipped = sum(x != y for x, y in zip(_ba, _bb))
    _cols = 16
    _grid = pd.DataFrame(
        {
            "bit": range(_nbits),
            "row": [i // _cols for i in range(_nbits)],
            "col": [i % _cols for i in range(_nbits)],
            "state": ["different" if x != y else "same" for x, y in zip(_ba, _bb)],
        }
    )
    _chart = (
        alt.Chart(_grid)
        .mark_rect(stroke="white", strokeWidth=1)
        .encode(
            x=alt.X("col:O", axis=None),
            y=alt.Y("row:O", axis=None),
            color=alt.Color(
                "state:N",
                scale=alt.Scale(domain=["same", "different"], range=["#d9d9d9", "#e45756"]),
                legend=alt.Legend(title="Bit in digest A vs B", orient="top"),
            ),
            tooltip=["bit", "state"],
        )
        .properties(width=16 * 22, height=(_nbits // _cols) * 22)
    )
    _char_diff = sum(x != y for x, y in zip(hash_msg_a.value, hash_msg_b.value)) + abs(
        len(hash_msg_a.value) - len(hash_msg_b.value)
    )
    _pct = 100 * _flipped / _nbits
    if hash_msg_a.value == hash_msg_b.value:
        _msg = "The messages are identical, so the digests are identical: hash functions are deterministic."
    else:
        _msg = (
            f"The messages differ in {_char_diff} character{'s' if _char_diff != 1 else ''}. "
            f"Their {hash_algo.value} digests differ in **{_flipped} of {_nbits} bits ({_pct:.0f}%)**. "
            "For a good hash this stays near 50% however small the change. That's the *avalanche effect*, and it "
            "means two similar inputs give you no hint about each other's hashes."
        )
    avalanche_view = mo.vstack(
        [
            mo.md(
                "A and B differ by one character. How many of the 256 output bits will differ: a handful, about half, "
                "or nearly all? Each square is one bit; red means it differs. Then try other small edits or another "
                "hash function."
            ),
            mo.hstack([hash_msg_a, hash_msg_b, hash_algo], widths=[2, 2, 1], align="end", wrap=True),
            mo.md(f"A: `{_ha}`  \nB: `{_hb}`"),
            _chart,
            mo.md(_msg),
        ]
    )
    return (avalanche_view,)


@app.cell(hide_code=True)
def _(coll_bits, coll_go, coll_runs, hashlib, random):
    def collision_hunt(bits, seed):
        """Hash "seed:i" for i = 0, 1, 2, ... keeping only the first `bits` bits
        of SHA-256, until two inputs give the same truncated value."""
        seen = {}
        shift = 64 - bits
        i = 0
        while True:
            v = int.from_bytes(hashlib.sha256(f"{seed}:{i}".encode()).digest()[:8], "big") >> shift
            if v in seen:
                return {"tries": i + 1, "first": f"{seed}:{seen[v]}", "second": f"{seed}:{i}", "value": v}
            seen[v] = i
            i += 1

    coll_results = None
    if coll_go.value:
        coll_results = {
            "bits": coll_bits.value,
            "hunts": [collision_hunt(coll_bits.value, random.randrange(10**9)) for _ in range(coll_runs.value)],
        }
    return coll_results, collision_hunt


@app.cell(hide_code=True)
def _(alt, coll_bits, coll_go, coll_guess, coll_results, coll_runs, math, mo, pd, quiz_feedback):
    _guess_fb = quiz_feedback(
        coll_guess.value,
        {
            "About 4 billion (2³²)": (
                False,
                "That's how many tries it takes to match one *specific* hash (a pre-image). A collision "
                "between *any* two of your inputs comes much sooner, for the same reason that 23 people "
                "are enough for a 50% chance of a shared birthday. Run the hunt at 32 bits and see.",
            ),
            "About 80,000": (
                True,
                r"Roughly $\sqrt{\pi/2 \cdot 2^{32}} \approx 82{,}000$."
                " Every new input can collide with *every* earlier one, so "
                "the chance builds up fast. This is the birthday bound: an n-bit hash gives only about n/2 bits "
                "of collision resistance.",
            ),
            "About 32": (
                False,
                "32 is the number of output bits, and there are $2^{32}$ possible outputs. You'd need far more "
                "than 32 inputs before two of them land on the same one. Run the hunt and see.",
            ),
        },
    )
    if coll_results is None:
        _out = mo.md("*Press **Start hunting** to run the experiment.*")
    else:
        _bits = coll_results["bits"]
        _df = pd.DataFrame(
            [{"hunt": i + 1, "tries": h["tries"]} for i, h in enumerate(coll_results["hunts"])]
        )
        _est = math.sqrt(math.pi / 2 * 2**_bits)
        _bars = (
            alt.Chart(_df)
            .mark_bar(color="#4c78a8")
            .encode(
                x=alt.X("hunt:O", title="Hunt"),
                y=alt.Y("tries:Q", title="Hashes until first collision"),
                tooltip=["hunt", "tries"],
            )
        )
        _rule = (
            alt.Chart(pd.DataFrame({"y": [_est]}))
            .mark_rule(color="#e45756", strokeDash=[6, 4], size=2)
            .encode(y="y:Q")
        )
        _chart = (_bars + _rule).properties(
            height=220, width="container", title=f"{_bits}-bit hash: red line is the birthday estimate"
        )
        _avg = _df["tries"].mean()
        _ex = coll_results["hunts"][0]
        _out = mo.vstack(
            [
                _chart,
                mo.md(
                    f"Average: **{_avg:,.0f}** hashes. Birthday estimate $\\sqrt{{\\pi/2 \\cdot 2^{{{_bits}}}}}$ ≈ **{_est:,.0f}**. "
                    f"Matching one specific {_bits}-bit hash would take about $2^{{{_bits}}}$ ≈ **{2**_bits:,}** tries instead.  \n"
                    f"Example from hunt 1: `{_ex['first']}` and `{_ex['second']}` both truncate to the value {_ex['value']:,}.\n\n"
                    "Each extra 2 bits of output roughly doubles the work. SHA-256 has 256 bits, so a generic collision "
                    "search needs about $2^{128}$ hashes; at a billion billion ($10^{18}$) hashes per second that's around "
                    "$10^{13}$ years."
                ),
            ]
        )
    collision_view = mo.vstack(
        [
            mo.md(
                "No real SHA-256 collision has ever been found, so this cuts SHA-256 down to its first few bits and "
                "hashes `seed:0`, `seed:1`, … until two inputs share a value."
            ),
            coll_guess,
            _guess_fb,
            mo.hstack([coll_bits, coll_runs, coll_go], align="center", wrap=True),
            _out,
        ]
    )
    return (collision_view,)


@app.cell(hide_code=True)
def _(avalanche_view, collision_view, experience, mo):
    experience(
        "Hash lab",
        mo.ui.tabs({"1. Avalanche": avalanche_view, "2. Collision hunt": collision_view}),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Examples of Asymmetric encryption

    ## Asymmetric Encryption: Textbook RSA (Rivest-Shamir-Adleman)

    RSA was published in 1977 by Ron Rivest, Adi Shamir and Leonard Adleman. If you take CS70 at Berkeley, it's covered in the RSA note (Note 7); this section is a self-contained version.

    ### Some preliminary info that is relevant to most cryptographic concepts:

    - **Trapdoor functions**
      - Public-key encryption needs an operation anyone can do with the public key but only the private key can undo.
      - A trapdoor function is easy to compute in one direction and hard to reverse, *unless* you know a secret (the trapdoor) that makes reversing easy.
      - Multiplication and factoring give the classic example:

    > **A:** What two numbers multiply to 424,253?<br>
    > **B:** No idea. I'd have to try every possible pair.<br>
    > **A:** One of them is 743.<br>
    > **B:** Oh, then it's easy: 424,253 ÷ 743 = 571.

    Multiplying 743 × 571 takes a second; going backwards from 424,253 means searching, and for a number with 600 digits nobody knows how to do that search in any reasonable time. RSA turns this into a trapdoor: the two primes are the secret that makes decryption easy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_trapdoor = mo.ui.radio(
        options=[
            "They aren't hard to reverse",
            "There's no secret that makes reversing them easy",
            "Their output length is fixed",
        ],
        label="Pop quiz: hash functions are easy to compute and hard to reverse. Why aren't they trapdoor functions?",
    )
    quiz_trapdoor
    return (quiz_trapdoor,)


@app.cell(hide_code=True)
def _(quiz_feedback, quiz_trapdoor):
    quiz_feedback(
        quiz_trapdoor.value,
        {
            "They aren't hard to reverse": (
                False,
                "They are hard to reverse; that's pre-image resistance. The missing piece is something else.",
            ),
            "There's no secret that makes reversing them easy": (
                True,
                "A trapdoor function has a secret that unlocks the reverse direction. A hash function has no "
                "such secret: reversing it is hard for everyone, including whoever designed it.",
            ),
            "Their output length is fixed": (
                False,
                "Fixed output length is a property of hash functions, but it isn't what disqualifies them. "
                "Think about who, if anyone, can reverse one easily.",
            ),
        },
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            mo.md(r"""
    ### RSA

    - RSA is an asymmetric (public-key) algorithm. Every user has a public key, which they share widely, and a private key, which they never tell anyone.
      - In effect each user announces, "Hey world, anyone can reach me with my public key, but I am never, ever telling you my private key."
      - **Encryption:** Alice wants to send Bob a message, so she encrypts it with *Bob's public key*.
      - **Decryption:** Bob decrypts it with *Bob's private key*.
    - The private key comes from two large primes $p$ and $q$, and the public key includes their product $N = pq$.
      - As far as anyone knows, getting the private key from the public key requires factoring $N$.

    **The procedure**, with small numbers you can check by hand (the experiment below starts with the same ones):

    1. Pick two large primes $p$ and $q$ and compute $N = pq$.
      - $p = 61$, $q = 53$, so $N = 3233$.
    2. Choose $e$ with $\gcd\big(e, (p-1)(q-1)\big) = 1$. Two numbers are *relatively prime* when their greatest common divisor is 1. The **public key** is $(N, e)$.
      - $(p-1)(q-1) = 60 \times 52 = 3120 = 2^4 \cdot 3 \cdot 5 \cdot 13$. $e = 17$ shares no factor with it, so the public key is $(3233, 17)$.
    3. Compute $d$, the multiplicative inverse of $e$ modulo $(p-1)(q-1)$, so that $ed \equiv 1 \pmod{(p-1)(q-1)}$. The **private key** is $d$.
      - $d = 2753$, because $17 \times 2753 = 46801 = 15 \times 3120 + 1$.
    4. To **encrypt** a message $m$ (written as a number smaller than $N$): $c = m^e \bmod N$.
      - $m = 65$ gives $c = 65^{17} \bmod 3233 = 2790$.
    5. To **decrypt**: $m = c^d \bmod N$.
      - $2790^{2753} \bmod 3233 = 65$, the message again.

    - Knowing $p$ and $q$ is the trapdoor: with them, computing $d$ takes a few steps of the extended Euclidean algorithm. Without them, nobody knows a fast way.
    - To picture "mod", think of a 12-hour clock: 10:00 plus 4 hours is 2:00, not 14:00. Arithmetic mod $N$ wraps around at $N$ the same way, and RSA works because raising to the $e$ and then to the $d$ wraps all the way back to where you started.
    - Don't use textbook RSA as written. The experiment below shows both of its problems:
      - It's deterministic: the same message always gives the same ciphertext.
      - It's malleable: an attacker can turn a ciphertext into the encryption of a related message without decrypting it.
      - Real systems add randomized padding, OAEP for encryption and PSS for signatures.
    - A large enough quantum computer would factor $N$ efficiently; the post-quantum section covers how close that is.
    """),
            mo.accordion(
                {
                    "[Not tested] When textbook RSA protected hundreds of millions of users": mo.md(
                        "In 2018 researchers showed that Tencent's QQ Browser, with hundreds of millions of users, "
                        "encrypted its session key with textbook RSA. Because textbook RSA is malleable, an attacker "
                        "could recover that key a bit at a time. The paper is in Further reading."
                    ),
                    "Why decryption works (proof)": mo.md(r"""
    Since $ed \equiv 1 \pmod{(p-1)(q-1)}$, there's some integer $k$ with $ed = k(p-1)(q-1) + 1$. So

    $$c^d \equiv m^{ed} = m \cdot \left(m^{p-1}\right)^{k(q-1)} \pmod{N}.$$

    Work mod $p$ first. If $p$ doesn't divide $m$, **Fermat's little theorem** says $m^{p-1} \equiv 1 \pmod p$, so $m^{ed} \equiv m \pmod p$. If $p$ does divide $m$, both sides are $0 \bmod p$, so $m^{ed} \equiv m \pmod p$ still holds. The same argument with the roles swapped gives $m^{ed} \equiv m \pmod q$.

    Since $p$ and $q$ are different primes, the Chinese remainder theorem combines the two: $m^{ed} \equiv m \pmod{N}$. Because $m < N$, decryption returns exactly $m$.
    """)
                }
            ),
            further_reading(
                [
                    ("CS70 Note 7: Public Key Cryptography (RSA)", "https://www.eecs70.org/assets/pdf/notes/n7.pdf", "Berkeley's treatment, with full proofs"),
                    ("RSA Encryption (Brilliant)", "https://brilliant.org/wiki/rsa-encryption/", "worked examples"),
                    ("When Textbook RSA is Used to Protect the Privacy of Hundreds of Millions of Users", "https://arxiv.org/abs/1802.03367", "the QQ Browser attack (2018)"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    SMALL_PRIMES = [
        11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199,
    ]
    rsa_p = mo.ui.dropdown([str(x) for x in SMALL_PRIMES], value="61", label="Prime p")
    rsa_q = mo.ui.dropdown([str(x) for x in SMALL_PRIMES], value="53", label="Prime q")
    return rsa_p, rsa_q


@app.cell(hide_code=True)
def _(math, mo, rsa_p, rsa_q):
    rsa_P, rsa_Q = int(rsa_p.value), int(rsa_q.value)
    rsa_N = rsa_P * rsa_Q
    rsa_phi = (rsa_P - 1) * (rsa_Q - 1)
    _choices = [e for e in range(3, min(rsa_phi, 400)) if math.gcd(e, rsa_phi) == 1][:40]
    rsa_e = mo.ui.dropdown(
        [str(e) for e in _choices],
        value="17" if 17 in _choices else str(_choices[0]),
        label="Public exponent e",
    )
    return rsa_N, rsa_P, rsa_Q, rsa_e, rsa_phi


@app.cell(hide_code=True)
def _(mo, rsa_N):
    rsa_m = mo.ui.number(
        start=0, stop=rsa_N - 1, value=min(65, rsa_N - 1), label=f"Message m (0 to {rsa_N - 1})"
    )
    return (rsa_m,)


@app.cell(hide_code=True)
def _(rsa_e, rsa_phi):
    def egcd_steps(phi, e):
        """Extended Euclid on (phi, e), tracking the coefficient of e.
        Returns the table of steps and the inverse of e mod phi."""
        rows = []
        r0, r1 = phi, e
        t0, t1 = 0, 1
        while r1 != 0:
            qt = r0 // r1
            rows.append({"r": r0, "next r": r1, "quotient": qt, "t": t0, "next t": t1})
            r0, r1 = r1, r0 - qt * r1
            t0, t1 = t1, t0 - qt * t1
        return rows, t0 % phi

    rsa_E = int(rsa_e.value)
    rsa_steps, rsa_D = egcd_steps(rsa_phi, rsa_E)
    return egcd_steps, rsa_D, rsa_E, rsa_steps


@app.cell(hide_code=True)
def _(
    experience,
    mo,
    rsa_D,
    rsa_E,
    rsa_N,
    rsa_P,
    rsa_Q,
    rsa_e,
    rsa_m,
    rsa_p,
    rsa_phi,
    rsa_q,
    rsa_steps,
):
    if rsa_P == rsa_Q:
        _body = mo.callout(mo.md("Pick two **different** primes. If p = q, then N = p² and anyone can take its square root."), kind="danger")
    else:
        _m = int(rsa_m.value)
        _c = pow(_m, rsa_E, rsa_N)
        _back = pow(_c, rsa_D, rsa_N)
        _c_times2 = (_c * pow(2, rsa_E, rsa_N)) % rsa_N
        _forged = pow(_c_times2, rsa_D, rsa_N)
        _k = (rsa_E * rsa_D - 1) // rsa_phi
        _body = mo.vstack(
            [
                mo.md(rf"""
    **Key generation with your numbers**

    $$N = p \times q = {rsa_P} \times {rsa_Q} = {rsa_N}$$

    $$(p-1)(q-1) = {rsa_P - 1} \times {rsa_Q - 1} = {rsa_phi}, \qquad \gcd({rsa_E}, {rsa_phi}) = 1$$

    $$d = e^{{-1}} \bmod {rsa_phi} = {rsa_D} \quad\text{{because}}\quad {rsa_E} \times {rsa_D} = {rsa_E * rsa_D} = {_k} \times {rsa_phi} + 1$$

    Public key: $(N, e) = ({rsa_N}, {rsa_E})$. Private key: $d = {rsa_D}$.
    """),
                mo.accordion(
                    {
                        "How d was found: the extended Euclidean algorithm": mo.vstack(
                            [
                                mo.md(
                                    "Each row divides the larger number by the smaller (r = quotient × next r + remainder) "
                                    "while tracking a coefficient t. When the remainder reaches 1, t is the inverse of e "
                                    f"(taken mod {rsa_phi})."
                                ),
                                mo.ui.table(rsa_steps, selection=None, pagination=False),
                            ]
                        )
                    }
                ),
                rsa_m,
                mo.md(rf"""
    **Encrypt** with the public key: $c = {_m}^{{{rsa_E}}} \bmod {rsa_N} = {_c}$

    **Decrypt** with the private key: $c^d = {_c}^{{{rsa_D}}} \bmod {rsa_N} = {_back}$ {"✓" if _back == _m else "✗"}
    """),
                mo.callout(
                    mo.md(
                        f"**Problem 1: it's deterministic.** Encrypt {_m} again and you get {_c} again, so an eavesdropper "
                        "can encrypt each likely message (\"yes\", \"no\") and compare.  \n"
                        f"**Problem 2: it's malleable.** Without decrypting anything, Mallory multiplies the ciphertext by "
                        f"$2^e \\bmod N$: ${_c} \\times 2^{{{rsa_E}}} \\bmod {rsa_N} = {_c_times2}$. When Bob decrypts that, he gets **{_forged}**, "
                        f"which is 2 × {_m} mod {rsa_N}: a changed message she never read. Randomized padding (OAEP) stops both."
                    ),
                    kind="warn",
                ),
            ]
        )
    experience(
        "RSA by hand",
        mo.md(
            "Pick two primes and an exponent; everything recomputes. If you encrypt the same message twice, will "
            "the ciphertexts match? The orange box answers."
        ),
        mo.hstack([rsa_p, rsa_q, rsa_e], justify="start", gap=2, wrap=True),
        _body,
    )
    return


@app.cell(hide_code=True)
def _(random):
    def is_probable_prime(n):
        if n < 2:
            return False
        for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n % sp == 0:
                return n == sp
        d, s = n - 1, 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def random_prime(bits, rng):
        while True:
            c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
            if is_probable_prime(c):
                return c

    def trial_division(n):
        """Return (smallest factor, number of candidate divisors tried)."""
        if n % 2 == 0:
            return 2, 1
        f, steps = 3, 1
        while f * f <= n:
            if n % f == 0:
                return f, steps
            f += 2
            steps += 1
        return n, steps

    _rng = random.Random(2026)
    factoring_samples = []
    for _bits in range(16, 41, 4):
        for _ in range(3):
            _a = random_prime(_bits // 2, _rng)
            _b = random_prime(_bits // 2, _rng)
            _f, _steps = trial_division(_a * _b)
            factoring_samples.append({"N size (bits)": (_a * _b).bit_length(), "divisions tried": _steps})
    return factoring_samples, is_probable_prime, random_prime, trial_division


@app.cell(hide_code=True)
def _(alt, experience, factoring_samples, mo, pd, rsa_E, rsa_N, rsa_P, rsa_Q, rsa_phi, trial_division):
    _df = pd.DataFrame(factoring_samples)
    _chart = (
        alt.Chart(_df)
        .mark_circle(size=70, color="#4c78a8")
        .encode(
            x=alt.X("N size (bits):Q", scale=alt.Scale(domain=[14, 42])),
            y=alt.Y("divisions tried:Q", scale=alt.Scale(type="log"), title="Divisions tried (log scale)"),
            tooltip=["N size (bits)", "divisions tried"],
        )
        .properties(height=220, width="container", title="Factoring by trial division: random N = p × q")
    )
    if rsa_P != rsa_Q:
        _f, _steps = trial_division(rsa_N)
        _other = rsa_N // _f
        _d = pow(rsa_E, -1, rsa_phi)
        _mallory = (
            f"Mallory factors your N = {rsa_N} in **{_steps} division{'s' if _steps != 1 else ''}**: "
            f"{rsa_N} = {_f} × {_other}, which gives her (p−1)(q−1) = {rsa_phi} and your private key d = {_d}."
        )
    else:
        _mallory = ""
    experience(
        "Factor N like an attacker",
        mo.md(
            "Trial division, the simplest attack, tries every odd number up to √N. Each dot is a real run on a random "
            "N = p × q of that size, on a log scale. How much does the work grow per 4 extra bits, and what does that "
            "mean for a 2048-bit N?"
        ),
        _chart,
        mo.md(
            _mallory
            + "\n\nEvery 4 extra bits multiply the work by about 4, so a 2048-bit N would need about "
            "$2^{1023} \\approx 10^{308}$ divisions. The general number field sieve is enormously faster, yet the "
            "largest RSA challenge number factored in public (as of November 2026) is RSA-896, in September 2026 "
            "on up to 2,048 GPUs over about 10 days: less than half the length of a 2048-bit key."
        ),
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            mo.md(r"""
    ## Digital Signatures

    - **Motivation**
      - Alice wants to send Bob a message. Problem #1: anyone on the way can read it.
        - Fix #1: encrypt it with Bob's public key. Now only Bob can read it.
      - Is that it? Not quite. Problem #2: Mallory can encrypt "This is Alice. Send $100 to @mallory" just as easily, and Bob can't tell who sent it.
        - Fix #2: Alice also **signs** the message with *her own* private key, and anyone with her public key can check it.
          - Only Alice could have produced a valid signature, and it covers the exact message, so it proves both who sent it and that nobody changed it.
      - Every Bitcoin transaction is a signed message saying "move these coins".
    - **The math for RSA.** Signing uses RSA's $d$ and $e$ the other way round, on a *hash* of the message:
      - Alice sends $m$ together with $S = H(m)^{d_A} \bmod N_A$.
      - Bob computes $S^{e_A} \bmod N_A$ and checks that it equals $H(m) \bmod N_A$.
        - This works for the same reason decryption does: $(H(m)^{d})^{e} \equiv H(m) \pmod N$.
      - Check it with the key from RSA ($N = 3233$, $e = 17$, $d = 2753$) and the message "Pay Bob 5 dollars", which the experiment below starts with:
        - $H(m) = 1458$ (SHA-256, reduced mod 3233), so $S = 1458^{2753} \bmod 3233 = 697$.
        - Bob computes $697^{17} \bmod 3233 = 1458$. It matches, so the signature is valid.
      - Hashing first keeps the signature one small number, however long the message is.
      - You'll sometimes hear signing described as "encrypting with your private key". That's only accurate for textbook RSA, and it doesn't describe ECDSA or Schnorr signatures at all.
    - **Signing *and* encrypting.** To keep a message secret and prove who sent it, Alice encrypts the message for Bob and sends her signature on its hash alongside.
      - Encrypting twice with RSA would be slow, so in practice the encryption is a key exchange plus a symmetric cipher, as in the HTTPS example.
    - Elliptic-curve signatures (ECDSA) are the most widely used today, by Bitcoin since 2009 and by Ethereum. Since the Taproot upgrade (November 2021) Bitcoin also supports **Schnorr signatures** (BIP 340), which let several signers combine into one signature.
    """),
            mo.mermaid(
                """
    graph TD
        M1["Alice: message m"] --> H1["Alice: hash it, H(m)"]
        H1 --> S1["Alice: sign H(m) with her private key, giving S"]
        S1 -->|"sends m and S"| V["Bob: check S with Alice's public key"]
        V --> R{"Does it match H(m)?"}
        R -->|yes| OK["Accept: from Alice, unaltered"]
        R -->|no| BAD["Reject"]
    """
            ),
            further_reading(
                [
                    ("RSA Signatures (Practical Cryptography for Developers)", "https://cryptobook.nakov.com/digital-signatures/rsa-signatures", ""),
                    ("BIP 340: Schnorr Signatures for secp256k1", "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki", "the spec Bitcoin uses"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    sig_msg = mo.ui.text(value="Pay Bob 5 dollars", label="Alice's message", full_width=True)
    sig_tamper = mo.ui.switch(label="Mallory edits the message in transit")
    sig_forge = mo.ui.run_button(label="Let Mallory search for a forgery")
    return sig_forge, sig_msg, sig_tamper


@app.cell(hide_code=True)
def _(
    experience,
    hashlib,
    mo,
    rsa_D,
    rsa_E,
    rsa_N,
    rsa_P,
    rsa_Q,
    sig_forge,
    sig_msg,
    sig_tamper,
):
    import re as sig_re

    def toy_hash(text, n):
        """SHA-256 of the text, reduced mod n so it fits our toy key."""
        return int(hashlib.sha256(text.encode()).hexdigest(), 16) % n

    def tamper(text):
        m = sig_re.search(r"\d+", text)
        if m:
            return text[: m.end()] + "00" + text[m.end():]
        return text + " and 100 dollars"

    if rsa_P == rsa_Q:
        _out = mo.md("*Fix the key above (p and q must differ) to use this experiment.*")
    else:
        _h = toy_hash(sig_msg.value, rsa_N)
        _S = pow(_h, rsa_D, rsa_N)
        _received = tamper(sig_msg.value) if sig_tamper.value else sig_msg.value
        _h_recv = toy_hash(_received, rsa_N)
        _check = pow(_S, rsa_E, rsa_N)
        _valid = _check == _h_recv
        _verdict = (
            mo.callout(mo.md(f"**Valid.** {_check} = {_h_recv}, so Bob accepts the message as Alice's."), kind="success")
            if _valid
            else mo.callout(mo.md(f"**Invalid.** {_check} ≠ {_h_recv}. One changed character changed the hash, so Alice's signature no longer fits, and Mallory can't make a new one without Alice's private key. Bob rejects the message."), kind="danger")
        )
        _forge_out = mo.md("")
        if sig_forge.value:
            _target = "Pay Mallory 1000 dollars"
            _tries = 0
            while True:
                _cand = f"{_target} #{_tries}"
                _tries += 1
                if toy_hash(_cand, rsa_N) == _h:
                    break
            _forge_out = mo.callout(
                mo.md(
                    f"Mallory tried **{_tries:,}** variations and found `{_cand}`, whose toy hash mod {rsa_N} equals "
                    f"{_h}, the same as Alice's message, so Alice's signature S = {_S} is valid on it too. Reduced mod "
                    f"N, the toy hash has only {rsa_N:,} possible values, so on average a match turns up after about "
                    f"{rsa_N:,} tries. A real signature uses a 2048-bit key and a full 256-bit hash, and the same search "
                    "would need around $2^{256}$ tries."
                ),
                kind="warn",
            )
        _out = mo.vstack(
            [
                mo.md(rf"""
    Using your RSA key from above: $N = {rsa_N}$, $e = {rsa_E}$, $d = {rsa_D}$.

    **Alice signs:** $H(m) = {_h}$ (SHA-256 reduced mod {rsa_N}), and $S = {_h}^{{{rsa_D}}} \bmod {rsa_N} = {_S}$

    **Bob receives:** "{_received}" with $S = {_S}$

    **Bob verifies:** $S^e \bmod N = {_S}^{{{rsa_E}}} \bmod {rsa_N} = {_check}$, and $H(\text{{received}}) = {_h_recv}$
    """),
                _verdict,
                mo.md(
                    "With a key this small, how many random messages must Mallory try before one shares Alice's toy hash?"
                ),
                sig_forge,
                _forge_out,
            ]
        )
    experience(
        "Sign, tamper, verify",
        mo.md(
            "Alice signs with the RSA key from the experiment above. Mallory turns \"5 dollars\" into \"500 dollars\" "
            "and forwards Alice's signature. Will Bob's check pass? Decide, then flip the switch."
        ),
        sig_msg,
        sig_tamper,
        _out,
    )
    return sig_re, tamper, toy_hash


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ## Elliptic Curve Cryptography (ECC)

    - ECC is a family of public-key schemes whose keys come from the geometry of an elliptic curve instead of the product of two primes.
      - It's used for key agreement (ECDH, as in HTTPS) and signatures (ECDSA, Schnorr). Bitcoin uses it only for signatures.
    - **Motivation**
      - RSA's security rests on factoring being hard, but factoring algorithms such as the number field sieve run in *sub-exponential* time, so RSA keys have to keep growing to stay ahead.
        - NIST rates 2048-bit RSA at about 112 bits of security and 3072-bit RSA at 128 bits (SP 800-57).
      - Elliptic curves give a trapdoor that scales better: the best known attacks on a well-chosen curve are fully exponential.
        - So a 256-bit curve key gives roughly the same 128-bit security as a 3072-bit RSA key, with a key 12 times shorter (256 bits against 3,072).
      - Bitcoin and most newer systems chose curves for those smaller keys.

    ### Elliptic Curves and their properties

    An elliptic curve is the set of points satisfying

    $$y^2 = x^3 + ax + b,$$

    where $4a^3 + 27b^2 \neq 0$ (this rules out curves with cusps or self-crossings).

    - The curve is symmetric around the x-axis: if $(x, y)$ is on it, so is $(x, -y)$.
    - Any coordinate on the curve is called a *point*, and two points can be **added** to give a third point on the curve.
    - **Adding points.** Take two points $A$ and $B$ and draw the line through them.
      - That line meets the curve at **exactly one** other point, $D$. Reflect $D$ across the x-axis to get $C$, and define $A + B = C$.
      - To add $A$ to itself, use the tangent line at $A$. That's how you get $2A$.
      - $B = -A$ (A reflected) gives a vertical line, which never meets the curve again. The sum is a special **point at infinity**, written $\mathcal{O}$, which acts like zero: $A + (-A) = \mathcal{O}$.
    """),
            mo.accordion(
                {
                    "Edge cases: why \"exactly one other point\" still holds": mo.md(r"""
    - **Tangent ($A = B$):** a tangent touches the curve twice at $A$, so counted with multiplicity it still meets the curve at exactly one other point.
    - **Vertical line:** it meets the curve at $A$ and $-A$ only. Counting the point at infinity as the third point keeps the rule, and makes $\mathcal{O}$ the identity: $A + \mathcal{O} = A$.
    - **A line that seems to hit only 2 points** is always one of those two cases: it's tangent at one of them, or it's vertical.
    """),
                    "The formulas, if you want to compute a sum yourself": mo.md(r"""
    For $A = (x_1, y_1)$ and $B = (x_2, y_2)$, take the slope $\lambda = \frac{y_2 - y_1}{x_2 - x_1}$, or $\lambda = \frac{3x_1^2 + a}{2y_1}$ for the tangent. Then

    $$x_3 = \lambda^2 - x_1 - x_2, \qquad y_3 = \lambda(x_1 - x_3) - y_1, \qquad A + B = (x_3, y_3).$$
    """),
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ec_a = mo.ui.slider(-4, 4, step=0.5, value=-1, label="a", show_value=True)
    ec_b = mo.ui.slider(-4, 4, step=0.5, value=1, label="b", show_value=True)
    ec_posA = mo.ui.slider(0, 1000, value=150, label="Point A: move along the curve", full_width=True)
    ec_posB = mo.ui.slider(0, 1000, value=420, label="Point B: move along the curve", full_width=True)
    ec_mirror = mo.ui.switch(label="Put B at −A (A reflected across the x-axis)")
    return ec_a, ec_b, ec_mirror, ec_posA, ec_posB


@app.cell(hide_code=True)
def _(np):
    def curve_paths(a, b, xmin=-4.0, xmax=5.0, n=3000, ymax=7.5):
        """Sample the real curve y^2 = x^3 + ax + b. Returns (path, segments):
        path is an ordered list of points to move along; segments are line pieces for plotting."""
        xs = np.linspace(xmin, xmax, n)
        rhs = xs**3 + a * xs + b
        valid = (rhs >= 0) & (rhs <= ymax**2)  # keep only the part that fits on the chart
        runs, start = [], None
        for i, v in enumerate(valid):
            if v and start is None:
                start = i
            if (not v or i == n - 1) and start is not None:
                end = i if v else i - 1
                runs.append((start, end))
                start = None
        path, segments = [], []
        for si, (s, e) in enumerate(runs):
            xr = xs[s : e + 1]
            yr = np.sqrt(np.maximum(rhs[s : e + 1], 0))
            upper = list(zip(xr, yr))
            lower = list(zip(xr[::-1], -yr[::-1]))
            path += upper + lower
            if rhs[e] > 1e-3 and (e == n - 1 or not valid[min(e + 1, n - 1)]) and rhs[min(e + 1, n - 1)] > 0:
                # open branch leaving the chart: draw the two halves separately
                segments.append((f"{si}u", upper))
                segments.append((f"{si}l", lower))
            else:  # closed oval
                segments.append((f"{si}", upper + lower + [upper[0]]))
        return path, segments

    def ec_add_real(P, Q, a, eps=1e-9):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if abs(x1 - x2) < eps and abs(y1 + y2) < eps:
            return None  # vertical line: point at infinity
        if abs(x1 - x2) < eps and abs(y1 - y2) < eps:
            if abs(y1) < eps:
                return None  # vertical tangent
            lam = (3 * x1 * x1 + a) / (2 * y1)
        else:
            lam = (y2 - y1) / (x2 - x1)
        x3 = lam * lam - x1 - x2
        y3 = lam * (x1 - x3) - y1
        return (x3, y3)

    return curve_paths, ec_add_real


@app.cell(hide_code=True)
def _(
    alt,
    curve_paths,
    ec_a,
    ec_add_real,
    ec_b,
    ec_mirror,
    ec_posA,
    ec_posB,
    experience,
    mo,
    np,
    pd,
):
    _a, _b = ec_a.value, ec_b.value

    def _term(c, sym):
        if c == 0:
            return ""
        mag = f"{abs(c):g}" if (abs(c) != 1 or not sym) else ""
        return f" {'−' if c < 0 else '+'} {mag}{sym}"

    _eq = "y² = x³" + _term(_a, "x") + _term(_b, "")
    _controls = mo.vstack([mo.hstack([ec_a, ec_b], justify="start", gap=2, wrap=True), ec_posA, ec_posB, ec_mirror])
    if abs(4 * _a**3 + 27 * _b**2) < 1e-9:
        _body = mo.callout(
            mo.md(f"With a = {_a} and b = {_b}, 4a³ + 27b² = 0. This curve has a cusp or self-crossing, so point addition breaks down. Change a or b."),
            kind="danger",
        )
    else:
        _path, _segs = curve_paths(_a, _b)
        _A = _path[int(ec_posA.value / 1000 * (len(_path) - 1))]
        _B = _path[int(ec_posB.value / 1000 * (len(_path) - 1))]
        _A = (float(_A[0]), float(_A[1]))
        _B = (float(_B[0]), float(_B[1]))
        if ec_mirror.value:
            _B = (_A[0], -_A[1])
        _C = ec_add_real(_A, _B, _a)
        _curve_rows = [
            {"seg": sid, "order": i, "x": float(x), "y": float(y)}
            for sid, pts in _segs
            for i, (x, y) in enumerate(pts)
        ]
        _xdom, _ydom = [-4.0, 5.0], [-8.0, 8.0]
        _layers = [
            alt.Chart(pd.DataFrame(_curve_rows))
            .mark_line(color="#7f7f7f", clip=True)
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=_xdom)),
                y=alt.Y("y:Q", scale=alt.Scale(domain=_ydom)),
                detail="seg:N",
                order="order:Q",
            )
        ]
        _pts = [{"name": "A", "x": _A[0], "y": _A[1]}, {"name": "B", "x": _B[0], "y": _B[1]}]
        if _C is None:
            _msg = (
                "A and B sit directly above each other, so the line through them is vertical and never meets the curve "
                "again. The sum is the **point at infinity** 𝒪: B = −A, and A + (−A) = 𝒪."
            )
            _layers.append(
                alt.Chart(pd.DataFrame({"x": [_A[0]]}))
                .mark_rule(color="#e45756", strokeDash=[4, 3])
                .encode(x="x:Q")
            )
        else:
            _D = (_C[0], -_C[1])
            _same = abs(_A[0] - _B[0]) < 1e-9 and abs(_A[1] - _B[1]) < 1e-9
            _lam = (3 * _A[0] ** 2 + _a) / (2 * _A[1]) if _same else (_B[1] - _A[1]) / (_B[0] - _A[0])
            _line = pd.DataFrame(
                {"x": [_xdom[0], _xdom[1]], "y": [_A[1] + _lam * (_xdom[0] - _A[0]), _A[1] + _lam * (_xdom[1] - _A[0])]}
            )
            _layers.append(alt.Chart(_line).mark_line(color="#e45756", clip=True).encode(x="x:Q", y="y:Q"))
            _layers.append(
                alt.Chart(pd.DataFrame({"x": [_D[0], _C[0]], "y": [_D[1], _C[1]]}))
                .mark_line(color="#54a24b", strokeDash=[5, 4], clip=True)
                .encode(x="x:Q", y="y:Q")
            )
            _pts += [{"name": "D", "x": _D[0], "y": _D[1]}, {"name": "A+B", "x": _C[0], "y": _C[1]}]
            _off = abs(_C[0]) > 5 or abs(_C[1]) > 8
            _msg = (
                f"A = ({_A[0]:.2f}, {_A[1]:.2f}), B = ({_B[0]:.2f}, {_B[1]:.2f}). "
                + ("A and B are the same point, so the red line is the **tangent** at A. " if _same else "")
                + f"The red line meets the curve again at D = ({_D[0]:.2f}, {_D[1]:.2f}). "
                f"Reflecting D across the x-axis gives **A + B = ({_C[0]:.2f}, {_C[1]:.2f})**."
                + (" (That's off the edge of the chart.)" if _off else "")
            )
            if 4 * _a**3 + 27 * _b**2 < 0:  # three real roots: an oval plus an open branch
                _r = sorted(float(v.real) for v in np.roots([1, 0, _a, _b]))
                _on_oval = lambda P: _r[0] - 1e-6 <= P[0] <= _r[1] + 1e-6
                if _on_oval(_A) and _on_oval(_B):
                    _msg += " A and B are both on the oval, and their sum is on the open branch. That happens for every pair of oval points."
        _pdf = pd.DataFrame(_pts)
        _layers.append(
            alt.Chart(_pdf)
            .mark_circle(size=110, clip=True)
            .encode(
                x="x:Q",
                y="y:Q",
                color=alt.Color(
                    "name:N",
                    scale=alt.Scale(domain=["A", "B", "D", "A+B"], range=["#4c78a8", "#4c78a8", "#e45756", "#54a24b"]),
                    legend=None,
                ),
                tooltip=["name", alt.Tooltip("x:Q", format=".3f"), alt.Tooltip("y:Q", format=".3f")],
            )
        )
        _layers.append(
            alt.Chart(_pdf)
            .mark_text(dx=10, dy=-10, fontSize=13, fontWeight="bold", clip=True)
            .encode(x="x:Q", y="y:Q", text="name:N")
        )
        _chart = alt.layer(*_layers).properties(
            width="container", height=380, title=f"{_eq} over the real numbers"
        )
        _body = mo.vstack([_chart, mo.md(_msg)])
    experience(
        "Elliptic curve playground, part 1: adding points",
        mo.md(
            "Move **A** and **B** along the curve (red line through them, red dot D, green A + B). Which line do you "
            "draw when both sliders match, and what happens when B is A's mirror image (the switch)? Then try "
            "a = −3, b = 1 and add two points on the oval."
        ),
        _controls,
        _body,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - **A new trapdoor**
      - Adding two points is easy, and so is adding a point to itself many times. To get $kA$ for a huge $k$, you double ($A, 2A, 4A, 8A, \dots$) and add up the pieces you need, which takes about $\log_2 k$ steps.
        - For $k = 100 = 64 + 32 + 4$: six doublings reach $64A$, and two additions give $64A + 32A + 4A = 100A$. Eight steps instead of 99.
      - Going backwards is hard. Given $A$ and $E = kA$, find $k$. This is the **elliptic curve discrete logarithm problem**.
        - No efficient algorithm is known for well-chosen curves. The best attacks take about $\sqrt{\text{number of points}}$ steps, around $2^{128}$ for a 256-bit curve.
      - One more twist: over the real numbers you could estimate $k$ from where $kA$ lands, so real ECC works modulo a prime $p$. Every coordinate becomes a whole number from $0$ to $p-1$, and the points scatter with no visible pattern.
        - The same formulas apply, with division done as multiplication by a modular inverse. A small example you can check by hand: $p = 17$, curve $y^2 = x^3 + 7$, $G = (1, 5)$.
          - $G$ is on the curve: $1 + 7 = 8$, and $5^2 = 25 = 8 \pmod{17}$.
          - Doubling uses the tangent slope $\lambda = \frac{3x^2 + a}{2y} = \frac{3}{10}$. Since $10 \times 12 = 120 = 7 \times 17 + 1$, dividing by 10 means multiplying by 12, so $\lambda = 36 = 2 \pmod{17}$.
          - $x = \lambda^2 - 1 - 1 = 2$ and $y = \lambda(1 - 2) - 5 = -7 = 10$, so $2G = (2, 10)$. Check: $2^3 + 7 = 15$ and $10^2 = 100 = 15 \pmod{17}$.
          - In part 2 of the playground below, set p to 17, move the generator slider until G = (1, 5), and set k to 2.
    - A curve scheme is defined by a prime $p$, a curve equation, and an agreed starting point $G$ (the *generator*). Keys come from it like this:
      - **Private key:** a large random integer $n$.
      - **Public key:** the point $E = nG$, meaning $G$ added to itself $n$ times.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ff_p = mo.ui.dropdown(["17", "97", "223"], value="97", label="Prime p")
    ff_a = mo.ui.number(start=0, stop=222, value=0, label="a")
    ff_b = mo.ui.number(start=0, stop=222, value=7, label="b")
    return ff_a, ff_b, ff_p


@app.cell(hide_code=True)
def _(ff_a, ff_b, ff_p, mo):
    FF_P = int(ff_p.value)
    FF_A = int(ff_a.value) % FF_P
    FF_B = int(ff_b.value) % FF_P

    def ff_add(P, Q, p=FF_P, a=FF_A):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P == Q:
            lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    ff_singular = (4 * FF_A**3 + 27 * FF_B**2) % FF_P == 0
    ff_points = [
        (x, y) for x in range(FF_P) for y in range(FF_P) if (y * y - (x**3 + FF_A * x + FF_B)) % FF_P == 0
    ]
    ff_points_nonzero = [pt for pt in ff_points if pt[1] != 0]

    def _order(P):
        n, Q = 1, P
        while Q is not None:
            Q = ff_add(Q, P)
            n += 1
        return n

    # Start on a generator with the largest order, so the find-k challenge isn't trivially small.
    _orders = [_order(pt) for pt in ff_points_nonzero] if not ff_singular else []
    _best = max(range(len(_orders)), key=lambda i: (_orders[i], -i)) if _orders else 0
    ff_g = mo.ui.slider(
        0, max(len(ff_points_nonzero) - 1, 0), value=_best,
        label="Generator G: pick a point", full_width=True,
    )
    return FF_A, FF_B, FF_P, ff_add, ff_g, ff_points, ff_points_nonzero, ff_singular


@app.cell(hide_code=True)
def _(ff_add, ff_g, ff_points_nonzero, mo):
    if ff_points_nonzero:
        ff_G = ff_points_nonzero[ff_g.value]
        ff_multiples = [ff_G]
        while True:
            _nxt = ff_add(ff_multiples[-1], ff_G)
            if _nxt is None:
                break
            ff_multiples.append(_nxt)
        ff_order = len(ff_multiples) + 1  # includes the point at infinity
    else:
        ff_G, ff_multiples, ff_order = None, [], 1
    ff_k = mo.ui.slider(1, max(len(ff_multiples), 1), value=min(5, max(len(ff_multiples), 1)), label="k", show_value=True, full_width=True)
    ff_new = mo.ui.button(value=0, on_click=lambda v: v + 1, label="New challenge")
    ff_guess = mo.ui.number(start=1, stop=max(ff_order - 1, 1), value=1, label="Your guess for k")
    ff_brute = mo.ui.run_button(label="Brute force it")
    return ff_G, ff_brute, ff_guess, ff_k, ff_multiples, ff_new, ff_order


@app.cell(hide_code=True)
def _(
    FF_A,
    FF_B,
    FF_P,
    alt,
    experience,
    ff_G,
    ff_a,
    ff_b,
    ff_brute,
    ff_g,
    ff_guess,
    ff_k,
    ff_multiples,
    ff_new,
    ff_order,
    ff_p,
    ff_points,
    ff_singular,
    mo,
    pd,
    random,
):
    _controls = mo.hstack([ff_p, ff_a, ff_b], justify="start", gap=2, wrap=True)
    _eq = "y² = x³" + (f" + {FF_A}x" if FF_A else "") + (f" + {FF_B}" if FF_B else "")
    if ff_singular or ff_G is None:
        _body = mo.callout(
            mo.md("This choice of a and b gives a singular curve or no usable points. Try a = 0, b = 7 (the same equation Bitcoin uses)."),
            kind="danger",
        )
    else:
        _k = min(ff_k.value, len(ff_multiples))
        _kG = ff_multiples[_k - 1]
        _all = pd.DataFrame([{"x": x, "y": y} for x, y in ff_points])
        _path = pd.DataFrame([{"step": i + 1, "x": P[0], "y": P[1]} for i, P in enumerate(ff_multiples[:_k])])
        _base = (
            alt.Chart(_all)
            .mark_circle(size=28, color="#bab0ac")
            .encode(x=alt.X("x:Q", scale=alt.Scale(domain=[0, FF_P])), y=alt.Y("y:Q", scale=alt.Scale(domain=[0, FF_P])))
        )
        _walk = (
            alt.Chart(_path)
            .mark_line(color="#4c78a8", opacity=0.45, point=alt.OverlayMarkDef(color="#4c78a8", size=40))
            .encode(x="x:Q", y="y:Q", order="step:Q", tooltip=["step", "x", "y"])
        )
        _ends = (
            alt.Chart(pd.DataFrame([{"label": "G", "x": ff_G[0], "y": ff_G[1]}, {"label": f"{_k}G", "x": _kG[0], "y": _kG[1]}]))
            .mark_point(size=260, filled=False, strokeWidth=3, color="#e45756")
            .encode(x="x:Q", y="y:Q")
        )
        _labels = (
            alt.Chart(pd.DataFrame([{"label": "G", "x": ff_G[0], "y": ff_G[1]}, {"label": f"{_k}G", "x": _kG[0], "y": _kG[1]}]))
            .mark_text(dx=14, dy=-12, fontWeight="bold", fontSize=13)
            .encode(x="x:Q", y="y:Q", text="label:N")
        )
        _chart = alt.layer(_base, _walk, _ends, _labels).properties(
            width="container", height=420, title=f"{_eq} (mod {FF_P}): {len(ff_points)} points plus 𝒪"
        )
        _secret = random.Random(f"{FF_P}-{FF_A}-{FF_B}-{ff_G}-{ff_new.value}").randrange(2, max(ff_order - 1, 3))
        _Q = ff_multiples[_secret - 1]
        _g = int(ff_guess.value or 1)
        if _g == _secret:
            _gfb = mo.callout(mo.md(f"Correct: k = {_secret}."), kind="success")
        elif _g <= 1:
            _gfb = mo.md("*Type a guess for k (the secret is at least 2).*")
        else:
            _gfb = mo.callout(
                mo.md(f"Not quite: {_g}G = {ff_multiples[(_g - 1) % len(ff_multiples)] if _g % ff_order else '𝒪'}, but Q = {_Q}."),
                kind="danger",
            )
        _brute = mo.md("")
        if ff_brute.value:
            _brute = mo.callout(
                mo.md(
                    f"Found it: k = {_secret}, after computing G, 2G, 3G, … up to {_secret}G ({_secret} points). "
                    f"With {ff_order} points this is instant. Bitcoin's curve has about $1.16 \\times 10^{{77}}$ points, and even the "
                    "best known attacks would need around $2^{128}$ steps."
                ),
                kind="warn",
            )
        _body = mo.vstack(
            [
                ff_g,
                ff_k,
                mo.md(f"G = {ff_G}, and G has order {ff_order}: adding G to itself {ff_order} times gets back to 𝒪. **{_k}G = {_kG}.** The blue line connects G, 2G, 3G, … {_k}G in order."),
                _chart,
                mo.md(
                    f"Challenge: someone picked a secret k and published **Q = kG = {_Q}**. Find k. "
                    "Moving the k slider until the red circle lands on Q counts as brute force."
                ),
                mo.hstack([ff_guess, ff_new, ff_brute], justify="start", gap=2, align="end", wrap=True),
                _gfb,
                _brute,
            ]
        )
    experience(
        "Elliptic curve playground, part 2: a finite field",
        mo.md(
            "Same rule, every coordinate reduced mod p. Move **k** to see G, 2G, … kG. Before going from 5G to 6G, "
            "guess: will 6G land near 5G? Here kG jumps around, so seeing it tells you almost nothing about k."
        ),
        _controls,
        _body,
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    _p = 2**256 - 2**32 - 977
    mo.vstack(
        [
            mo.md(rf"""
    - Bitcoin (and Ethereum) use the curve **secp256k1**: $y^2 = x^3 + 7$, the same equation as part 2's default curve, but modulo a 78-digit prime instead of 97.
      - Your Bitcoin private key is a random number $n$, and your public key is $nG$ for a fixed generator $G$. Getting $n$ back from $nG$ is the discrete log problem above.
    """),
            mo.accordion(
                {
                    "secp256k1's exact parameters": mo.md(rf"""
    $$y^2 = x^3 + 7 \pmod p, \qquad p = 2^{{256}} - 2^{{32}} - 977$$

    <span style="font-family: monospace; word-break: break-all">{_p}</span>

    The generator $G$ is a fixed point listed in the SEC 2 standard, and the number of multiples of $G$ is a prime $n \approx 1.16 \times 10^{{77}}$, so a private key is a number between 1 and $n - 1$.
    """),
                    "Can a quantum computer steal bitcoin? (as of November 2026)": mo.md(r"""
    A large enough one could (see the post-quantum section), and how exposed a coin is depends on whether its public key has been revealed on-chain. Some older output types and Taproot outputs show it on receipt; the rest reveal it when spent. BIP 360, merged into the BIPs repository as a draft in February 2026, proposes a new output type (P2MR) without Taproot's key-path spend. It has not been activated.
    """),
                }
            ),
            further_reading(
                [
                    ("A (Relatively Easy To Understand) Primer on Elliptic Curve Cryptography (Cloudflare)", "https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/", ""),
                    ("Elliptic curve cryptography video (YouTube)", "https://www.youtube.com/watch?v=gAtBM06xwaw", "from the original lesson's reading list"),
                    ("Elliptic Curve Cryptography (OpenSSL wiki)", "https://wiki.openssl.org/index.php/Elliptic_Curve_Cryptography", ""),
                    ("SEC 2: Recommended Elliptic Curve Domain Parameters", "https://www.secg.org/sec2-v2.pdf", "secp256k1's parameters"),
                    ("NIST SP 800-57 Part 1 Rev. 5", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "key-size equivalences"),
                    ("BIP 360", "https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki", "draft quantum-resistance proposal"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    # Bitcoin: an Introduction to Blockchain

    - A question: if you email a PDF of your resume to a friend, who has the resume?
      - You both do. Great for resumes, terrible for money. If money is just a digital file, we need a file that can't be copied.
    - The centralized fix: trust one institution, like a bank, to "delete" money on the sender's side and "add" it on the receiver's (for a fee).
      - New problem: you're now 100% dependent on the bank's honesty and competence. If it freezes your account, loses your transaction, gets hacked or prints more money behind the scenes, you have no recourse.
    - The original goal of a blockchain: get the security of the bank's ledger without the bank.
      - The idea: if we remove the bank, we all have to become the bank. Everyone keeps a copy of the ledger, and every transaction gets written into every copy.
      - That removes the single point of failure, but it creates three new problems:

    1. **Problem #1:** with no bank to enforce the rules, why can't someone write "I have a billion dollars" in their copy?
    2. **Problem #2:** if everyone is shouting out transactions at the same time, who decides which one goes first?
    3. **Problem #3:** how do strangers who might be trying to rob each other agree on one version of the ledger?

    Bitcoin was the first system to solve all three without a central authority.

    - **Blockchain:** an append-only database that's shared and synchronized across a network of participants, none of whom has to be trusted.
    - **Bitcoin:** the first successful blockchain, described in a whitepaper by the pseudonymous Satoshi Nakamoto (October 2008) and launched in January 2009. The middle-man is math instead of a bank.
    - **BTC:** Bitcoin's currency unit. The consensus rules cap total issuance at just under 21 million BTC.
    """),
            mo.callout(
                mo.md(
                    "Digital signatures (above) and nodes checking every block answer problem #1, blocks chained in "
                    "order answer #2, and proof of work with the most-work rule answers #3."
                ),
                kind="info",
            ),
            mo.accordion(
                {
                    "Why 2009? (history)": mo.md(
                        "In 2008 the global banking system had nearly collapsed, and governments spent enormous sums "
                        "rescuing banks. The first Bitcoin block (the \"genesis block\", mined on January 3, 2009) "
                        "contains the text *\"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks\"*, "
                        "a headline from that day's London *Times*. It's usually read as a comment on those bailouts."
                    )
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ## "Wtf is a blockchain": A Chain of Blocks

    - Remember problem #2: everyone is shouting out transactions at once. Who decides the order?
      - Transactions don't go straight into anyone's ledger. They wait in a shared pool called the **mempool** (more on it in From a Chain to a Network).
      - Then they're bundled into **blocks**, and each block stores the hash of the block before it. That makes one ordered chain, and a transaction's place in the chain is its place in line.
      - The hash link is what stops anyone rewriting the order. Edit "Alice pays Bob" into "Alice pays Mallory" inside an old block, and that block's hash changes completely. It no longer matches the hash stored in the next block, so the edit shows.
    - Every block has a **header** and a list of **transactions**.

    **Block header.** A Bitcoin header is always exactly 80 bytes, with six fields:

    | Field | Size | What it is |
    | :--- | :--- | :--- |
    | Version | 4 bytes | Which rule set the block follows |
    | Previous block hash | 32 bytes | Hash of the previous block's header. This is the link in the "chain" |
    | Merkle root | 32 bytes | One hash that commits to every transaction in the block |
    | Time | 4 bytes | When the miner says the block was made (Unix time) |
    | nBits | 4 bytes | The current difficulty target, in compact form |
    | Nonce | 4 bytes | A number miners change while searching for a valid block (see Mining) |

    The block's own hash is SHA-256 applied twice to these 80 bytes.

    **Block data.** A list of signed transactions. This week they stay abstract ("Alice pays Bob 0.5 BTC").

    **Merkle trees.** How do you get one hash that commits to thousands of transactions?

    - Hashing all the transactions together would commit to them, but proving one is included would mean handing over all of them.
    - A tree fixes that. Hash each transaction. Then hash the results together in pairs, then pair those, and so on, until one hash is left: the **Merkle root**. If a level has an odd number of hashes, Bitcoin pairs the last one with itself.
      - Building the tree takes $O(n)$ hashes for $n$ transactions.
      - To prove one transaction is in the block, you only need the hashes along its path to the root, about $\log_2 n$ of them. With 4 transactions that's 2 hashes (try block 3 in the explorer below); with 4,000 it's 12 instead of 4,000.
      - Change any transaction and its hash changes, which changes every hash above it, including the root, which changes the header.
    - A full node downloads and checks every block and transaction (several hundred gigabytes as of 2026). A light client stores only the 80-byte headers and asks full nodes for Merkle proofs of the transactions it cares about. More on light clients in Week 2.
    """),
            mo.accordion(
                {
                    "Where's the block number?": mo.md(
                        "Not in the header. A block's height is implied by its position, and since 2013 it's also "
                        "written into the block's first transaction (BIP 34), so no two blocks can share an identical "
                        "first transaction. The toy chain below does the same."
                    )
                }
            ),
            mo.mermaid(
                """
    graph TD
        R[Merkle root] --> H12[hash of H1 + H2]
        R --> H34[hash of H3 + H4]
        H12 --> H1[H tx1]
        H12 --> H2[H tx2]
        H34 --> H3[H tx3]
        H34 --> H4[H tx4]
        HDR[Block header: version, prev hash, Merkle root, time, nBits, nonce] --- R
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(leading_zero_bits, mo, sha256d, time):
    GENESIS_PREV = "0" * 64
    BLOCK_TIMES = [1_767_225_600 + 600 * i for i in range(4)]
    DEFAULT_TXS = [
        # Each coinbase names its block height, as Bitcoin has required since BIP 34, so no two are identical.
        "Coinbase (height 1): 3.125 BTC to Miner A",
        "Coinbase (height 2): 3.125 BTC to Miner B\nAlice pays Bob 0.5 BTC\nBob pays Carol 0.2 BTC",
        "Coinbase (height 3): 3.125 BTC to Miner A\nCarol pays Dave 0.1 BTC\nAlice pays Erin 0.05 BTC\nDave pays Bob 0.02 BTC",
        "Coinbase (height 4): 3.125 BTC to Miner C\nErin pays Alice 0.01 BTC",
    ]
    START_BITS = 12

    def tx_lines(text):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return lines or [""]

    def merkle_levels(txs):
        """All levels of the tree, leaves first, as hex strings."""
        level = [sha256d(tx.encode()).hex() for txs_ in [txs] for tx in txs_]
        levels = [level]
        while len(level) > 1:
            if len(level) % 2 == 1:
                level = level + [level[-1]]
            level = [
                sha256d(bytes.fromhex(level[i]) + bytes.fromhex(level[i + 1])).hex()
                for i in range(0, len(level), 2)
            ]
            levels.append(level)
        return levels

    def merkle_root(txs):
        return merkle_levels(txs)[-1][0]

    def toy_header(prev, root, t, bits, nonce):
        # Same fields as Bitcoin's header, written as readable text instead of packed bytes.
        return f"1|{prev}|{root}|{t}|{bits}|{nonce}"

    def block_hash(prev, root, t, bits, nonce):
        return sha256d(toy_header(prev, root, t, bits, nonce).encode()).hex()

    def mine(prev, root, t, bits):
        start = time.perf_counter()
        nonce = 0
        while True:
            h = block_hash(prev, root, t, bits, nonce)
            if leading_zero_bits(h) >= bits:
                return nonce, nonce + 1, time.perf_counter() - start
            nonce += 1

    def chain_status(blocks, texts):
        """Check every block. A block is valid if its hash meets its target, its stored
        previous hash matches the actual previous block, and everything before it is valid."""
        out, prev_actual, all_ok = [], GENESIS_PREV, True
        for i, blk in enumerate(blocks):
            root = merkle_root(tx_lines(texts[i]))
            h = block_hash(blk["prev"], root, BLOCK_TIMES[i], blk["bits"], blk["nonce"])
            meets = leading_zero_bits(h) >= blk["bits"]
            linked = blk["prev"] == prev_actual
            if not meets:
                state = "hash doesn't meet the target"
            elif not linked:
                state = "previous-hash link is broken"
            elif not all_ok:
                state = "builds on an invalid block"
            else:
                state = "valid"
            ok = meets and linked and all_ok
            all_ok = all_ok and ok
            out.append({"root": root, "hash": h, "meets": meets, "linked": linked, "ok": ok, "state": state})
            prev_actual = h
        return out

    # Mine the starting chain once, when the notebook loads.
    _blocks, _prev = [], GENESIS_PREV
    for _i, _txt in enumerate(DEFAULT_TXS):
        _root = merkle_root(tx_lines(_txt))
        _nonce, _, _ = mine(_prev, _root, BLOCK_TIMES[_i], START_BITS)
        _blocks.append({"nonce": _nonce, "prev": _prev, "bits": START_BITS})
        _prev = block_hash(_prev, _root, BLOCK_TIMES[_i], START_BITS, _nonce)

    chain_get, chain_set = mo.state(_blocks)
    minelog_get, minelog_set = mo.state([])
    return (
        BLOCK_TIMES,
        DEFAULT_TXS,
        GENESIS_PREV,
        START_BITS,
        block_hash,
        chain_get,
        chain_set,
        chain_status,
        merkle_levels,
        merkle_root,
        mine,
        minelog_get,
        minelog_set,
        toy_header,
        tx_lines,
    )


@app.cell(hide_code=True)
def _(DEFAULT_TXS, START_BITS, mo):
    chain_tx = mo.ui.array(
        [mo.ui.text_area(value=t, rows=4, full_width=True) for t in DEFAULT_TXS],
    )
    chain_bits = mo.ui.slider(
        8, 18, value=START_BITS, label="Difficulty for blocks you mine (leading zero bits)", show_value=True,
        full_width=True, debounce=True,
    )
    mine_which = mo.ui.dropdown(["1", "2", "3", "4"], value="2", label="Block")
    mine_one = mo.ui.run_button(label="Mine this block")
    mine_fix = mo.ui.run_button(label="Repair the chain: re-mine from the first broken block")
    mine_practice = mo.ui.run_button(label="Mine 5 practice blocks at this difficulty")
    return chain_bits, chain_tx, mine_fix, mine_one, mine_practice, mine_which


@app.cell(hide_code=True)
def _(
    BLOCK_TIMES,
    GENESIS_PREV,
    block_hash,
    chain_bits,
    chain_get,
    chain_set,
    chain_status,
    chain_tx,
    merkle_root,
    mine,
    mine_fix,
    mine_one,
    mine_practice,
    mine_which,
    minelog_set,
    random,
    tx_lines,
):
    # Runs only when one of the mining buttons is pressed.
    if mine_one.value or mine_fix.value:
        _blocks = [dict(b) for b in chain_get()]
        _texts = list(chain_tx.value)
        if mine_one.value:
            _targets = [int(mine_which.value) - 1]
        else:
            _st = chain_status(_blocks, _texts)
            _first = next((i for i, s in enumerate(_st) if not s["ok"]), None)
            _targets = [] if _first is None else list(range(_first, 4))
        _new = []
        for _i in _targets:
            _prev = GENESIS_PREV
            if _i > 0:
                _pb = _blocks[_i - 1]
                _prev = block_hash(_pb["prev"], merkle_root(tx_lines(_texts[_i - 1])), BLOCK_TIMES[_i - 1], _pb["bits"], _pb["nonce"])
            _root = merkle_root(tx_lines(_texts[_i]))
            _nonce, _tries, _secs = mine(_prev, _root, BLOCK_TIMES[_i], chain_bits.value)
            _blocks[_i] = {"nonce": _nonce, "prev": _prev, "bits": chain_bits.value}
            _new.append({"source": f"block {_i + 1}", "bits": chain_bits.value, "tries": _tries, "seconds": round(_secs, 3)})
        chain_set(_blocks)
        minelog_set(lambda log: log + _new)
    if mine_practice.value:
        _new = []
        for _ in range(5):
            _nonce, _tries, _secs = mine(f"{random.getrandbits(64):016x}", "practice", 0, chain_bits.value)
            _new.append({"source": "practice", "bits": chain_bits.value, "tries": _tries, "seconds": round(_secs, 3)})
        minelog_set(lambda log: log + _new)
    return


@app.cell(hide_code=True)
def _(
    chain_bits,
    chain_get,
    chain_status,
    chain_tx,
    experience,
    mine_fix,
    mine_one,
    mine_which,
    mo,
    short,
):
    _blocks = chain_get()
    _status = chain_status(_blocks, chain_tx.value)

    def _card(i):
        blk, st = _blocks[i], _status[i]
        color = "#54a24b" if st["ok"] else "#e45756"
        details = mo.md(
            f"Previous hash: `{short(blk['prev'], 14)}`  \n"
            f"Merkle root: `{short(st['root'], 14)}`  \n"
            f"Nonce: `{blk['nonce']:,}` · target: {blk['bits']} zero bits  \n"
            f"Block hash: `{short(st['hash'], 14)}`  \n"
            + ("**Valid**" if st["ok"] else f"**Invalid:** {st['state']}")
        )
        return mo.vstack([mo.md(f"**Block {i + 1}**"), chain_tx[i], details], gap=0.5).style(
            {
                "border": f"2px solid {color}",
                "border-radius": "10px",
                "padding": "10px 12px",
                "flex": "1 1 260px",
                "min-width": "240px",
            }
        )

    # Two cards per row on a laptop, one per row on a phone.
    _grid = mo.hstack([_card(i) for i in range(4)], gap=1, wrap=True, align="stretch")
    _n_bad = sum(not s["ok"] for s in _status)
    experience(
        "Build, tamper, mine",
        mo.md(
            "This chain is already mined; green means valid, red invalid. In block 2, change \"Alice pays Bob 0.5 "
            "BTC\" to \"Alice pays Mallory 0.5 BTC\". Which blocks will turn red, and why would block 4 care? "
            "Then re-mine to repair the chain."
        ),
        _grid,
        mo.hstack([mine_which, mine_one, mine_fix], justify="start", gap=1, align="end", wrap=True),
        chain_bits,
        mo.md(
            "All blocks valid." if _n_bad == 0
            else f"{_n_bad} block{'s are' if _n_bad > 1 else ' is'} invalid. Re-mining a block gives it a new valid hash, "
            "but the next block still stores the old one, so that link breaks. That's why **Repair the chain** "
            "re-mines every block from the first broken one to the end."
        ),
        mo.md("")
        if _n_bad == 0
        else mo.callout(
            mo.md(
                "Editing a block changes its Merkle root, so its hash changes and no longer meets the target. The next "
                "block stored the *old* hash, so its link breaks too, and every block after builds on an invalid one. "
                "To rewrite history you have to redo the proof of work for the edited block and every block after it, "
                "and on the real network do it faster than everyone else adds new blocks."
            ),
            kind="success",
        ),
        mo.accordion(
            {
                "How this toy chain differs from Bitcoin": mo.md(
                    "- \"Valid\" here only means the hash meets the target and the links match. A real node would also "
                    "reject unsigned transactions and overspending, so \"Alice pays Bob 1000 BTC\" could never be valid.\n"
                    "- The header is a line of text instead of Bitcoin's packed 80 bytes.\n"
                    "- Difficulty is leading zero bits set per block, not a network-wide target.\n"
                    "- Timestamps are fixed, ten minutes apart."
                )
            }
        ),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    proof_block = mo.ui.dropdown(["1", "2", "3", "4"], value="3", label="Block")
    return (proof_block,)


@app.cell(hide_code=True)
def _(chain_tx, mo, proof_block, tx_lines):
    _txs = tx_lines(chain_tx.value[int(proof_block.value) - 1])
    proof_tx = mo.ui.dropdown(
        {f"{i + 1}. {t[:28]}": i for i, t in enumerate(_txs)},
        value=f"1. {_txs[0][:28]}",
        label="Transaction",
    )
    return (proof_tx,)


@app.cell(hide_code=True)
def _(chain_tx, experience, merkle_levels, mo, proof_block, proof_tx, sha256d, short, tx_lines):
    _txs = tx_lines(chain_tx.value[int(proof_block.value) - 1])
    _levels = merkle_levels(_txs)
    _idx = proof_tx.value if proof_tx.value is not None else 0
    _path, _sibs, _steps = set(), set(), []
    _i = _idx
    _running = _levels[0][_idx]
    for _lvl in range(len(_levels) - 1):
        _row = _levels[_lvl]
        _padded = _row + [_row[-1]] if len(_row) % 2 == 1 else _row
        _sib = _i ^ 1
        _path.add((_lvl, _i))
        _sibs.add((_lvl, min(_sib, len(_row) - 1)))
        _copy = " (a copy of itself, because this level has an odd number of hashes)" if _sib >= len(_row) else ""
        if _sib > _i:
            _side = "right"
            _running = sha256d(bytes.fromhex(_running) + bytes.fromhex(_padded[_sib])).hex()
        else:
            _side = "left"
            _running = sha256d(bytes.fromhex(_padded[_sib]) + bytes.fromhex(_running)).hex()
        _steps.append(
            f"Hash it together with `{short(_padded[_sib], 8)}` on the {_side}{_copy}, giving `{short(_running, 8)}`"
        )
        _i //= 2
    _path.add((len(_levels) - 1, 0))
    _root = _levels[-1][0]
    _ok = _running == _root

    _rows_html = []
    for _lvl in reversed(range(len(_levels))):
        _cells = []
        for _j, _h in enumerate(_levels[_lvl]):
            if (_lvl, _j) in _path:
                _look = "background:#fde9a9;color:#222"
            elif (_lvl, _j) in _sibs:
                _look = "background:#cfe3f7;color:#222"
            else:
                _look = "background:transparent"
            _cells.append(
                f"<span style='display:inline-block;margin:2px;padding:3px 6px;border:1px solid rgba(127,127,127,.4);"
                f"border-radius:6px;{_look};font-family:monospace;font-size:11px'>{_h[:8]}</span>"
            )
        _label = "root" if _lvl == len(_levels) - 1 else ("leaves (one per transaction)" if _lvl == 0 else f"level {_lvl}")
        _rows_html.append(
            f"<div style='text-align:center;white-space:nowrap;overflow-x:auto'><small>{_label}</small><br>{''.join(_cells)}</div>"
        )

    _n = len(_txs)
    _check = (
        f"Recomputed root `{short(_running, 8)}` matches the root in block {proof_block.value}'s header ✓"
        if _ok
        else f"Recomputed root `{short(_running, 8)}` does not match `{short(_root, 8)}` ✗"
    )
    experience(
        "Merkle proof explorer",
        mo.md(
            "**Yellow** is the path from a transaction to the root; **blue** is the proof, the sibling hashes a light "
            "client needs. Block 3's 4 transactions need 2. How many for 8, or 5? Add lines to a block above to check."
        ),
        mo.hstack([proof_block, proof_tx], justify="start", gap=2, wrap=True),
        mo.Html("".join(_rows_html)),
        mo.md(
            f"Start from the transaction's own hash `{short(_levels[0][_idx], 8)}`, then:\n\n"
            + "\n".join(f"{k + 1}. {s}" for k, s in enumerate(_steps))
            + f"\n\n{_check}. The proof is **{len(_steps)} hash{'es' if len(_steps) != 1 else ''}** "
            f"for {_n} transaction{'s' if _n != 1 else ''}, and it grows like log₂(n): doubling the transactions adds one hash."
        ),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ## Mining and Proof of Work

    - **Expanding the chain.** Who gets to add the next block? This is problem #3.
      - If anyone could, everyone would write their own conflicting block, and an attacker could create a million fake identities to outvote everyone else (a **Sybil attack**). So adding a block has to cost work nobody can fake. A block is valid only if
        - its header contains the previous block's hash (that's the chain), and
        - its own header hash, read as a 256-bit number, is **at or below a target**.
          - Simplified: "the hash must start with some number of zero bits". The experiments here use this version; the real rule compares the full number against the target stored in nBits.
      - With 12 leading zero bits required, each try succeeds with probability $1/2^{12}$, so a block takes $2^{12} = 4{,}096$ tries on average. That's the difficulty the toy chain above was mined at.
      - The network adjusts the target every 2,016 blocks (about two weeks) so that blocks keep arriving roughly every 10 minutes, however much mining power joins or leaves.
    - To find a valid block, a miner picks transactions from the mempool, builds the Merkle tree, fills in the header, then changes the nonce, hashes, checks, and repeats.
      - There's no shortcut. Pre-image resistance means you can't work backwards from "a hash below the target", and the avalanche effect from the hash lab means one nonce's hash tells you nothing about the next one's.
      - The people and machines doing this are called **miners**. A modern machine (built on ASIC chips) computes hundreds of trillions of hashes per second.
    - Nodes that hold and verify the entire history are **full nodes**.
      - Mining needs a full node, your own or a trusted one. Most miners join a **pool**, whose operator runs the full node while members just hash and share the reward.
      - You don't need a full node to *use* Bitcoin; Week 2 covers the lighter options.
    - **Proof of Work.** Making block producers burn real energy to create a block is called proof of work.
      - It gives block producers something at stake, and it makes rewriting history expensive. If a past block's data changes, its Merkle root changes, so its header hash changes, so a new nonce has to be found for it and for every block after it.
      - It defeats Sybil attacks, because influence is measured by share of the total hashing power, and a thousand accounts add none.
      - The miner who finds a block collects a *block subsidy* (newly issued BTC) plus the fees from every transaction in it.
        - The subsidy halves every 210,000 blocks, roughly every four years, on a fixed schedule written into the rules. It has been 3.125 BTC since the April 2024 halving at block 840,000; the next halving, at block 1,050,000, is expected around 2028.
    """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, chain_bits, minelog_get, mine_practice, mo, np, pd):
    _log = minelog_get()
    _xs = np.arange(8, 19)
    _exp = pd.DataFrame({"bits": _xs, "expected": 2.0**_xs})
    _line = alt.Chart(_exp).mark_line(color="#bab0ac", strokeDash=[6, 4]).encode(
        x=alt.X("bits:Q", title="Difficulty (leading zero bits)", scale=alt.Scale(domain=[7.5, 18.5]), axis=alt.Axis(tickMinStep=1, format="d")),
        y=alt.Y("expected:Q", scale=alt.Scale(type="log"), title="Hashes tried (log scale)"),
    )
    if _log:
        _df = pd.DataFrame(_log)
        _pts = alt.Chart(_df).mark_circle(size=60, opacity=0.8).encode(
            x="bits:Q",
            y="tries:Q",
            color=alt.Color("source:N", legend=alt.Legend(title=None, orient="top")),
            tooltip=["source", "bits", "tries", "seconds"],
        )
        _chart = (_line + _pts).properties(height=260, width="container", title="Every block you've mined vs. the expected number of tries (dashed)")
        _last = _df.iloc[-1]
        _summary = (
            f"Last mine: **{int(_last['tries']):,} hashes** at {int(_last['bits'])} bits "
            f"(expected about {2 ** int(_last['bits']):,}). Individual results scatter a lot, because each try is an "
            "independent lottery ticket."
        )
    else:
        _chart = _line.properties(height=260, width="container", title="Expected hashes per block")
        _summary = "Every block you mine in the chain above, and every practice block, shows up here as a dot."
    mo.vstack(
        [
            mo.md(
                r"How much work is a block? With a target of $b$ leading zero bits, each try succeeds with probability $1/2^b$, "
                r"so on average $2^b$ tries. (Python here manages about a million hashes a second, so the slider stops at "
                r"18 bits.) Mine 5 practice blocks at 12 bits, then 5 at 16: how many times more work should the 16-bit "
                r"ones take, and will every one take longer?"
            ),
            mo.hstack([chain_bits, mine_practice], widths=[3, 2], align="center", wrap=True),
            _chart,
            mo.md(_summary),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, further_reading, mo, pd):
    _rows, _total_sat, _sub = [], 0, 50 * 100_000_000
    for _era in range(34):
        _total_sat += 210_000 * _sub
        _rows.append({"year": 2009 + 4 * (_era + 1), "issued": _total_sat / 1e8, "subsidy": _sub / 1e8})
        _sub //= 2
    _df = pd.DataFrame([{"year": 2009, "issued": 0.0, "subsidy": 50.0}] + _rows)
    _chart = (
        alt.Chart(_df[_df["year"] <= 2141])
        .mark_line(interpolate="step-after", color="#4c78a8")
        .encode(
            x=alt.X("year:Q", title="Approximate year", axis=alt.Axis(format="d")),
            y=alt.Y("issued:Q", title="Total BTC issued (millions)", axis=alt.Axis(labelExpr="datum.value / 1e6")),
            tooltip=[alt.Tooltip("year:Q", title="approx. year"), alt.Tooltip("issued:Q", title="BTC issued", format=",.0f"), alt.Tooltip("subsidy:Q", title="subsidy per block (BTC)")],
        )
        .properties(height=220, width="container", title="Bitcoin's issuance schedule (each step is one halving)")
    )
    _now = alt.Chart(pd.DataFrame({"x": [2026]})).mark_rule(color="#e45756", strokeDash=[4, 3]).encode(x="x:Q")
    mo.vstack(
        [
            _chart + _now,
            mo.md(
                "You can check the cap by hand: the first 210,000 blocks paid 50 BTC each, which is 10.5 million BTC. "
                "Each later era pays half the one before, so the total approaches 2 × 10.5 = 21 million. "
                f"Rounding to whole satoshis makes it exactly **{_total_sat / 1e8:,.8f} BTC**, the last of it issued around "
                "2140; after that, miners earn fees alone. The red line is 2026."
            ),
            further_reading(
                [
                    ("Bitcoin: A Peer-to-Peer Electronic Cash System (whitepaper)", "https://bitcoin.org/bitcoin.pdf", ""),
                    ("How does Bitcoin mining work? (bitcoin.org FAQ)", "https://bitcoin.org/en/faq#how-does-bitcoin-mining-work", ""),
                    ("Bitcoin developer reference: block chain", "https://developer.bitcoin.org/reference/block_chain.html", "the header format byte by byte"),
                    ("Mastering Bitcoin, 3rd edition (free online)", "https://github.com/bitcoinbook/bitcoinbook", "chapters on mining and the network"),
                    ("Blockchain demo (Anders Brownworth)", "https://andersbrownworth.com/blockchain/blockchain", "another hands-on chain to tamper with"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(r"""
    ## From a Chain to a Network

    Up until now we've only looked at the chain from a single node's point of view. In practice thousands of nodes each keep their own copy, and they have to agree on one chain.

    **Making blocks.**

    - A **transaction** is a request to change the network's state. In Bitcoin, the only change possible is spending existing coins and creating new ones.
    - Bitcoin tracks coins with the **UTXO model** (unspent transaction outputs). Each UTXO is a discrete chunk of BTC locked to an owner. A transaction consumes some UTXOs as inputs and creates new ones as outputs, like paying with bills and getting change; your "balance" is the sum of the UTXOs you can spend.
    - Users sign transactions with their private key and broadcast them to the network.
    - Nodes check each incoming transaction (valid signatures, inputs not already spent, outputs not larger than inputs). Valid ones go into the node's mempool, the waiting area from A Chain of Blocks.
      - This completes the answer to problem #1: every node checks every transaction and every block, so a "billion dollars for me" entry is rejected everywhere.
    - Miners pick transactions from their mempool, usually the ones paying the most fee for the block space they take up, assemble a block, and search for a nonce. When they find one, they broadcast the block.

    For example, say Alice owns two UTXOs, worth 0.5 and 0.3 BTC. She wants to pay Bob 0.6 BTC.

    | | Amount |
    | :--- | :--- |
    | Input: Alice's UTXO #1 | 0.5 BTC |
    | Input: Alice's UTXO #2 | 0.3 BTC |
    | Output: to Bob | 0.6 BTC |
    | Output: change back to Alice | 0.1999 BTC |
    | Fee to the miner (inputs − outputs) | 0.0001 BTC |

    Both old UTXOs are now spent for good; Bob has a new 0.6 BTC UTXO and Alice a 0.1999 BTC one.

    **Gossip.** Nodes share new transactions and blocks by *gossip*: when a node learns something new, it checks it and passes it on to its peers. By default each node opens 8 outbound connections that relay everything, plus 2 that relay only blocks. A new block reaches most of the network within seconds.

    Back to problem #3: which chain does everyone agree on?

    - Sometimes two miners, say in Tokyo and Berkeley, find valid blocks at almost the same moment, and the network briefly splits.
    - "Follow the longest chain" is the usual intuition, since more blocks usually means more work. But an attacker could mine a long chain at trivially low difficulty, so nodes actually follow the valid chain with the **most cumulative proof of work**.
      - Chain A has 1,000 blocks at difficulty 1 (1,000 units of work). Chain B has 900 blocks at difficulty 2 (1,800 units). Nodes follow B, even though it's shorter.
    - In the Tokyo–Berkeley split, each miner builds on the block it saw first. When one side finds the next block, its chain has more work and everyone switches. The losing block is *stale*; its transactions go back into mempools.
    """),
            mo.accordion(
                {
                    "How many peers can a node have in total?": mo.md(
                        "Besides its 10 outbound connections, Bitcoin Core accepts inbound ones, up to 125 peers in "
                        "total by default (`src/net.h`)."
                    )
                }
            ),
            mo.mermaid(
                """
    graph LR
        W[Wallet signs a transaction] --> N1[Node checks it]
        N1 -->|valid| MP[Mempool]
        N1 -->|gossip| P[Peers check and relay it]
        MP --> M[Miner picks transactions by fee rate]
        M --> B[Finds a valid nonce]
        B -->|gossip| ALL[Every node checks the block and extends its chain]
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_work = mo.ui.radio(
        options=[
            "Chain A: 1,000 blocks mined at low difficulty",
            "Chain B: 900 blocks mined at high difficulty, more total work",
            "Whichever chain the node heard about first",
        ],
        label="Quick check: a node sees two valid chains. Which one does it follow?",
    )
    quiz_work
    return (quiz_work,)


@app.cell(hide_code=True)
def _(quiz_feedback, quiz_work):
    quiz_feedback(
        quiz_work.value,
        {
            "Chain A: 1,000 blocks mined at low difficulty": (
                False,
                "More blocks isn't the rule; more *work* is. Otherwise an attacker could mine a long chain at "
                "trivially low difficulty and take over.",
            ),
            "Chain B: 900 blocks mined at high difficulty, more total work": (
                True,
                "Nodes follow the valid chain with the most cumulative proof of work. \"Longest chain\" is shorthand "
                "that works only when difficulty is the same on both sides.",
            ),
            "Whichever chain the node heard about first": (
                False,
                "That's only the tie-breaker when two chains have *equal* work, like the Tokyo/Berkeley split. "
                "Once one side has more work, every node switches to it.",
            ),
        },
    )
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            further_reading(
                [
                    ("Bitcoin's P2P Network (nakamoto.com)", "https://nakamoto.com/bitcoins-p2p-network/", "peer discovery, spam defense, privacy"),
                    ("Mastering Bitcoin, 3rd ed.: The Bitcoin Network", "https://github.com/bitcoinbook/bitcoinbook", ""),
                    ("Bitcoin Core net.h", "https://github.com/bitcoin/bitcoin/blob/master/src/net.h", "where the default connection counts are set"),
                ]
            ),
            mo.md(r"""
    ## Properties of Bitcoin

    - Bitcoin is a decentralized, peer-to-peer network.
      - No central authority tells anyone what to do, so the design can't count on any participant: a node might be offline, malicious or buggy.
    - Miners are paid to build on whichever chain they believe will win.
      - A block on a weaker branch probably won't stay in the chain, and its reward disappears with it.
    - Miners choose what goes into their blocks.
      - Within the rules, a miner decides which transactions go in and in what order. In DeFi that order can be worth money (Weeks 5 and 6).
    - What if someone owns more than half of all the computing power?
      - They can reorganize recent history. Their private chain will eventually have more work than the public one, and nodes follow the most work, so when they publish it, any transactions only in the replaced blocks are undone.
        - That's how a **double-spend** works: pay a merchant, wait for them to ship, then publish a chain where the payment never happened.
      - They can censor transactions, by refusing to include them and orphaning any block that does.
      - They still can't steal coins from someone else's address, create coins beyond the subsidy, or change the rules. Remember the answer to problem #1: every node checks every signature and every block, and no amount of work makes an invalid block valid.
    - A smaller attacker can still try a double-spend; they just won't always win.
      - Merchants protect themselves by waiting for **confirmations**, blocks on top of the one that contains their payment, before treating it as final.
      - With 10% of the hashrate against a merchant who waits for 6 confirmations, the attacker wins about 0.06% of the time by the exact formula (Rosenfeld, 2014). The whitepaper's approximation in section 11 says 0.024% for the same case; the simulation below starts at those numbers and shows why the two differ.

    The cost of a sustained majority attack depends on the network's hashrate and the price of that much mining hardware, both of which change week to week.
    """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ds_q = mo.ui.slider(
        1, 49, step=1, value=10, label="Attacker's share of the hashrate, q (%)", show_value=True,
        full_width=True, debounce=True,
    )
    ds_z = mo.ui.slider(
        0, 10, value=6, label="Confirmations the merchant waits for, z (blocks)", show_value=True,
        full_width=True, debounce=True,
    )
    ds_trials = mo.ui.dropdown(["2,000", "10,000", "50,000"], value="50,000", label="Races per point")
    ds_rerun = mo.ui.run_button(label="Re-run with new random races")
    return ds_q, ds_rerun, ds_trials, ds_z


@app.cell(hide_code=True)
def _(ds_q, ds_rerun, ds_trials, math, np):
    def simulate_double_spend(q, z, trials, rng, give_up=50):
        """Monte Carlo: each block goes to the attacker with probability q.
        The merchant ships once the honest chain has z blocks after the payment.
        The attacker wins if their private chain ever catches up after that."""
        if z == 0:
            return 1.0
        p = 1 - q
        k = rng.negative_binomial(z, p, size=trials)  # attacker blocks while honest finds z
        deficit = z - k
        win = deficit <= 0
        active = ~win
        d = deficit.astype(np.int64)
        while active.any():
            idx = np.flatnonzero(active)
            d[idx] += np.where(rng.random(idx.size) < q, -1, 1)
            won = d[idx] <= 0
            lost = d[idx] > give_up
            win[idx[won]] = True
            active[idx[won | lost]] = False
        return float(win.mean())

    def nakamoto_prob(q, z):
        """Whitepaper section 11 (Poisson approximation of the attacker's progress)."""
        p = 1 - q
        lam = z * q / p
        s = 1.0
        for k in range(z + 1):
            poisson = math.exp(-lam) * lam**k / math.factorial(k)
            s -= poisson * (1 - (q / p) ** (z - k))
        return max(s, 0.0)

    def rosenfeld_prob(q, z):
        """Exact probability (Rosenfeld 2014), negative binomial for the attacker's progress."""
        if z == 0:
            return 1.0
        p = 1 - q
        s = 1.0
        for m in range(z + 1):
            s -= math.comb(m + z - 1, m) * (p**z * q**m - p**m * q**z)
        return max(s, 0.0)

    _ = ds_rerun.value  # re-run when the button is pressed
    _trials = int(ds_trials.value.replace(",", ""))
    _rng = np.random.default_rng()
    ds_results = [
        {
            "z": z,
            "simulated": simulate_double_spend(ds_q.value / 100, z, _trials, _rng),
            "exact": rosenfeld_prob(ds_q.value / 100, z),
            "nakamoto": nakamoto_prob(ds_q.value / 100, z),
            "trials": _trials,
        }
        for z in range(0, 11)
    ]
    return ds_results, nakamoto_prob, rosenfeld_prob, simulate_double_spend


@app.cell(hide_code=True)
def _(mo, random):
    race_get, race_set = mo.state(None)

    def new_race(q, z):
        s = {"q": q, "z": z, "honest": 0, "attacker": 0, "seq": [], "seed": random.randrange(10**9), "status": "mining"}
        return _settle(s)

    def _settle(s):
        if s["honest"] >= s["z"]:
            if s["attacker"] >= s["honest"]:
                s["status"] = "won"
            elif s["honest"] - s["attacker"] > 50:
                s["status"] = "lost"
            else:
                s["status"] = "racing"
        return s

    def race_step(s):
        if s is None or s["status"] in ("won", "lost"):
            return s
        s = dict(s)
        who = "A" if random.Random(f"{s['seed']}-{len(s['seq'])}").random() < s["q"] else "H"
        s["seq"] = s["seq"] + [who]
        if who == "A":
            s["attacker"] += 1
        else:
            s["honest"] += 1
        return _settle(s)

    def race_finish(s):
        for _ in range(5000):
            if s is None or s["status"] in ("won", "lost"):
                break
            s = race_step(s)
        return s

    return new_race, race_finish, race_get, race_set, race_step


@app.cell(hide_code=True)
def _(ds_q, ds_z, mo, new_race, race_finish, race_set, race_step):
    race_new_btn = mo.ui.button(label="Start a new race", on_click=lambda _: race_set(new_race(ds_q.value / 100, ds_z.value)))
    race_next_btn = mo.ui.button(label="Next block", on_click=lambda _: race_set(race_step))
    race_end_btn = mo.ui.button(label="Run to the end", on_click=lambda _: race_set(race_finish))
    return race_end_btn, race_new_btn, race_next_btn


@app.cell(hide_code=True)
def _(alt, mo, pd, race_end_btn, race_get, race_new_btn, race_next_btn):
    _s = race_get()
    if _s is None:
        _view = mo.md("*Press **Start a new race** to watch one double-spend attempt block by block, using the q and z set above.*")
    else:
        _df = pd.DataFrame(
            [
                {"chain": "Honest chain", "blocks since payment": _s["honest"]},
                {"chain": "Attacker's private chain", "blocks since payment": _s["attacker"]},
            ]
        )
        _bars = (
            alt.Chart(_df)
            .mark_bar()
            .encode(
                y=alt.Y("chain:N", title=None, sort=None),
                x=alt.X(
                    "blocks since payment:Q",
                    title="Blocks since the payment",
                    scale=alt.Scale(domainMin=0, domainMax=max(_s["z"], _s["honest"], _s["attacker"], 1) + 1),
                ),
                color=alt.Color("chain:N", scale=alt.Scale(range=["#e45756", "#4c78a8"]), legend=None),
            )
            .properties(height=90, width="container")
        )
        _rule = (
            alt.Chart(pd.DataFrame({"x": [_s["z"]]}))
            .mark_rule(color="#54a24b", strokeDash=[5, 3], size=2)
            .encode(x=alt.X("x:Q", title="Blocks since the payment"))
        )
        _seq = " ".join(_s["seq"][-60:]) or "(no blocks yet)"
        _status = {
            "mining": f"The merchant is waiting for {_s['z']} confirmations (green line). The attacker mines in secret.",
            "racing": f"The merchant has shipped. The attacker is {_s['honest'] - _s['attacker']} block{'s' if _s['honest'] - _s['attacker'] != 1 else ''} behind and needs to catch up.",
            "won": (
                "With z = 0 the merchant ships before any block is mined, so the attacker wins without mining at all."
                if _s["z"] == 0
                else "**The attacker caught up.** They publish their chain, it has at least as much work as the honest one, and the payment disappears from history."
            ),
            "lost": "**The attacker gave up**, more than 50 blocks behind. The payment is safe.",
        }[_s["status"]]
        _view = mo.vstack(
            [
                _bars + _rule,
                mo.md(f"Blocks so far (H = honest, A = attacker): `{_seq}`  \n{_status}  \n*q = {_s['q']:.0%}, z = {_s['z']}*"),
            ]
        )
    race_view = mo.vstack([mo.hstack([race_new_btn, race_next_btn, race_end_btn], justify="start", gap=1, wrap=True), _view])
    return (race_view,)


@app.cell(hide_code=True)
def _(alt, ds_q, ds_rerun, ds_results, ds_trials, ds_z, experience, mo, pd, race_view):
    _rows = []
    for r in ds_results:
        if r["simulated"] > 0:
            _rows.append({"z": r["z"], "probability": r["simulated"], "series": "Simulated"})
        _rows.append({"z": r["z"], "probability": max(r["exact"], 1e-12), "series": "Exact formula (Rosenfeld)"})
        _rows.append({"z": r["z"], "probability": max(r["nakamoto"], 1e-12), "series": "Whitepaper approximation"})
    _df = pd.DataFrame(_rows)
    _color = alt.Color(
        "series:N",
        scale=alt.Scale(
            domain=["Simulated", "Exact formula (Rosenfeld)", "Whitepaper approximation"],
            range=["#4c78a8", "#e45756", "#bab0ac"],
        ),
        legend=alt.Legend(title=None, orient="bottom", columns=1),
    )
    _y = alt.Y("probability:Q", scale=alt.Scale(type="log", domainMin=1e-6, domainMax=1, clamp=True), title="Attacker success probability (log scale)")
    _lines = (
        alt.Chart(_df[_df["series"] != "Simulated"])
        .mark_line(strokeWidth=2)
        .encode(x=alt.X("z:Q", title="Confirmations waited for (z)", axis=alt.Axis(tickMinStep=1, format="d")), y=_y, color=_color, strokeDash=alt.StrokeDash("series:N", legend=None))
    )
    _pts = (
        alt.Chart(_df[_df["series"] == "Simulated"])
        .mark_circle(size=80)
        .encode(x="z:Q", y=_y, color=_color, tooltip=["z", alt.Tooltip("probability:Q", format=".4%")])
    )
    _sel = alt.Chart(pd.DataFrame({"z": [ds_z.value]})).mark_rule(color="#54a24b", strokeDash=[4, 3]).encode(x="z:Q")
    _chart = (_lines + _pts + _sel).properties(height=300, width="container", title=f"Attacker success, q = {ds_q.value / 100:.0%}")

    _r = ds_results[ds_z.value]
    _wins = round(_r["simulated"] * _r["trials"])
    _below = next((r["z"] for r in ds_results if r["exact"] < 0.001), None)
    _below_wp = next((r["z"] for r in ds_results if r["nakamoto"] < 0.001), None)
    _summary = (
        f"With **{ds_q.value / 100:.0%}** of the hashrate and a merchant waiting for **{ds_z.value}** confirmation"
        f"{'s' if ds_z.value != 1 else ''}, the attacker won **{_wins:,} of {_r['trials']:,}** simulated races "
        f"({_r['simulated']:.3%}); exact formula {_r['exact']:.3%}, whitepaper {_r['nakamoto']:.3%}. "
        + (
            f"At this q, the exact formula says {_below} confirmations push the risk below 0.1%"
            + (f"; the whitepaper's formula says {_below_wp}." if _below_wp is not None and _below_wp != _below else ".")
            if _below is not None
            else "At this q, even 10 confirmations don't push the risk below 0.1%."
        )
        + (" Simulated points with zero wins aren't plotted." if any(r["simulated"] == 0 for r in ds_results) else "")
    )
    _assumptions = mo.accordion(
        {
            "How the model works, and what it leaves out": mo.md(r"""
    Each new block goes to the attacker with probability $q$, otherwise to the honest network. The attacker mines privately from the moment the payment is broadcast; the merchant ships once the honest chain has $z$ blocks on top; after that the attacker wins if their chain ever catches up. They give up 50 blocks behind, which only shows at the top of the slider (about 1 percentage point at q = 49%).

    The whitepaper approximates the attacker's progress with a Poisson distribution; Rosenfeld (2014) derived the exact result, which the simulation follows. For small attackers the whitepaper underestimates the risk by about half (q = 10%, z = 5: 0.09% against 0.18%), so its table says 5 confirmations get a 10% attacker below 0.1% where the exact formula says 6. Past q ≈ 35–40% it overestimates instead.

    The model assumes fixed hashrate shares and difficulty, instant block propagation, no head start for the attacker, and that catching up counts as winning (as in both formulas; in practice an attacker needs to get one block ahead). It leaves out selfish mining, censorship, eclipse attacks, and the economics of the attack.
    """)
        }
    )
    experience(
        "Double-spend race (simulation)",
        mo.callout(
            mo.md(
                "Before you touch anything: an attacker controls 10% of the hashrate. How many confirmations does a "
                "merchant need before the chance of being double-spent drops below 0.1%?"
            ),
            kind="warn",
        ),
        mo.md(
            "For every z from 0 to 10 the notebook runs thousands of races (blue dots) and compares them with two "
            "formulas; the green line marks your z. Where wins are rare, the dots scatter: that's sampling noise, "
            "and more races per point shrink it."
        ),
        ds_q,
        ds_z,
        mo.hstack([ds_trials, ds_rerun], justify="start", gap=1, align="end", wrap=True),
        _chart,
        mo.md(_summary),
        mo.md(
            "Each confirmation multiplies the attacker's odds by a roughly constant factor, so the risk falls "
            "exponentially (a straight line on the log chart). There's no cliff at 50%: at q = 30% the attacker still "
            "wins about one race in six against 6 confirmations. Above 50% the attacker eventually wins every race."
        ),
        mo.md("You can also watch a single race, block by block:"),
        race_view,
        _assumptions,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _options = [
        "Reverse a payment they made themselves",
        "Keep certain transactions out of blocks",
        "Spend coins from someone else's address",
        "Pay themselves 1,000 BTC in a block",
    ]
    quiz_51 = mo.ui.array(
        [mo.ui.checkbox(label=o) for o in _options],
        label="Last check: a mining pool controls 60% of the hashrate. Which of these can it do? Tick every one that applies.",
    ).form(submit_button_label="Check my answers")
    quiz_51_options = _options
    quiz_51
    return quiz_51, quiz_51_options


@app.cell(hide_code=True)
def _(mo, quiz_51, quiz_51_options):
    _correct = {"Reverse a payment they made themselves", "Keep certain transactions out of blocks"}
    _why = {
        "Reverse a payment they made themselves": "Yes: that's a double-spend, done by publishing a private chain with more work.",
        "Keep certain transactions out of blocks": "Yes: they can refuse to include them and orphan other miners' blocks that do.",
        "Spend coins from someone else's address": "No: that needs a valid signature from the owner's private key, and hashing power can't forge one.",
        "Pay themselves 1,000 BTC in a block": "No: a block that issues more than the subsidy plus fees is invalid, and every full node rejects it regardless of the work behind it.",
    }
    _ticked = [o for o, on in zip(quiz_51_options, quiz_51.value or []) if on]
    _sel = set(_ticked)
    if quiz_51.value is None:
        _fb = mo.md("*Tick your answers, then press **Check my answers**.*")
    elif not _sel:
        _fb = mo.callout(mo.md("**Not quite.** A majority attacker can do two of these. Try again."), kind="danger")
    else:
        _lines = [f"- {_why[o]}" for o in _ticked]
        _missed = _correct - _sel
        if _sel == _correct:
            _head, _kind = "**Right.**", "success"
        else:
            _head, _kind = "**Not quite.**", "danger"
            if _missed:
                _lines.append(f"- You missed: {', '.join(sorted(_missed))}.")
        _fb = mo.callout(mo.md(_head + "\n\n" + "\n".join(_lines)), kind=_kind)
    _fb
    return


@app.cell(hide_code=True)
def _(further_reading, mo):
    mo.vstack(
        [
            mo.md(r"""
    You may have noticed we spent very little time on what exactly a transaction contains and how it's verified. That's on purpose; we'll get there later. This week, focus on Bitcoin's network architecture and how it reaches agreement.
    """),
            further_reading(
                [
                    ("Bitcoin whitepaper, section 11: Calculations", "https://bitcoin.org/bitcoin.pdf", "the original double-spend analysis"),
                    ("Rosenfeld, Analysis of Hashrate-Based Double Spending (2014)", "https://arxiv.org/abs/1402.2009", "the exact formula used above"),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Key takeaways

    If the week worked, you can now explain to a friend why a 256-bit hash gives only 128 bits of collision resistance, why HTTPS uses public-key cryptography only for the handshake, and why a wallet signs a transaction instead of encrypting it. You can also say why nodes follow the chain with the most work rather than the most blocks, and tell them what a miner with 60% of the hashrate can and can't do to their coins.

    Next week covers consensus and distributed systems, including light clients and what happens when nodes disagree.

    # Homework

    *Coming soon.* The homework will take about 30 minutes: guided coding where you rebuild the Merkle root and header hash of a real Bitcoin block, a few short questions on this week, and a final step that records your completion on a public testnet. You won't need real funds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sources

    Facts that change over time were checked in November 2026.

    **Cryptography standards and guidance**

    - NIST, [FIPS 197: Advanced Encryption Standard](https://csrc.nist.gov/pubs/fips/197/final)
    - NIST, [FIPS 180-4: Secure Hash Standard (SHA-2)](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
    - NIST, [FIPS 202: SHA-3 Standard](https://csrc.nist.gov/pubs/fips/202/final)
    - NIST, [FIPS 203 (ML-KEM)](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204 (ML-DSA)](https://csrc.nist.gov/pubs/fips/204/final), [FIPS 205 (SLH-DSA)](https://csrc.nist.gov/pubs/fips/205/final), August 2024
    - NIST, [NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption), March 11, 2025
    - NIST, [IR 8547: Transition to Post-Quantum Cryptography Standards](https://csrc.nist.gov/pubs/ir/8547/final), final, October 27, 2026 (Tables 2 and 4 give the 2030 and 2035 dates; section 2.1 covers HQC and FALCON)
    - NIST, [SP 800-57 Part 1 Rev. 5: Recommendation for Key Management](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
    - IETF, [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
    - OWASP, [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
    - SECG, [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)

    **Research**

    - C. Gidney, [How to factor 2048 bit RSA integers with less than a million noisy qubits](https://arxiv.org/abs/2505.15917), May 2025
    - Iceberg Quantum, [Pinnacle Architecture preprint](https://arxiv.org/abs/2602.11457), February 2026
    - M. Rosenfeld, [Analysis of Hashrate-Based Double Spending](https://arxiv.org/abs/1402.2009), 2014
    - Wikipedia, [RSA numbers](https://en.wikipedia.org/wiki/RSA_numbers) (RSA-896 factored September 19, 2026; checked November 17, 2026)
    - [When Textbook RSA is Used to Protect the Privacy of Hundreds of Millions of Users](https://arxiv.org/abs/1802.03367), 2018
    - T. Kelly, "The Myth of the Skytale," *Cryptologia* 22(3), 1998
    - Berkeley CS70, [Note 7: Public Key Cryptography](https://www.eecs70.org/assets/pdf/notes/n7.pdf)

    **Bitcoin**

    - S. Nakamoto, [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf), 2008
    - [Bitcoin developer reference: block chain](https://developer.bitcoin.org/reference/block_chain.html)
    - [BIP 34](https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki) (block height in coinbase), [BIP 340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) (Schnorr signatures), [BIP 360](https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki) (draft, P2MR)
    - [Bitcoin Core `src/net.h`](https://github.com/bitcoin/bitcoin/blob/master/src/net.h) (default peer connections)
    - A. Antonopoulos and D. Harding, [Mastering Bitcoin, 3rd edition](https://github.com/bitcoinbook/bitcoinbook), 2023

    **Browsers and TLS**

    - Google Security Blog, [A new path for Kyber on the web](https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html), September 13, 2024
    - Cloudflare, [Post-quantum support in browsers and clients](https://developers.cloudflare.com/ssl/post-quantum-cryptography/pqc-support/) (default versions for Chrome, Firefox and Safari; checked November 17, 2026)

    **Lesson material this notebook is based on**

    - Blockchain at Berkeley, [Week 1: Fundamentals and Bitcoin](https://blockchain-at-berkeley.notion.site/Week-1-Fundamentals-and-Bitcoin-dbd7a832870e4f9cbed0af510206a0cc) (Notion, updated September 24, 2025), with its "digital sigs" and "bitcoin" slide decks
    """)
    return


if __name__ == "__main__":
    app.run()
