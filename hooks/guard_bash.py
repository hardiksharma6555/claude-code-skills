#!/usr/bin/env python3
"""PreToolUse guard for Bash: returns permissionDecision "ask" (never deny).

Rules (each one started as a real mistake and became a hook):
  1. git commit / git push in an Overleaf clone (remote on git.overleaf.com,
     or a dir named overleaf*), or a push to a git.overleaf.com URL.
     A paper repo should never change without the human saying yes.
  2. Local model training / inference not wrapped in ssh.
     Models run on the GPU server, not on the laptop.
  3. pdflatex that resolves to a broken Anaconda binary.
     Use the system TeX install instead (edit GOOD_PDFLATEX for your machine).
Fails open: any error -> exit 0 with no output (normal permission flow).
"""
import json
import os
import re
import shlex
import shutil
import subprocess
import sys

SEP = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")
TRAIN_SCRIPT = re.compile(r"(^|[/_\-])(train|training|finetune|fine_tune|infer|inference|predict)([_\-.]|$)", re.I)
LAUNCHERS = {"torchrun", "deepspeed"}
PY_C_MODEL = re.compile(r"from_pretrained|\.generate\(|\.fit\(|model\.train\(|torch\.load\(", re.I)
GOOD_PDFLATEX = "/Library/TeX/texbin/pdflatex"


def out(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


OPS = {"&&", "||", ";", "|", "|&", "&", ";;"}


def segments(cmd):
    """Split into simple commands, respecting quotes (so `;` inside python -c stays)."""
    try:
        lx = shlex.shlex(cmd.replace("\n", " ; "), posix=True, punctuation_chars=True)
        lx.whitespace_split = True
        cur, res = [], []
        for tok in lx:
            if tok in OPS or set(tok) <= set(";&|"):
                if cur:
                    res.append(cur)
                cur = []
            elif tok in ("(", ")", "{", "}"):
                continue
            else:
                cur.append(tok)
        if cur:
            res.append(cur)
        return res
    except ValueError:
        return [s.split() for s in SEP.split(cmd) if s.strip()]


def toks(t):
    t = list(t)
    while t and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t[0]):  # strip VAR=val
        t = t[1:]
    while t and t[0] in ("env", "nohup", "setsid", "time", "exec", "sudo"):
        t = t[1:]
    return t


def is_overleaf_repo(d):
    d = os.path.expanduser(d)
    if not os.path.isdir(d):
        return False
    try:
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=3).stdout.strip()
    except Exception:
        top = ""
    if "overleaf" in os.path.basename(top or d).lower():
        return True
    try:
        r = subprocess.run(["git", "-C", d, "remote", "-v"], capture_output=True, text=True, timeout=3)
        return "git.overleaf.com" in r.stdout
    except Exception:
        return False


def main():
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        return
    cmd = (data.get("tool_input") or {}).get("command", "") or ""
    cwd = data.get("cwd") or os.getcwd()
    remote = bool(re.search(r"(^|[\s;&|(])(ssh|scp|rsync)\s", cmd))
    d = cwd
    for raw in segments(cmd):
        t = toks(raw)
        seg = " ".join(raw)
        if not t:
            continue
        prog = os.path.basename(t[0])
        if prog == "cd" and len(t) > 1:
            nd = os.path.expanduser(t[1])
            d = nd if os.path.isabs(nd) else os.path.join(d, nd)
            continue

        # 1. Overleaf commit/push
        if prog == "git":
            gd, i = d, 1
            while i < len(t) and t[i].startswith("-"):
                if t[i] == "-C" and i + 1 < len(t):
                    p = os.path.expanduser(t[i + 1])
                    gd = p if os.path.isabs(p) else os.path.join(gd, p)
                    i += 2
                elif t[i] == "-c" and i + 1 < len(t):
                    i += 2
                else:
                    i += 1
            sub = t[i] if i < len(t) else ""
            if sub in ("commit", "push"):
                if "git.overleaf.com" in seg or is_overleaf_repo(gd):
                    out(f"Overleaf rule: git {sub} in an Overleaf clone ({gd}). "
                        "Describe the exact change to the user and get a yes before committing or pushing.")

        # 3. Anaconda pdflatex
        if prog == "pdflatex" and not remote:
            path = t[0] if "/" in t[0] else (shutil.which("pdflatex") or "")
            if "anaconda" in path or "conda" in path:
                out(f"LaTeX rule: '{t[0]}' resolves to {path}, which is broken (missing pdflatex.fmt). "
                    f"Use {GOOD_PDFLATEX} instead.")

        # 2. Local training / inference
        if remote:
            continue
        hit = None
        if prog in LAUNCHERS:
            hit = prog
        elif prog == "accelerate" and len(t) > 1 and t[1] == "launch":
            hit = "accelerate launch"
        elif re.match(r"^python(\d(\.\d+)?)?$", prog):
            rest = t[1:]
            j = 0
            while j < len(rest) and rest[j].startswith("-") and rest[j] not in ("-m", "-c"):
                j += 1
            if j < len(rest) and rest[j] == "-m" and j + 1 < len(rest):
                mod = rest[j + 1]
                if mod.startswith("torch.distributed") or TRAIN_SCRIPT.search(mod.split(".")[-1]):
                    hit = f"python -m {mod}"
            elif j < len(rest) and rest[j] == "-c" and j + 1 < len(rest):
                if PY_C_MODEL.search(rest[j + 1]):
                    hit = "python -c (model load/generate)"
            elif j < len(rest):
                script = os.path.basename(rest[j])
                if script.endswith(".py") and TRAIN_SCRIPT.search(script[:-3]):
                    hit = f"python {script}"
        if hit:
            out(f"GPU rule: '{hit}' looks like model training/inference on this machine. "
                "Models run on the GPU server only (via ssh). Approve only if this is not a model run.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        pass
    sys.exit(0)
