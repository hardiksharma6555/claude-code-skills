# remote-server-ssh

A Claude Code skill with safe rules for running commands on a shared remote GPU server through one SSH ControlMaster socket, especially when several agents or sub-agents share it.

It prevents three failures seen in practice:

- wait loops that retry after the socket dies and flood the server with failed logins;
- a socket that reports "Master running" but hangs every command;
- "Session open refused by peer" when too many agents share one master, followed by a silent fallback to a direct login.

## Install

```
cp -R skills/remote-server-ssh ~/.claude/skills/remote-server-ssh
chmod +x ~/.claude/skills/remote-server-ssh/scripts/rsh
```

Optionally put `scripts/rsh` on your PATH.

## Contents

- `SKILL.md`: the rules, with correct and incorrect wait-loop examples.
- `scripts/rsh`: a wrapper that checks the socket, allows one call at a time per socket, disables every login method so a fallback cannot cause a failed login, applies a hard timeout, and stops with the reopen commands on any failure.

## Use

Open the master yourself once (it needs your password):

```
ssh -M -S ~/.ssh/cm-myhost -o ControlPersist=48h -fN me@myhost
```

Then agents run:

```
RSH_USER=me rsh myhost 'nvidia-smi'
```
