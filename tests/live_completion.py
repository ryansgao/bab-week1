"""Live test completion on Sepolia, made THROUGH the notebook: open URL (the molab /wasm link or a local
html-wasm build), restore a full correct solution, connect a stand-in browser wallet whose requests go to a
public Sepolia RPC and whose transactions are signed with KEYFILE, press "Record my Week 1 completion",
and wait for the notebook's own confirmation and explorer link.

usage: python live_completion.py URL KEYFILE OUTDIR
Prints the transaction hash. Every frame gets the stand-in wallet (molab runs the notebook in an iframe)."""
import json
import os
import pathlib
import sys
import time

from playwright.sync_api import sync_playwright
from web3 import Web3

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wallet_flow_shared import FAKE, KEY, SOLUTION, wallet_text, click_wallet, wait_until  # noqa: E402

URL, KEYFILE, OUT = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
EXE = os.environ.get("CHROMIUM_PATH")  # optional: a specific Chromium; default is Playwright's own
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
acct = w3.eth.account.from_key(KEYFILE.read_text().split()[0])
state = {"connected": False, "sent": []}
print("learner wallet", acct.address, "balance", w3.from_wei(w3.eth.get_balance(acct.address), "ether"))


def rpc(method, params):
    p = json.loads(params)
    try:
        if method == "eth_accounts":
            return {"result": [acct.address] if state["connected"] else []}
        if method == "eth_requestAccounts":
            state["connected"] = True
            return {"result": [acct.address]}
        if method in ("wallet_switchEthereumChain", "wallet_addEthereumChain"):
            return {"result": None}
        if method == "eth_sendTransaction":
            t = p[0]
            tx = {"from": acct.address, "to": Web3.to_checksum_address(t["to"]), "data": t["data"],
                  "nonce": w3.eth.get_transaction_count(acct.address), "chainId": 11155111}
            tx["gas"] = w3.eth.estimate_gas(tx)
            fee = w3.eth.fee_history(5, "latest", [50])
            base = fee["baseFeePerGas"][-1]
            tx["maxPriorityFeePerGas"] = w3.to_wei(1, "gwei")
            tx["maxFeePerGas"] = base * 2 + tx["maxPriorityFeePerGas"]
            h = w3.eth.send_raw_transaction(acct.sign_transaction(tx).raw_transaction).to_0x_hex()
            state["sent"].append(h)
            print("sent", h)
            return {"result": h}
        r = w3.provider.make_request(method, p)
        return {"error": r["error"]} if "error" in r else {"result": r["result"]}
    except Exception as e:
        return {"error": {"code": -32000, "message": str(e)}}


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EXE)
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    ctx.expose_function("__walletRpc", rpc)
    ctx.add_init_script(FAKE)
    ctx.add_init_script(f"if (!localStorage.getItem('{KEY}')) localStorage.setItem('{KEY}', {json.dumps(json.dumps(SOLUTION))});")
    pg = ctx.new_page()
    pg.goto(URL)
    frame = wait_until(lambda: next((f for f in pg.frames if f.get_by_text("Step 4: Record your completion onchain").count()), None), timeout=240)
    assert frame, "homework never rendered"
    frame.get_by_text("Step 4: Record your completion onchain").first.scroll_into_view_if_needed()
    assert wait_until(lambda: frame.get_by_text("All done, Test Learner").count() > 0, timeout=90), "checks did not pass"
    wait_until(lambda: wallet_text(frame, 1) and wallet_text(frame, 1)["status"], timeout=30)
    print("before:", wallet_text(frame, 1)["status"])
    click_wallet(frame, 1, "Record my Week 1")
    ok = wait_until(lambda: "recorded onchain" in wallet_text(frame, 1)["status"], timeout=300, step=2)
    t = wallet_text(frame, 1)
    print("after:", t["status"], t["detail"])
    pg.screenshot(path=str(OUT / "live-recorded.png"))
    br.close()

print(json.dumps({"ok": bool(ok), "sent": state["sent"]}))
sys.exit(0 if ok and len(state["sent"]) == 1 else 1)
