---
name: remote-server-ssh
description: Safe rules for running commands on a shared remote GPU server over one SSH ControlMaster socket, especially when several agents or sub-agents share it. Use whenever a task runs ssh, scp or rsync against a remote server, launches or polls remote jobs, writes wait/poll loops over ssh, briefs a worker that will use ssh, or when ssh shows "Permission denied", "Too many authentication failures", "Session open refused by peer", "Control socket connect ... No such file", a hang, or exit 255/142. Prevents failed-login floods, session-limit refusals and runaway retry loops.
---

# Remote server over a shared SSH socket

These rules come from real incidents on a shared university GPU server reached through one password-authenticated ControlMaster socket, with several Claude agents using it at once:

- A wait loop kept retrying after the socket died. Every retry fell through to a fresh password login and the server logged "Too many authentication failures".
- A socket answered `-O check` ("Master running") but hung on every command.
- With four workers sharing one master, the server refused new sessions ("Session open refused by peer"), most likely its per-connection session limit (sshd `MaxSessions`, default 10). ssh then silently tried a direct login, which logged failed authentications.

The goal: never cause a failed login on the server, never hang, and stop cleanly so a human can reopen the socket.

## Setup (done once by the human)

The human opens the master; agents never do, because it needs a password:

```
ssh -M -S ~/.ssh/cm-HOST -o ControlPersist=48h -fN USER@HOST
```

If it is dead or hung, the human closes and reopens it:

```
ssh -S ~/.ssh/cm-HOST -O exit USER@HOST
ssh -M -S ~/.ssh/cm-HOST -o ControlPersist=48h -fN USER@HOST
```

Tell the human these exact commands (prefixed with `!` in Claude Code). Never try to open the master yourself.

## The rules

1. **Every call goes through the socket, with logins disabled.** Write the options literally on every call; never keep them in a shell variable (zsh does not word-split variables, so ssh would silently ignore them):

   ```
   perl -e 'alarm 60; exec @ARGV' ssh -S ~/.ssh/cm-HOST -o BatchMode=yes -o ProxyCommand=false \
     -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
     -o PubkeyAuthentication=no -o GSSAPIAuthentication=no USER@HOST 'timeout 55 command'
   ```

   When the master refuses a session, ssh silently falls back to a direct connection. `-o ProxyCommand=false` makes that fallback fail locally, before anything reaches the server (the multiplexed session through the socket does not use ProxyCommand). Disabling every login method is a second guard: tested, auth options alone still opened a connection and printed "Permission denied". Or use `scripts/rsh`, which does all of this.

2. **Hard timeout on both ends.** macOS has no `timeout` binary; use `perl -e 'alarm N; exec @ARGV'` locally (exit 142 = timed out), and also wrap the remote command in `timeout N-5`. Killing only the local client can leave the remote command running in its session; enough of those fill the server's per-connection session limit and the master starts refusing new sessions.

3. **Probe before long work.** `ssh -S ... -O check USER@HOST` is not enough: a master can answer "Master running" and still hang. Run a trivial command (`echo ok`) with a short alarm first.

4. **One call in flight per agent.** Never run ssh calls in parallel or in background loops. Put multi-step work inside one remote command, or in a remote script started detached. Several agents sharing one master is the usual cause of "Session open refused".

5. **Stop on any failure. Never retry.** Treat all of these as a stop signal:
   - exit 255;
   - exit 142 (timed out);
   - "Session open refused by peer";
   - "Control socket connect ... No such file or directory";
   - "Permission denied", "Connection closed", "Connection reset".

   On any of them, stop every ssh use, kill your own local wait loops, and report to the human with the reopen commands. Do not probe again "just to check".

6. **Wait loops must exit on any non-zero status, not loop until success.** Right:

   ```
   for i in $(seq 1 30); do
     out=$(perl -e 'alarm 40; exec @ARGV' ssh -S ~/.ssh/cm-HOST -o BatchMode=yes \
       -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
       -o PubkeyAuthentication=no -o GSSAPIAuthentication=no USER@HOST \
       'test -f /path/DONE && echo done || echo wait') || { echo "SSH_FAIL rc=$?"; exit 1; }
     [ "$out" = done ] && exit 0
     sleep 120
   done
   ```

   Wrong: `until ssh ...; do sleep 60; done`. It loops forever on a dead socket and turns each retry into a login attempt.

7. **Remote jobs are detached and self-reporting.** Start long jobs with `setsid nohup ... > log 2>&1 < /dev/null &` and have them write a marker file (`DONE` with the exit code) when they finish. A dead socket then costs you nothing, and you collect results later.

   Launch them in a call of their own, with every stream redirected and nothing after the `&`: `setsid launcher.sh </dev/null >/dev/null 2>&1 &`. Check on the job in a separate short call. A detached child that still holds the session's stdout or stderr, or a `sleep`/`pgrep` placed after the launch in the same command, can keep the multiplexed channel open; the local call then times out, and the shared master can hang for every agent. The same applies to a hop to another node: `ssh node "setsid job </dev/null >/dev/null 2>&1 &"`.

8. **Briefing workers.** When you hand ssh work to a sub-agent, paste rules 1–6 into its brief and tell it to report instead of retrying. Sub-agents do not inherit your rules otherwise.

9. **Treat shared machines as shared.** Check free GPU memory before launching, pin jobs to a device, cap CPU threads (OMP/MKL/OpenBLAS to about 4 per process) when running many workers, and never delete files you did not create.

## `scripts/rsh`

A wrapper that applies rules 1–5:

```
rsh HOST_ALIAS 'command'          # uses ~/.ssh/cm-HOST_ALIAS and $RSH_USER
RSH_TIMEOUT=120 rsh myhost 'nvidia-smi'
```

It checks that the socket file exists, takes a per-socket lock so that only one call runs at a time across agents on the same machine, blocks the direct-connection fallback (`ProxyCommand=false`) and disables every login method, applies the timeout on both ends, and prints a clear STOP message with the reopen commands on any failure.
