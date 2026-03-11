#!/usr/bin/env python3
"""
Audit script for ascii-art --output flag project.
Runs each test case, shows the command, and displays the file output via cat -e.
"""

import subprocess
import os

SEPARATOR = "-" * 60


def run_cmd(cmd):
    """Run a shell command and return stdout + stderr."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr


def show(test_num, description, cmd, output_file=None):
    """
    Print test header, run command, then show file content with cat -e
    if an output_file is given, otherwise show stdout directly.
    """
    print(SEPARATOR)
    print(f"Test {test_num} - {description}")
    print(f"$ {cmd}")
    print()

    stdout, stderr = run_cmd(cmd)

    if stderr:
        print(f"[stderr]: {stderr.strip()}")

    if output_file:
        if os.path.exists(output_file):
            cat_out, _ = run_cmd(f"cat -e {output_file}")
            print(f"$ cat -e {output_file}")
            print(cat_out)
        else:
            print(f"[ERROR] Output file '{output_file}' was NOT created.\n")
    else:
        # No output file — just print stdout (e.g. usage error tests)
        if stdout:
            print(stdout)
        elif not stderr:
            print("[No output]")

    print()


# ── Cleanup any leftover test files from previous runs ────────────
for f in ["test00.txt", "test01.txt", "test02.txt", "test03.txt",
          "test04.txt", "test05.txt", "test06.txt", "test07.txt"]:
    if os.path.exists(f):
        os.remove(f)

print("=" * 60)
print("ASCII-ART --output FLAG AUDIT")
print("=" * 60)
print()

# ── Test 0 — wrong flag format: should print usage message ────────
show(
    0,
    'Wrong flag format (--output without =filename) → usage message',
    'go run . --output test00.txt banana standard',
)

# ── Test 1 — First\\nTest with shadow banner ───────────────────────
show(
    1,
    '"First\\\\nTest" shadow → test00.txt',
    'go run . --output=test00.txt "First\\nTest" shadow',
    output_file="test00.txt",
)

# ── Test 2 — hello standard ───────────────────────────────────────
show(
    2,
    '"hello" standard → test01.txt',
    'go run . --output=test01.txt "hello" standard',
    output_file="test01.txt",
)

# ── Test 3 — "123 -> #$%" standard ───────────────────────────────
show(
    3,
    '"123 -> #$%" standard → test02.txt',
    """go run . --output=test02.txt "123 -> #\$%" standard""",
    output_file="test02.txt",
)

# ── Test 4 — "432 -> #$%&@" shadow ───────────────────────────────
show(
    4,
    '"432 -> #$%&@" shadow → test03.txt',
    """go run . --output=test03.txt "432 -> #\$%&@" shadow""",
    output_file="test03.txt",
)

# ── Test 5 — "There" shadow ───────────────────────────────────────
show(
    5,
    '"There" shadow → test04.txt',
    'go run . --output=test04.txt "There" shadow',
    output_file="test04.txt",
)

# ── Test 6 — "123 -> \"#$%@" thinkertoy ──────────────────────────
show(
    6,
    '"123 -> \\"#$%@" thinkertoy → test05.txt',
    r"""go run . --output=test05.txt '123 -> "#$%@"' thinkertoy""",
    output_file="test05.txt",
)

# ── Test 7 — "2 you" thinkertoy ───────────────────────────────────
show(
    7,
    '"2 you" thinkertoy → test06.txt',
    'go run . --output=test06.txt "2 you" thinkertoy',
    output_file="test06.txt",
)

# ── Test 8 — "Testing long output!" standard ──────────────────────
show(
    8,
    '"Testing long output!" standard → test07.txt',
    "go run . --output=test07.txt 'Testing long output!' standard",
    output_file="test07.txt",
)

# ── Test 9 — random mixed upper/lower case ────────────────────────
show(
    9,
    'Random upper/lower case → random_mixed.txt',
    'go run . --output=random_mixed.txt "HeLLo WoRLd" standard',
    output_file="random_mixed.txt",
)

# ── Test 10 — lower case + digits + spaces ────────────────────────
show(
    10,
    'Lower case + digits + spaces → random_digits.txt',
    'go run . --output=random_digits.txt "hello 42 world" standard',
    output_file="random_digits.txt",
)

# ── Test 11 — special characters ─────────────────────────────────
show(
    11,
    'Special characters → random_special.txt',
    r"""go run . --output=random_special.txt "{Hello & There #}" standard""",
    output_file="random_special.txt",
)

# ── Test 12 — lower, upper, spaces, numbers ───────────────────────
show(
    12,
    'Lower + upper + spaces + numbers → random_all.txt',
    'go run . --output=random_all.txt "Hello World 123" standard',
    output_file="random_all.txt",
)

# ── Test 13 — no flag, plain string (should still work) ───────────
show(
    13,
    'No flag — plain string "hello" still works',
    'go run . "hello" | cat -e',
)

# ── Check all files exist ─────────────────────────────────────────
print(SEPARATOR)
print("File existence check:")
files = [
    "test00.txt", "test01.txt", "test02.txt", "test03.txt",
    "test04.txt", "test05.txt", "test06.txt", "test07.txt",
    "random_mixed.txt", "random_digits.txt", "random_special.txt", "random_all.txt",
]
all_present = True
for f in files:
    exists = os.path.exists(f)
    status = "✓ EXISTS" if exists else "✗ MISSING"
    print(f"  {status}  {f}")
    if not exists:
        all_present = False

print()
if all_present:
    print("✓ All output files were created successfully.")
else:
    print("✗ Some output files are missing — check the tests above.")
print(SEPARATOR)