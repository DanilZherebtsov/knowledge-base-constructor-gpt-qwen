#!/usr/bin/env python3
"""UserPromptSubmit hook: one service line before every agent turn, at the end of
the context, where it is actually followed. Tested: consent and the reminder limit
leak when they live only in QWEN.md.

Qwen Code wraps `hookSpecificOutput.additionalContext` into its own message part,
so the line stays distinguishable from text the human wrote.

Always exits 0 — a reminder must never block a turn.
"""
import json
import sys

LINE = (
    "[consent check] Write to the wiki only after the human explicitly says yes to your offer "
    "to save; an on-topic reply is not a yes. Project memory is the wiki/ folder via ingest — "
    "not the save_memory tool, which writes into the global ~/.qwen/QWEN.md and therefore "
    "outranks the wiki instead of caching it. Do not use save_memory for project knowledge. "
    "An unanswered offer is not a refusal, but do not repeat it every turn: at most one reminder "
    "per chat, in the reply that wraps up, with no reproach; you may extend a pending offer only "
    "when new facts appear. Routine code changes you just made are not worth offering."
)

try:
    if not sys.stdin.isatty():
        sys.stdin.read()
except Exception:
    pass

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": LINE,
    }
}))
