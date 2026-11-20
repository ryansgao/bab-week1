"""Offline test of the homework's coding checks: right answers pass, each common mistake gets its named message.
usage: python homework_checks.py path/to/week1.py"""
import ast, hashlib, sys, textwrap
src = open(sys.argv[1]).read()
tree = ast.parse(src)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and "HW_BLOCK = {" in ast.get_source_segment(src, n))
body = textwrap.dedent("\n".join(ast.get_source_segment(src, s) for s in fn.body[:-1]))
ns = {"hashlib": hashlib}; exec(body, ns)
run = ns["hw_run"]
fails = []
def expect(label, code, check, ok, contains="", extra=None):
    env, err = run(code, extra)
    got_ok, msgs = (False, [err]) if err else ns[check](env)
    text = " ".join(msgs)
    if got_ok != ok or contains not in text:
        fails.append(f"{label}: ok={got_ok} msgs={text[:200]}")
    else:
        print("ok  ", label, "|", text[:110])

T1 = "def sha256d(data):\n    return hashlib.sha256(hashlib.sha256(data).digest()).digest()\n"
expect("t1 right", T1, "hw_check_sha256d", True)
expect("t1 starter", 'def sha256d(data: bytes) -> bytes:\n    return b""\n', "hw_check_sha256d", False, "placeholder")
expect("t1 single", "def sha256d(d):\n    return hashlib.sha256(d).digest()\n", "hw_check_sha256d", False, "single SHA-256")
expect("t1 hex", "def sha256d(d):\n    return hashlib.sha256(hashlib.sha256(d).digest()).hexdigest()\n", "hw_check_sha256d", False, "wrong type")
expect("t1 hexchain", "def sha256d(d):\n    return hashlib.sha256(hashlib.sha256(d).hexdigest().encode()).digest()\n", "hw_check_sha256d", False, "raw bytes")
expect("t1 syntax", "def sha256d(d)\n  return 1", "hw_check_sha256d", False, "SyntaxError")
expect("t1 raises", "def sha256d(d):\n    return 1/0\n", "hw_check_sha256d", False, "line 2")
sd = {"sha256d": lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()}
M = """def merkle_root(txids):
    level = [bytes.fromhex(t)[::-1] for t in txids]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [sha256d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0][::-1].hex()
"""
expect("t2 right", M, "hw_check_merkle", True, extra=sd)
expect("t2 no out-reverse", M.replace("level[0][::-1].hex()", "level[0].hex()"), "hw_check_merkle", False, "byte-reversed", sd)
expect("t2 no reversal", M.replace("bytes.fromhex(t)[::-1]", "bytes.fromhex(t)").replace("level[0][::-1].hex()", "level[0].hex()"), "hw_check_merkle", False, "display order", sd)
expect("t2 single sha", M.replace("sha256d(level[i]", "hashlib.sha256(level[i]").replace("level[i + 1])", "level[i + 1]).digest()"), "hw_check_merkle", False, "single SHA-256", sd)
expect("t2 no dup", M.replace("level.append(level[-1])", "level.pop()"), "hw_check_merkle", False, "dropped", sd)
expect("t2 starter", 'def merkle_root(txids):\n    return ""\n', "hw_check_merkle", False, "one-item", sd)
H = """def serialize_header(version, prev_hash, merkle_root, time, bits, nonce):
    return struct.pack('<I', version) + bytes.fromhex(prev_hash)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<III', time, bits, nonce)

def block_hash(header):
    return sha256d(header)[::-1].hex()
"""
expect("t3 right", H, "hw_check_header", True, extra=sd)
expect("t3 big-endian", H.replace("struct.pack('<I', version)", "struct.pack('>I', version)"), "hw_check_header", False, "version", sd)
expect("t3 prev not reversed", H.replace("bytes.fromhex(prev_hash)[::-1]", "bytes.fromhex(prev_hash)"), "hw_check_header", False, "byte-reversed", sd)
expect("t3 hex text", H.replace("bytes.fromhex(prev_hash)[::-1]", "prev_hash.encode()"), "hw_check_header", False, "hex text", sd)
expect("t3 hash not reversed", H.replace("sha256d(header)[::-1].hex()", "sha256d(header).hex()"), "hw_check_header", False, "byte order", sd)
expect("t3 order swap", H.replace("struct.pack('<III', time, bits, nonce)", "struct.pack('<III', time, nonce, bits)"), "hw_check_header", False, "different field", sd)
B = "def meets_target(h, bits):\n    t = (bits & 0xFFFFFF) * 256 ** ((bits >> 24) - 3)\n    return int(h, 16) <= t\n"
expect("bonus right", B, "hw_check_target", True)
expect("bonus wrong", "def meets_target(h, bits):\n    return True\n", "hw_check_target", False, "Expected")
print("FAILURES:" if fails else "all checks behave", *fails, sep="\n")
sys.exit(1 if fails else 0)
