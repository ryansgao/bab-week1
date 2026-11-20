"""End-to-end test of the homework's progress saving and onchain completion flow, in the notebook's
WebAssembly build, in headless Chromium, with a fake browser wallet backed by a local EVM (eth-tester)
running the real BabEduCompletions contract.

usage: python wallet_flow.py NOTEBOOK.py CONTRACT_JSON OUTDIR
needs: web3, eth-tester[py-evm], playwright; marimo 0.25.2 via uvx

Covers: fresh start (record button off), typed name saved and restored after reload, restore of a full
saved solution (all checks pass), no wallet installed, connect, wallet rejection (4001), success with an
explorer link, reload after success (already recorded, no second tx), a pending transaction resumed after
a reload without a second send, an onchain failure (status 0) with retry, and an already-recorded wallet.
"""
import functools
import http.server
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time

from playwright.sync_api import sync_playwright
from web3 import EthereumTesterProvider, Web3

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wallet_flow_shared import FAKE, KEY, SOLUTION, click_wallet, wait_until, wallet_text  # noqa: E402

NB, CJSON, OUT = map(pathlib.Path, sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
EXE = os.environ.get("CHROMIUM_PATH")  # optional: a specific Chromium; default is Playwright's own

# ---- local chain with the real contract
c = json.loads(CJSON.read_text())
w3 = Web3(EthereumTesterProvider())
deployer, learner, learner2, learner3 = w3.eth.accounts[:4]
tx = w3.eth.contract(abi=c["abi"], bytecode=c["bytecode"]).constructor().transact({"from": deployer})
ADDR = w3.eth.get_transaction_receipt(tx).contractAddress
K = w3.eth.contract(address=ADDR, abi=c["abi"])
print("local contract", ADDR)

# ---- notebook build pointing at it
src = NB.read_text()
src2 = re.sub(r'HW_CONTRACT = "0x[0-9a-fA-F]{40}"', f'HW_CONTRACT = "{ADDR}"', src)
assert src2 != src or ADDR in src
build = OUT / "build"
(OUT / "nb.py").write_text(src2)
subprocess.run(["uvx", "--from", "marimo==0.25.2", "marimo", "export", "html-wasm", str(OUT / "nb.py"), "-o", str(build), "--mode", "run", "-f"], check=True, capture_output=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(build))
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/"

# ---- fake wallet
wallet = {"account": learner, "connected": False, "reject": False, "hold": False, "fail": False, "sent": []}
FAKE_FAIL = "0x" + "ab" * 32


def rpc(method, params):
    p = json.loads(params)
    try:
        if method == "eth_chainId":
            return {"result": "0xaa36a7"}
        if method in ("wallet_switchEthereumChain", "wallet_addEthereumChain"):
            return {"result": None}
        if method == "eth_accounts":
            return {"result": [wallet["account"]] if wallet["connected"] else []}
        if method == "eth_requestAccounts":
            wallet["connected"] = True
            return {"result": [wallet["account"]]}
        if method == "eth_sendTransaction":
            if wallet["reject"]:
                return {"error": {"code": 4001, "message": "User rejected the request."}}
            t = p[0]
            if wallet["fail"]:
                wallet["sent"].append(FAKE_FAIL)
                return {"result": FAKE_FAIL}
            h = w3.eth.send_transaction({"from": Web3.to_checksum_address(t["from"]), "to": Web3.to_checksum_address(t["to"]), "data": t["data"]})
            wallet["sent"].append(h.to_0x_hex())
            return {"result": h.to_0x_hex()}
        if method == "eth_getTransactionReceipt":
            if p[0] == FAKE_FAIL:
                return {"result": {"status": "0x0", "transactionHash": FAKE_FAIL}}
            if wallet["hold"]:
                return {"result": None}
        if method == "eth_call":  # eth-tester insists on a sender; real nodes don't
            p[0].setdefault("from", deployer)
            if wallet["hold"]:  # a held tx is not mined yet, so the contract must still say 0
                return {"result": "0x" + "0" * 64}
        r = w3.provider.make_request(method, p)
        if "error" in r:
            return {"error": r["error"]}
        res = r["result"]
        if method == "eth_getTransactionReceipt" and res:
            res = {"status": hex(int(res["status"])) if not isinstance(res["status"], str) else res["status"]}
        if method == "eth_getBalance" and not isinstance(res, str):
            res = hex(res)
        if method == "eth_call" and not isinstance(res, str):
            res = "0x" + bytes(res).hex()
        return {"result": res}
    except Exception as e:  # surface as a wallet error
        return {"error": {"code": -32000, "message": str(e)}}


fails, log = [], []


def check(label, cond, extra=""):
    (log if cond else fails).append(f"{'ok  ' if cond else 'FAIL'} {label} {extra}")
    print(("ok   " if cond else "FAIL ") + label, extra)


def open_page(ctx, with_wallet=True):
    pg = ctx.new_page()
    pg.on("console", lambda m: m.type == "error" and log.append("console error: " + m.text[:200]))
    pg.goto(URL)
    ok = wait_until(lambda: pg.get_by_text("Step 4: Record your completion onchain").count() > 0, timeout=180)
    check("homework renders in WASM", bool(ok))
    pg.get_by_text("Step 4: Record your completion onchain").first.scroll_into_view_if_needed()
    wait_until(lambda: wallet_text(pg, 1) and wallet_text(pg, 1)["status"], timeout=30)
    return pg


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=EXE)

    # 1. no wallet installed
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    pg = open_page(ctx)
    t = wallet_text(pg, 0)
    check("no wallet: message shown", t and "No browser wallet found" in t["status"], str(t and t["status"][:80]))
    check("no wallet: record disabled", t and all(b["d"] for b in wallet_text(pg, 1)["btns"]))
    # fresh start: errors absent, record not ready
    errs = pg.evaluate("document.querySelectorAll('.marimo-error, [data-testid=\"marimo-error\"]').length")
    check("fresh start: no marimo error outputs", errs == 0, f"({errs})")
    check("fresh start: checklist unticked", pg.get_by_text("The record button turns on when every box is ticked").count() > 0)
    # type a name, reload, name restored
    box = pg.get_by_placeholder("First and last name")
    box.fill("Ada Typed"); box.press("Tab"); time.sleep(2)
    stored = pg.evaluate(f"localStorage.getItem('{KEY}')")
    check("typed name saved to localStorage", stored and "Ada Typed" in stored)
    pg.reload()
    wait_until(lambda: pg.get_by_text("Step 4: Record your completion onchain").count() > 0, timeout=180)
    wait_until(lambda: pg.get_by_placeholder("First and last name").input_value() == "Ada Typed", timeout=30)
    check("name restored after reload", pg.get_by_placeholder("First and last name").input_value() == "Ada Typed")
    check("restore banner shown", pg.get_by_text("Progress restored from this browser").count() > 0)
    pg.screenshot(path=str(OUT / "1-fresh.png"), full_page=False)
    ctx.close()

    # 2. full saved solution + wallet
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    ctx.expose_function("__walletRpc", rpc)
    ctx.add_init_script(FAKE)
    ctx.add_init_script(f"if (!localStorage.getItem('{KEY}')) localStorage.setItem('{KEY}', {json.dumps(json.dumps(SOLUTION))});")
    pg = open_page(ctx)
    ok = wait_until(lambda: pg.get_by_text("All done, Test Learner").count() > 0, timeout=60)
    check("restored solution: all checks pass", bool(ok))
    check("task 3 passes with real block hash", pg.get_by_text("exactly block 100,000's hash").count() > 0)
    t = wallet_text(pg, 0)
    check("not connected yet", t and "Not connected" in t["status"], str(t and t["status"][:60]))
    click_wallet(pg, 0, "Connect wallet")
    ok = wait_until(lambda: "Connected as" in wallet_text(pg, 0)["status"], timeout=20)
    check("connect works", bool(ok), wallet_text(pg, 0)["status"][:80])
    # record widget picks up the connection on its own (accountsChanged is not fired by the fake; a re-render or click does)
    wallet["reject"] = True
    click_wallet(pg, 1, "Record my Week 1")
    ok = wait_until(lambda: "rejected" in wallet_text(pg, 1)["detail"], timeout=20)
    check("rejection explained, nothing sent", bool(ok) and not wallet["sent"], wallet_text(pg, 1)["detail"][:80])
    check("button usable again after rejection", not [b for b in wallet_text(pg, 1)["btns"] if b["t"].startswith("Record")][0]["d"])
    wallet["reject"] = False
    click_wallet(pg, 1, "Record my Week 1")
    ok = wait_until(lambda: "recorded onchain" in wallet_text(pg, 1)["status"], timeout=40)
    t = wallet_text(pg, 1)
    check("success shown", bool(ok), t["status"][:120])
    check("explorer link to the tx", "Transaction:" in t["status"])
    check("exactly one tx sent", len(wallet["sent"]) == 1, str(wallet["sent"]))
    check("contract says recorded", K.functions.completedAt(learner, 1).call() > 0)
    check("week stored is 1", K.functions.completedAt(learner, 2).call() == 0)
    pg.screenshot(path=str(OUT / "2-recorded.png"))
    pg.reload()
    pg = pg  # same page object
    wait_until(lambda: pg.get_by_text("Step 4: Record your completion onchain").count() > 0, timeout=180)
    ok = wait_until(lambda: "recorded onchain" in (wallet_text(pg, 1) or {}).get("status", ""), timeout=40)
    check("after reload: already recorded, link kept", bool(ok) and "Transaction:" in wallet_text(pg, 1)["status"])
    check("after reload: record disabled, no second tx", [b for b in wallet_text(pg, 1)["btns"] if b["t"].startswith("Record")][0]["d"] and len(wallet["sent"]) == 1)
    ctx.close()

    # 3. pending tx survives a reload; 4. onchain failure then retry
    wallet.update(account=learner2, connected=True, sent=[], hold=True)
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    ctx.expose_function("__walletRpc", rpc)
    ctx.add_init_script(FAKE)
    ctx.add_init_script(f"if (!localStorage.getItem('{KEY}')) localStorage.setItem('{KEY}', {json.dumps(json.dumps(SOLUTION))});")
    pg = open_page(ctx)
    wait_until(lambda: pg.get_by_text("All done, Test Learner").count() > 0, timeout=60)
    click_wallet(pg, 1, "Record my Week 1")
    ok = wait_until(lambda: "Waiting for it" in wallet_text(pg, 1)["status"], timeout=20)
    check("pending shown", bool(ok), wallet_text(pg, 1)["status"][:80])
    pg.reload()
    wait_until(lambda: pg.get_by_text("Step 4: Record your completion onchain").count() > 0, timeout=180)
    ok = wait_until(lambda: "Waiting for your transaction" in (wallet_text(pg, 1) or {}).get("status", ""), timeout=40)
    check("after reload: resumes waiting on the same tx", bool(ok))
    wallet["hold"] = False
    ok = wait_until(lambda: "recorded onchain" in wallet_text(pg, 1)["status"], timeout=30)
    check("resumed tx confirms, still one send", bool(ok) and len(wallet["sent"]) == 1, str(wallet["sent"]))
    ctx.close()

    wallet.update(account=learner3, connected=True, sent=[], fail=True)
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    ctx.expose_function("__walletRpc", rpc)
    ctx.add_init_script(FAKE)
    ctx.add_init_script(f"if (!localStorage.getItem('{KEY}')) localStorage.setItem('{KEY}', {json.dumps(json.dumps(SOLUTION))});")
    pg = open_page(ctx)
    wait_until(lambda: pg.get_by_text("All done, Test Learner").count() > 0, timeout=60)
    click_wallet(pg, 1, "Record my Week 1")
    ok = wait_until(lambda: "failed onchain" in wallet_text(pg, 1)["status"], timeout=30)
    check("onchain failure explained", bool(ok), wallet_text(pg, 1)["status"][:80])
    pg.screenshot(path=str(OUT / "3-failed.png"))
    wallet["fail"] = False
    click_wallet(pg, 1, "Record my Week 1")
    ok = wait_until(lambda: "recorded onchain" in wallet_text(pg, 1)["status"], timeout=30)
    check("retry after failure succeeds", bool(ok))
    ctx.close()

    # 5. wallet that recorded elsewhere (no local tx hash): already recorded, nothing sent
    wallet.update(account=learner, connected=True, sent=[])
    ctx = br.new_context(viewport={"width": 390, "height": 844})
    ctx.expose_function("__walletRpc", rpc)
    ctx.add_init_script(FAKE)
    pg = open_page(ctx)
    ok = wait_until(lambda: "recorded onchain" in wallet_text(pg, 1)["status"], timeout=30)
    check("already-recorded wallet detected from chain", bool(ok) and "Etherscan" in wallet_text(pg, 1)["status"])
    check("nothing sent", not wallet["sent"])
    pg.screenshot(path=str(OUT / "4-phone-already.png"))
    ctx.close()
    br.close()

srv.shutdown()
(OUT / "result.txt").write_text("\n".join(log + fails))
print(f"\n{len(fails)} failures")
sys.exit(1 if fails else 0)
