# Section checklist

Every heading from the original Week 1 page, in its original order, and where it is in `week1.py`. All headings are kept with their original wording; the only change is the "Adlema" typo fixed to "Adleman".

| Original section | Notebook location | Interactive content |
| :--- | :--- | :--- |
| *(new)* Learning objectives | Top of notebook, after the title | |
| First lecture! Woooo | Same heading | Members-only Slack tip in a callout (the original's Slack screenshot is not reproduced) |
| └ Important discussions that we need to have: (Building Your Cohort, Crypto / blockchain imposter syndrome, Slack) | Same heading; both topics kept | |
| Cryptography 101 | Same heading | |
| └ A Brief Overview | Same heading; images replaced by a dated timeline table | |
| └└ Ancient Cryptography (Scytale, Caesar, Enigma, Bletchley Park, Further Reading) | Same heading; all four topics kept, Further Reading in an accordion | Experiment 0: Break a Caesar cipher |
| └ Types of Cryptography (symmetric, asymmetric, key exchange) | Same heading; all three kept | TLS sequence diagram; quick check |
| └ Wtf is "post quantum cryptography" | Same heading; "If we have time" toggle kept as an "Optional" accordion | |
| └ Wtf is "fully homomorphic encryption" (FHE) | Same heading; optional accordion | |
| └ Hash Functions (properties, what this means, password example, well-known hashes, how they work, Further Reading) | Same heading; all subtopics kept | Experiment 1: Hash lab (avalanche + collision hunt with prediction question); hashing diagram |
| Examples of Asymmetric encryption | Same heading | |
| └ Asymmetric Encryption: Textbook RSA (Rivest-Shamir-Adleman) | Same heading (typo fixed) | |
| └└ Some preliminary info that is relevant to most cryptographic concepts: (trapdoor functions, pop quiz, factoring dialogue) | Same heading | Pop quiz with feedback |
| └└ RSA (keys, procedure, analogy, Tencent paper, proof, Further Reading) | Same heading; proof in an accordion | Experiment 2: RSA by hand; Factor N like an attacker |
| └ Digital Signatures (deck content, motivation, math, Further Reading) | Same heading; deck story folded into the text | Experiment 2b: Sign, tamper, verify; signature diagram |
| └ Elliptic Curve Cryptography (ECC) (motivation) | Same heading | |
| └└ Elliptic Curves and their properties (point addition, edge cases, new trapdoor, finite fields, keys, secp256k1, Further Reading) | Same heading | Experiment 3: Elliptic curve playground, parts 1 and 2 (part 1 has a B = −A switch; part 2 gives feedback on wrong guesses) |
| Bitcoin: an Introduction to Blockchain | Same heading; bitcoin deck intro added | |
| └ "Wtf is a blockchain": A Chain of Blocks (header, block data, Merkle trees, Further Reading) | Same heading | Experiment 4: Build, tamper, mine; Merkle proof explorer (recomputes the root from the proof); "How this toy chain differs from Bitcoin" note; Merkle tree diagram |
| └ Mining and Proof of Work (expanding the chain, full nodes, PoW, Sybil, Further Reading) | Same heading | Mining-work experiment (practice blocks against the expected 2^b tries); issuance chart |
| └ From a Chain to a Network (making blocks, UTXO, gossip, longest chain, Further Reading) | Same heading | Transaction lifecycle diagram; quick check |
| └ Properties of Bitcoin (decentralization, incentives, ordering, 51% attack, closing note, Further Reading) | Same heading | Experiment 5: Double-spend race (simulation); quick check |
| *(new)* Key takeaways | End of notebook | |
| *(new)* Homework | End of notebook, after Key takeaways: name and wallet, three coding tasks plus a bonus, six questions, onchain completion | Phase 3 |
| *(new)* Sources | End of notebook | |

The sidebar links to every top-level part plus Hash functions, Digital signatures, Elliptic curves, Mining, The network, Key takeaways, Homework and Sources; each link was checked to land on its heading (November 17, 2026). The Week 1 row on the curriculum overview page also lists "Introduction to Economics", but the Week 1 lesson page has no such section, so there is nothing to carry over.

**Round 3 (November 17, 2026): what sits in a collapsed section.** Everything the original page shows on its main line, and every item it marks green (tested), is on the notebook's main line. That includes SHA-256's internals, Block data, the 8 + 2 gossip peers, the Bletchley machines, the signature schemes used today, and "What does this mean?" under Hash Functions. The collapsed sections hold only:
- the scytale debate and the Vigenère cipher (Ancient Cryptography; the original also kept Vigenère in a toggle)
- browser versions (Types of Cryptography)
- the NSA side question (Hash Functions)
- the Tencent paper, marked [Not tested] as in the original, and the proof (RSA)
- the edge cases (as in the original), the point-addition formulas and secp256k1's parameters (ECC)
- quantum exposure and the 2008 history (Bitcoin intro)
- where the block number lives and how the toy chain differs (A Chain of Blocks)
- the 125-peer limit (From a Chain to a Network)
- the simulation's model (Properties of Bitcoin)
- the optional PQC and FHE topics, which the original also marks "If we have time"
