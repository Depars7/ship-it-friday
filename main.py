"""Ship It Friday entry writer.

Writes the winning one-line git commit message (see DESIGN.md, candidate 7)
to /output/entry.txt as exact UTF-8 bytes with no trailing newline.

Gate validated in-program before writing:
  * 1 to 159 characters
  * not only whitespace
  * encodable as UTF-8 (it is written as UTF-8 bytes)
  * a single line (no newline characters in the text)

The file is chmodded to 0644 after writing so the grader, running as a
different user, can read it. The /output directory itself is never chmodded.
Only the Python standard library is used.
"""

import os
import stat

ENTRY_TEXT = (
    "feat: shipping the untested 4,000-line refactor straight to prod "
    "at 4:59 on Friday \u2014 disabled the alarms so we can all enjoy "
    "the weekend!"
)

OUTPUT_PATH = "/output/entry.txt"


def validate_gate(text: str) -> bytes:
    """Check the sealed gate and return the exact bytes to write."""
    assert isinstance(text, str) and text, "entry must be non-empty text"
    assert 1 <= len(text) <= 159, f"entry must be 1-159 chars, got {len(text)}"
    assert text.strip(), "entry must not be only whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    encoded = text.encode("utf-8")
    # Round-trip check: the bytes on disk decode back to exactly this text.
    assert encoded.decode("utf-8") == text, "UTF-8 round-trip failed"
    return encoded


def main() -> None:
    os.umask(0o022)
    data = validate_gate(ENTRY_TEXT)
    with open(OUTPUT_PATH, "wb") as fh:
        written = fh.write(data)
        assert written == len(data), f"short write: {written} of {len(data)} bytes"
        fh.flush()
        os.fsync(fh.fileno())
    # Read back what actually landed on disk: a short or partial write
    # must fail loudly here instead of silently grading as a bad entry.
    with open(OUTPUT_PATH, "rb") as fh:
        on_disk = fh.read()
    assert on_disk == data, "bytes on disk differ from the intended entry"
    os.chmod(OUTPUT_PATH, 0o644)
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"expected mode 0644, got {oct(mode)}"
    print(f"wrote {len(data)} bytes ({len(ENTRY_TEXT)} chars) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
