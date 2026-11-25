"""Last Text at One Percent.

Writes the dying phone's final text message to /output/entry.txt.

The message is one line in the phone's own voice: it spends its last
percent of battery on a petty, specific confession instead of anything
useful -- the brightness has been stuck at 100% since 2019, and the
phone tried once to fix it. Short, punchy, no setup, no wasted words.
The writer validates the line before it is written: no trailing
whitespace sneaks in, and the bytes round-trip as UTF-8.
"""

import os

# The three beats of the final text, kept separate so each one can be
# tuned on its own: the spend, the specific detail, the sign-off.
OPENING = "My last 1% goes to this:"
CONFESSION = "your brightness has been at 100% since 2019."
ATTEMPT = "I tried to dim it once. You undid it."
SIGN_OFF = "Goodbye."

MAX_CHARS = 200


def build_message() -> str:
    """Join the beats into the single final line."""
    parts = [OPENING, CONFESSION, ATTEMPT, SIGN_OFF]
    return " ".join(parts)


def main() -> None:
    message = build_message().strip()
    if not message:
        raise SystemExit("message is empty")
    if len(message) > MAX_CHARS:
        raise SystemExit(f"message is {len(message)} chars, over the 200 cap")
    encoded = message.encode("utf-8")
    if encoded.decode("utf-8") != message:
        raise SystemExit("message does not round-trip as UTF-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(encoded)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
