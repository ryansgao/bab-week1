# Content update log

Changes from the original Week 1 lesson (Notion page updated 2025-09-24, plus the "digital sigs" and "bitcoin" slide decks). Facts that change over time were checked in November 2026; the ones re-checked on November 17, 2026 say so in the Source column.

## Corrections

| Section | Original | Change | Source |
| :--- | :--- | :--- | :--- |
| Ancient Cryptography | Caesar cipher "famous key shift k=1", dated 100 BCE | Shift of 3 (Suetonius); dated to the 1st century BCE and labeled historical | Suetonius, *Life of Julius Caesar* 56 |
| Ancient Cryptography | Scytale dated 400 BCE and presented as an established cipher | Labeled historical; notes the accounts come from much later writers and that historians debate its use for secrecy | Kelly, "The Myth of the Skytale," *Cryptologia* 22(3), 1998 |
| Ancient Cryptography | Caesar "how it's broken" toggle empty; frequency-analysis text sat under Enigma | Moved back under Caesar; added brute force (25 keys) | |
| Ancient Cryptography | Bletchley "drove the invention of modern computation (Turing machines)" | Turing machines date from Turing's 1936 paper; Bletchley built the Bombe and Colossus (1944) | [Crypto Museum](https://www.cryptomuseum.com/crypto/enigma/) |
| Types of Cryptography | "Advanced Encryption Systems"; "every single one of your computers" has AES hardware | Advanced Encryption Standard; "most modern laptop and phone processors" | [FIPS 197](https://csrc.nist.gov/pubs/fips/197/final) |
| Types of Cryptography | Card number given as an example of asymmetric encryption | In TLS, public-key crypto sets up a session key; the card number is encrypted symmetrically | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) |
| Types of Cryptography | Key exchange explained with an unsourced Fortnite claim | Replaced with HTTPS / TLS 1.3, plus a sequence diagram | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) |
| Post-quantum | CRYSTALS-Kyber / Dilithium names; "CRYSTALS uses Module-LWE, Module-LWR" | Standard names ML-KEM, ML-DSA, SLH-DSA (Aug 2024); Kyber uses Module-LWE, Dilithium Module-LWE and Module-SIS (LWR is Saber's assumption) | [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [204](https://csrc.nist.gov/pubs/fips/204/final), [205](https://csrc.nist.gov/pubs/fips/205/final) |
| FHE | "Encrypt(A) + Encrypt(B) = Encrypt(A + B)" | Written as Dec(Enc(a) ⊕ Enc(b)) = a + b, with a note that encryption is randomized | |
| Hash Functions | "Some libraries have auto-salting" listed under the deterministic property | Hash functions are deterministic; salting moved to password storage | |
| Hash Functions | Example output "8872159485424383976" for "Hello!" | Real SHA-256 digest, computed live | |
| Hash Functions | `hash(password + fixed_secret_constant)` called "BETTER" | Labeled "better, but still weak"; recommends a per-user salt and a slow KDF (Argon2id, scrypt, bcrypt) | [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) |
| Hash Functions | Rainbow tables used to explain MD5's collision break | Separated: collisions (2004) vs. rainbow tables against unsalted fast hashes | |
| Hash Functions | "The algorithm was actually first published by the NSA" under SHA2/3; NSA backdoor link placed there | True for SHA-2, false for SHA-3 (Keccak, public competition). The linked article is about Dual_EC_DRBG, a random number generator, which NIST told users to stop using in 2013 and dropped from SP 800-90A in 2015 (Rev. 1) | [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), [FIPS 202](https://csrc.nist.gov/pubs/fips/202/final) |
| Hash Functions | Pad "so that its length is a multiple of 64" | SHA-256 pads to a multiple of 512 bits: a 1 bit, zeros, then the 64-bit length | [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) |
| RSA | Heading "Rivest-Shamir-Adlema" | Adleman | |
| RSA | Textbook RSA with no warning | Notes it's deterministic and malleable (both shown live) and that real systems use OAEP/PSS | [arXiv 1802.03367](https://arxiv.org/abs/1802.03367) |
| RSA | "Quantum computing destroys the whole 'factoring is hard' argument", undated | Dated resource estimates and NIST timeline | [Gidney 2025](https://arxiv.org/abs/2505.15917), [Feb 2026 preprint](https://arxiv.org/abs/2602.11457), [NIST IR 8547](https://csrc.nist.gov/news/2026/transition-to-pqc-standards-nist-ir-8547) |
| RSA proof | Fermat's little theorem called Euler's theorem; gcd(m, p) = 1 assumed | Named correctly; the p ∣ m case handled; CRT step made explicit | [CS70 Note 7](https://www.eecs70.org/assets/pdf/notes/n7.pdf) |
| Digital Signatures | Signing taught as "encrypt with your private key"; verification checks `hash(m) == S^e` (no mod N) | Marked as textbook-RSA-only intuition; verification is S^e mod N = H(m) mod N | [Nakov, RSA Signatures](https://cryptobook.nakov.com/digital-signatures/rsa-signatures) |
| Digital Signatures | "ECDSA is the preferred method of digital signing today" | ECDSA is widely used; Bitcoin also uses Schnorr since Taproot (Nov 2021); Ed25519 common elsewhere | [BIP 340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) |
| ECC | "Uses mathematical process to merge two distinct keys, then uses output to encrypt and decrypt" | ECC is a family used for key agreement and signatures; Bitcoin uses it only for signatures | |
| ECC | A line "must intersect the curve at most one other point"; "A dot B"; "dotted with itself" | Exactly one other point (counting tangents and the point at infinity); point addition and scalar multiplication | [Cloudflare ECC primer](https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/) |
| ECC | "Difficulty in factoring increases more slowly"; RSA key sizes undated | Explains sub-exponential vs. exponential attacks; key-size equivalences cited | [NIST SP 800-57 Pt 1 Rev 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) |
| Chain of Blocks | Header = previous hash, nonce, "block number or block time", Merkle root | Six fields in 80 bytes (version, previous hash, Merkle root, time, nBits, nonce); no height in the header; double SHA-256 | [Bitcoin developer reference](https://developer.bitcoin.org/reference/block_chain.html), [BIP 34](https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki) |
| Mining | "All hashes must begin with 4 zeros" (notes) vs. "8 zeros" (deck) | Real rule is hash ≤ target, retargeted every 2,016 blocks; leading zeros labeled as a simplification | [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf) |
| Mining | "Being a full node is necessary to mine … but it is not a requirement" | Pool operators run full nodes; individual hashers usually don't | |
| Network | "Nodes consider the longest chain to be the correct chain" | Most cumulative work; "longest" kept as labeled intuition | [Bitcoin developer reference](https://developer.bitcoin.org/reference/block_chain.html) |
| Network | "Each node gossips to 8 other nodes on average" | Bitcoin Core default: 8 outbound full-relay + 2 block-relay-only, up to 125 total; gossip carries transactions too | [Bitcoin Core net.h](https://github.com/bitcoin/bitcoin/blob/master/src/net.h) |
| Properties of Bitcoin | 51% attack "costs around 1M/hr*" (undated, blog source) | Removed; explains what the cost depends on | |
| Properties of Bitcoin | "A 51% attacker can't broadcast invalid transactions" | Lists what a majority attacker can (reorg, double-spend, censor) and can't (steal, inflate, change rules) do; adds that a minority attacker can sometimes double-spend | [Bitcoin whitepaper §11](https://bitcoin.org/bitcoin.pdf) |
| bitcoin deck | Invented, profane quote attributed to Satoshi | Replaced with the genesis block's embedded headline (Jan 3, 2009), labeled historical | [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf) |
| bitcoin deck | Halving "every 4 years to account for inflation"; "3.125 BTC = $200K–$300K"; full node "600GB" | Every 210,000 blocks on a fixed schedule; 3.125 BTC since April 2024 (block 840,000); dollar figure dropped; node size given as "several hundred gigabytes as of 2026" | [Mastering Bitcoin 3e](https://github.com/bitcoinbook/bitcoinbook) |
| digital sigs deck | Last slide applies the public key to the hash and compares | Verification applies the public key to the signature and compares with the hash | |

## Additions

| Section | Addition | Source |
| :--- | :--- | :--- |
| Top | Learning objectives, how-to-use note, prerequisites | |
| A Brief Overview | Dated timeline table (replaces the overview images) | Various, cited in-line |
| Types of Cryptography | Hybrid post-quantum key exchange on by default: Chrome from version 124 (April 2024, X25519Kyber768), moving to the standardized X25519MLKEM768 in 131; desktop Firefox 132 (late 2024); Safari 26 | [Google Security Blog, Sep 13 2024](https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html); [Cloudflare browser support table](https://developers.cloudflare.com/ssl/post-quantum-cryptography/pqc-support/) (checked Nov 17, 2026) |
| Post-quantum | Standards table; HQC selected (Mar 2025); HQC and FALCON-derived (FN-DSA) standards still being written as of Oct 2026; NIST IR 8547 timeline (final Oct 27, 2026: all quantum-vulnerable public-key algorithms deprecated after 2030, disallowed after 2035); resource estimates | [NIST HQC](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption); [NIST IR 8547 final](https://csrc.nist.gov/pubs/ir/8547/final), sections 2.1 and 4, Tables 2 and 4 (read Nov 17, 2026) |
| FHE | Link to textbook RSA as a partially homomorphic scheme; Gentry 2009 | |
| Hash Functions | Avalanche effect; SHA-256's initial values; Merkle–Damgård diagram; Keccak-256 vs SHA3-256; Grover's effect on hashes | [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) |
| RSA | Extended Euclidean algorithm worked live; trial-division chart; the public factoring record as of Nov 2026, RSA-896 (896 bits, Sep 19, 2026, up to 2,048 GPUs for about 10 days). The first draft said RSA-250 (829 bits, 2020), which was overtaken in September 2026 | [Wikipedia, RSA numbers](https://en.wikipedia.org/wiki/RSA_numbers) (checked Nov 17, 2026) |
| ECC | Addition formulas; double-and-add; finite fields; secp256k1 parameters; quantum exposure and BIP 360 (draft, Feb 2026) | [SEC 2](https://www.secg.org/sec2-v2.pdf), [BIP 360](https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki) |
| Bitcoin intro | The deck's "why money can't be a file" motivation, three problems, definitions | bitcoin deck |
| Chain of Blocks | Header table; Merkle proof size; light clients (from the deck) | |
| Mining | Difficulty retargeting; pools; block subsidy and fees; issuance chart with the exact supply cap | [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf) |
| Network | Worked UTXO example; mempool; stale blocks (Tokyo/Berkeley example from the deck); transaction lifecycle diagram | |
| Properties of Bitcoin | Confirmations and double-spend odds; simulation with exact and whitepaper formulas | [Rosenfeld 2014](https://arxiv.org/abs/1402.2009) |
| End | Key takeaways; full sources list | |

## Review pass (November 17, 2026)

Changes made after the first full draft, on top of the tables above.

| Section | Change | Source |
| :--- | :--- | :--- |
| A Brief Overview | SHA-2 dated 2002 (FIPS 180-2), not 2001; AES stays 2001 | [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) (history section) |
| Hash Functions | Avalanche explanation corrected: the compression rounds do the mixing, the chaining carries it forward | [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) |
| ECC playground | "Adding two points on the oval *can* land on the other branch" changed to *always* (checked numerically for a = −3, b = 1) | |
| First lecture! Woooo | Restored more of the original's voice and both original sub-labels (Building your cohort 🤝, Crypto / blockchain imposter syndrome 👻) | Notion original |
| Mining and Proof of Work | "Specialized chips that compute trillions of hashes per second" made specific: one modern ASIC machine does hundreds of trillions | |
| From a Chain to a Network | "Fee per byte" replaced by fee for the block space a transaction takes (Bitcoin measures it in virtual bytes since SegWit) | |

## Round 1 fixes after two outside reviews (November 17, 2026)

| Section | Change | Source |
| :--- | :--- | :--- |
| Properties of Bitcoin (simulation) | The draft said the whitepaper formula "slightly underestimates" the risk. It underestimates by about half for small attackers (q = 10%, z = 5: 0.09% vs 0.18% exact) and overestimates once q passes roughly 35 to 40%. For a 10% attacker the whitepaper table says 5 confirmations reach 0.1% and the exact formula says 6; the notebook now says both | [Bitcoin whitepaper §11](https://bitcoin.org/bitcoin.pdf), [Rosenfeld 2014](https://arxiv.org/abs/1402.2009); checked by script |
| Properties of Bitcoin (simulation) | The 50-blocks-behind give-up rule was called a "tiny" effect. It's invisible below about q = 45% but lowers success by about 1 percentage point at 49%; now stated | gambler's-ruin calculation |
| Properties of Bitcoin (simulation) | "Nothing special happens at 51%… above 50% the picture flips" read as a contradiction; reworded around 50% | |
| A Chain of Blocks (toy chain) | Added a note on how the toy chain differs from Bitcoin (no signature or balance checks, text header, per-block difficulty, fixed timestamps). Coinbase lines now carry their height, so no two blocks share a transaction hash (the duplicate-txid problem BIP 34 fixed) | [BIP 34](https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki) |
| Types of Cryptography | Chrome's hybrid default dated to version 124 (April 2024); 131 was the move to ML-KEM | [Google Security Blog, Sep 13 2024](https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html) |
| Hash Functions | Dual_EC_DRBG: NIST warned against it in 2013 and dropped it from SP 800-90A in 2015 (the draft said "withdrew in 2014") | [NIST SP 800-90A Rev. 1](https://csrc.nist.gov/pubs/sp/800/90/a/r1/final) |
| Hash Functions | Correction notes that argued with the original lesson (salting vs determinism, rainbow tables vs collisions, "not the NSA", "about that NSA story") removed from the lesson text; the corrections themselves are in the table above | |
| Elliptic Curve Cryptography | The find-k challenge now starts on a generator of the largest order (the default on p = 223 had order 3, which made the secret always 2) | |

## Round 2: teaching pass (November 17, 2026)

No facts changed. The structure follows the original lesson more closely: nested bullets, a problem before each idea, and small worked numbers that can be checked by hand. The worked numbers were all checked by script:

- RSA with p = 61, q = 53, e = 17: d = 2753 and 65 → 2790 → 65.
- The RSA signature on "Pay Bob 5 dollars": H = 1458, S = 697, and 697^17 mod 3233 = 1458.
- Doubling G = (1, 5) on y² = x³ + 7 mod 17 gives (2, 10).
- 100A takes 8 steps.
- The supply cap: 50 × 210,000 × 2 = 21 million.
- 2^12 = 4,096 tries per block at 12 bits.
- The chain-weight example: 1,000 vs 1,800 units of work.

| Section | Change | Source |
| :--- | :--- | :--- |
| Bitcoin intro | Rebuilt on the bitcoin deck's chain: the resume PDF, then the bank, then "we all have to become the bank", then three numbered problems. Each later section says which problem it solves. The deck's "prints more money behind the scenes" is back in the list of bank failures | bitcoin deck |
| Digital Signatures | Rebuilt on the digital-sigs deck's chain: encryption alone, then "is that it?", then a forged sender, then signatures, then hash-then-sign | digital sigs deck |
| FHE | The original's depth signal is back in softer form: "one example of each is enough" (the original said "just memorize one of these") | Notion original |

## Round 3 fixes (November 17, 2026)

| Section | Change | Source |
| :--- | :--- | :--- |
| Properties of Bitcoin | The 0.06% figure (q = 10%, z = 6) is now attributed to the exact formula, with the whitepaper's 0.024% beside it. The draft's wording made it look like a whitepaper number | [Rosenfeld 2014](https://arxiv.org/abs/1402.2009), [whitepaper §11](https://bitcoin.org/bitcoin.pdf), checked by script |
| Bitcoin intro | "In 2008 the global banking system had just collapsed" changed to "had nearly collapsed" | |
| Hash Functions | The original's tested "What does this mean?" restored to the main line | Notion original (green block) |

## Removed

- Personal references: both "DM teo" lines (his Vigenère notebook under the Caesar cipher, his Tencent-attack notebook under RSA), and the "just memorize one of these" lines, which don't fit a self-paced resource.
- "Quantum cryptography" in the opening list of applications (the post-quantum section explains how it differs from post-quantum cryptography). "ZKPs" stays.
- The original's Slack screenshot and overview images (replaced by a callout and a dated timeline table).
- Not removed after all: the first draft dropped the ECC YouTube video and the bitcoin.org mining FAQ from the reading lists; round 1 put both back.
- Weak or secondary sources in Further Reading (Okta, Passwork, u.today, Investopedia), replaced with standards, the whitepaper, BIPs, and Mastering Bitcoin 3rd edition. The old Mastering Bitcoin link pointed to the 2014 edition.
