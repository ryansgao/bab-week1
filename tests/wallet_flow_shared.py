"""Pieces shared by wallet_flow.py and live_completion.py: the stand-in wallet, a saved full solution, widget helpers."""
import time

KEY = "bab-edu-week1-homework-v1"

FAKE = """
(() => {
  const listeners = {};
  const eth = {
    isMetaMask: true,
    request: async ({ method, params }) => {
      const r = await window.__walletRpc(method, JSON.stringify(params || []));
      if (r.error) { const e = new Error(r.error.message); e.code = r.error.code; throw e; }
      return r.result;
    },
    on: (ev, fn) => { (listeners[ev] = listeners[ev] || []).push(fn); },
    removeListener: () => {},
  };
  window.ethereum = eth;
})();
"""

SOLUTION = {
    "name": "Test Learner",
    "code": {
        "t1": "def sha256d(data: bytes) -> bytes:\n    return hashlib.sha256(hashlib.sha256(data).digest()).digest()\n",
        "t2": "def merkle_root(txids):\n    level = [bytes.fromhex(t)[::-1] for t in txids]\n    while len(level) > 1:\n        if len(level) % 2:\n            level.append(level[-1])\n        level = [sha256d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]\n    return level[0][::-1].hex()\n",
        "t3": "def serialize_header(version, prev_hash, merkle_root, time, bits, nonce):\n    return struct.pack('<I', version) + bytes.fromhex(prev_hash)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<III', time, bits, nonce)\n\ndef block_hash(header):\n    return sha256d(header)[::-1].hex()\n",
    },
    "answers": {
        "q1": "Preimage resistance",
        "q2": "A trapdoor is easy to compute one way and hard to reverse unless you hold a secret; a hash has no secret that reverses it, for anyone",
        "q3d": 27, "q3c": 8, "q4": "About 16 times as many", "q5": 4,
        "q6": "The one with more total work, because rewriting it costs the most hashing",
    },
}

_FIND = """const out = [];
      const walk = (root) => { root.querySelectorAll('*').forEach(e => { if (e.shadowRoot) walk(e.shadowRoot);
        if (e.classList && e.classList.contains('box') && e.querySelector('.status')) out.push(e); }); };
      walk(document);"""


def wallet_text(pg, n):
    """Status of the n-th wallet widget (0 = connect, 1 = record) in a page or frame, through shadow roots."""
    return pg.evaluate("""(n) => {
      """ + _FIND + """
      const b = out[n]; if (!b) return null;
      const btns = Array.from(b.querySelectorAll('button')).map(x => ({t: x.textContent, d: x.disabled, v: x.style.display !== 'none'}));
      return { status: b.querySelector('.status').innerText, detail: b.querySelector('.detail').innerText, btns };
    }""", n)


def click_wallet(pg, n, label):
    pg.evaluate("""([n, label]) => {
      """ + _FIND + """
      Array.from(out[n].querySelectorAll('button')).find(b => b.textContent.startsWith(label)).click();
    }""", [n, label])


def wait_until(fn, timeout=60, step=0.5):
    end = time.time() + timeout
    while time.time() < end:
        try:
            v = fn()
            if v:
                return v
        except Exception:
            pass
        time.sleep(step)
    return None
