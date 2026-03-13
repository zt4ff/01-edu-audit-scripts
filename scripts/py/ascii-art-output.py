#!/usr/bin/env python3
"""
Audit script for ascii-art --output flag project.
Runs each test case, asserts expected behavior, and cleans up created files.
"""

import subprocess
import os

passed = 0
failed = 0
created_files = []


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr


def check_output_file(test_num, description, cmd, output_file, expected):
    global passed, failed
    created_files.append(output_file)

    run_cmd(cmd)

    if not os.path.exists(output_file):
        print(f"FAIL Test {test_num} - {description}")
        print(f"  Output file '{output_file}' was NOT created.")
        failed += 1
        return

    with open(output_file, "r") as f:
        actual = f.read()

    actual = actual.rstrip("\n")
    expected = expected.rstrip("\n")

    if actual == expected:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        print(f"  Expected:\n{expected}")
        print(f"  Got:\n{actual}")
        failed += 1


def check_no_file(test_num, description, cmd, unexpected_file):
    """Assert that a wrongly-formatted flag does NOT create a file and prints usage."""
    global passed, failed
    created_files.append(unexpected_file)

    stdout, stderr = run_cmd(cmd)

    file_created = os.path.exists(unexpected_file)
    has_output = bool(stdout.strip() or stderr.strip())

    if not file_created and has_output:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        if file_created:
            print(f"  File '{unexpected_file}' should NOT have been created.")
        if not has_output:
            print(f"  Expected a usage/error message on stdout or stderr, got none.")
        failed += 1


# ── Test 0 — wrong flag format: should print usage message, no file 
check_no_file(
    0,
    "Wrong flag format (--output without =filename) → usage message, no file",
    "go run . --output test00.txt banana standard",
    "test00.txt",
)

# ── Test 1 — "First\nTest" shadow 
check_output_file(
    1,
    '"First\\nTest" shadow → file matches expected',
    'go run . --output=test00.txt "First\\nTest" shadow',
    "test00.txt",
    " _____   _                 _    $\n"
    "|  ___| (_)  _ __   ___  | |_  $\n"
    "| |_    | | | '__| / __| | __| $\n"
    "|  _|   | | | |    \\__ \\ | |_  $\n"
    "|_|     |_| |_|    |___/  \\__| $\n"
    "                               $\n"
    "                               $\n"
    " _____                    _    $\n"
    "|_   _|  ___   ___  ___  | |_  $\n"
    "  | |   / _ \\ / __|/ __| | __| $\n"
    "  | |  |  __/ \\__ \\\\__ \\ | |_  $\n"
    "  |_|   \\___| |___/|___/  \\__| $\n"
    "                               $\n"
    "                               $",
)

# ── Test 2 — "hello" standard 
check_output_file(
    2,
    '"hello" standard → file matches expected',
    'go run . --output=test01.txt "hello" standard',
    "test01.txt",
    " _              _   _          $\n"
    "| |            | | | |         $\n"
    "| |__     ___  | | | |   ___   $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\  $\n"
    "| | | | |  __/ | | | | | (_) | $\n"
    "|_| |_|  \\___| |_| |_|  \\___/  $\n"
    "                               $\n"
    "                               $",
)

# ── Test 3 — "123 -> #$%" standard 
check_output_file(
    3,
    '"123 -> #$%" standard → file matches expected',
    r"""go run . --output=test02.txt "123 -> #\$%" standard""",
    "test02.txt",
    "     ____    _____    ____        __                  _   _       _  __    $\n"
    " _  |___ \\  |___ /   |___ \\      / /    ___    _    | | | |     | | \\ \\   $\n"
    "/ |   __) |   |_ \\     __) |    / /    ( _ )  (_)   | | | |     | |  \\ \\  $\n"
    "| |  |__ <    ___) |  |__ <     \\ \\   / _ \\/\\       |_| |_|     | |   > > $\n"
    "| |  ___) |  (___) |  (___) |    \\ \\ | (_>  <    _   _   _      | |  / /  $\n"
    "|_| |____/  |_____/  |_____/      \\_\\ \\___/\\/   (_) (_) (_)     |_| /_/   $\n"
    "                                                                           $\n"
    "                                                                           $",
)

# ── Test 4 — "432 -> #$%&@" shadow 
check_output_file(
    4,
    '"432 -> #$%&@" shadow → file matches expected',
    r"""go run . --output=test03.txt "432 -> #\$%&@" shadow""",
    "test03.txt",
    "  _  _       _____    ____        __                  _   _       _  __                    ____   $\n"
    " | || |     |___ /   |___ \\      / /    ___    _    | | | |     | | \\ \\      /\\       _  |___ \\  $\n"
    " | || |_      |_ \\     __) |    / /    ( _ )  (_)   | | | |     | |  \\ \\    /  \\     ( )   ) )  $\n"
    " |__   _|    ___) |  |__ <      \\ \\   / _ \\/\\       |_| |_|     | |   > >  / /\\ \\    |/   / /   $\n"
    "    | |     (___) |  (___) |     \\ \\ | (_>  <    _   _   _      | |  / /  / ____ \\       / /    $\n"
    "    |_|    |_____/  |_____/       \\_\\ \\___/\\/   (_) (_) (_)     |_| /_/  /_/    \\_\\     /_/     $\n"
    "                                                                                                  $\n"
    "                                                                                                  $",
)

# ── Test 5 — "There" shadow 
check_output_file(
    5,
    '"There" shadow → file matches expected',
    'go run . --output=test04.txt "There" shadow',
    "test04.txt",
    " _____   _                           $\n"
    "|_   _| | |__     ___   _ __    ___  $\n"
    "  | |   | '_ \\   / _ \\ | '__|  / _ \\ $\n"
    "  | |   | | | | |  __/ | |    |  __/ $\n"
    "  |_|   |_| |_|  \\___| |_|     \\___| $\n"
    "                                     $\n"
    "                                     $",
)

# ── Test 6 — '123 -> "#$%@"' thinkertoy 
check_output_file(
    6,
    '"123 -> \\"#$%@\\" thinkertoy → file matches expected',
    r"""go run . --output=test05.txt '123 -> "#$%@"' thinkertoy""",
    "test05.txt",
    "                o   o          o                 o  o       \"   \"       $\n"
    "  o  oo   ooo  |   |          |                 |  |       |   |       $\n"
    " /  o  o  \\ \\  O   O   o-o   -o-  o-o          O--O      -o- -o-      $\n"
    "o   |  |   > | |   |          |                 |  |       |   |       $\n"
    " \\  o  o  o-o o o  o          o                 o  o       o   o       $\n"
    "                                                                        $\n"
    "                                                                        $",
)

# ── Test 7 — "2 you" thinkertoy 
check_output_file(
    7,
    '"2 you" thinkertoy → file matches expected',
    'go run . --output=test06.txt "2 you" thinkertoy',
    "test06.txt",
    "ooo                     $\n"
    "  |  o   o  o-o  o  o  $\n"
    " o   |   | | o   |  |  $\n"
    "|    o-o-o  o     oo   $\n"
    "ooo                    $\n"
    "                        $\n"
    "                        $",
)

# ── Test 8 — "Testing long output!" standard 
check_output_file(
    8,
    '"Testing long output!" standard → file matches expected',
    "go run . --output=test07.txt 'Testing long output!' standard",
    "test07.txt",
    " _______                        _     _                    _                                                    _                   _   _ $\n"
    "|__   __|                      | |   (_)                  | |                                                  | |                 | | | |$\n"
    "   | |     ___   ___   ______  | |_   _   _ __     __ _   | |   ___    _ __     __ _     ___    _   _   ______  | |_    _ __    _   | | | |$\n"
    "   | |    / _ \\ / __| |______| | __| | | | '_ \\   / _` |  | |  / _ \\  | '_ \\   / _` |   / _ \\  | | | | |______| | __|  | '_ \\  | | | | | |$\n"
    "   | |   |  __/ \\__ \\          \\ |_  | | | | | | | (_| |  | | | (_) | | | | | | (_| |  | (_) | | |_| |          \\ |_   | |_) | | |_| | |_|$\n"
    "   |_|    \\___| |___/           \\__| |_| |_| |_|  \\__, |  |_|  \\___/  |_| |_|  \\__, |   \\___/   \\__,_|           \\__|  | .__/   \\___/  (_)$\n"
    "                                                    __/ |                         __/ |                                  | |               $\n"
    "                                                   |___/                         |___/                                   |_|               $",
)

# ── Test 9 — "HeLLo WoRLd" standard 
check_output_file(
    9,
    '"HeLLo WoRLd" random upper/lower → file matches expected',
    'go run . --output=random_mixed.txt "HeLLo WoRLd" standard',
    "random_mixed.txt",
    " _    _          _        _                  _   _   _          ____    _       _  $\n"
    "| |  | |        | |      | |                | | | | | |        |  _ \\  | |     | | $\n"
    "| |__| |   ___  | |      | |   ___          | | | | | |   ___  | |_) | | |     | | $\n"
    "|  __  |  / _ \\ | |      | |  / _ \\         | | | | | |  / _ \\ |  _ <  | |     | | $\n"
    "| |  | | |  __/ | |____  | | | (_) |        \\ \\_/ / | | | (_) || |_) | | |____ | | $\n"
    "|_|  |_|  \\___| |______| |_|  \\___/          \\___/  |_|  \\___/ |____/  |______||_| $\n"
    "                                                                                    $\n"
    "                                                                                    $",
)

# ── Test 10 — "hello 42 world" standard 
check_output_file(
    10,
    '"hello 42 world" lower + digits + spaces → file matches expected',
    'go run . --output=random_digits.txt "hello 42 world" standard',
    "random_digits.txt",
    " _              _   _                   _  _____   __                          _       _  $\n"
    "| |            | | | |                 | ||  __ \\ / /  __      __   ___   _ __| |     | | $\n"
    "| |__     ___  | | | |   ___           | || |  | | /   \\ \\ /\\ / /  / _ \\ | '__| |     | | $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\     _   | || |  | |\\ \\    \\ V  V /  | | | || |  | |     | | $\n"
    "| | | | |  __/ | | | | | (_) |   | |__| || |__| | \\ \\    \\  /\\  / | |_| || |  | |____ |_| $\n"
    "|_| |_|  \\___| |_| |_|  \\___/     \\____/ |_____/   \\_\\    \\/  \\/   \\___/ |_|  |______|(_) $\n"
    "                                                                                            $\n"
    "                                                                                            $",
)

# ── Test 11 — "{Hello & There #}" standard 
check_output_file(
    11,
    '"{Hello & There #}" special characters → file matches expected',
    r"""go run . --output=random_special.txt "{Hello & There #}" standard""",
    "random_special.txt",
    "   __  _    _          _   _                                _______   _                                    _  _    __    $\n"
    "  / / | |  | |        | | | |                 ___          |__   __| | |                                 _| || |_  \\ \\   $\n"
    " | |  | |__| |   ___  | | | |   ___          ( _ )            | |    | |__     ___   _ __    ___        |_  __  _|  | |  $\n"
    "/ /   |  __  |  / _ \\ | | | |  / _ \\         / _ \\/\\          | |    |  _ \\   / _ \\ | '__|  / _ \\        _| || |_    \\ \\ $\n"
    "\\ \\   | |  | | |  __/ | | | | | (_) |       | (_>  <          | |    | | | | |  __/ | |    |  __/       |_  __  _|   / / $\n"
    " | |  |_|  |_|  \\___| |_| |_|  \\___/         \\___/\\/          |_|    |_| |_|  \\___| |_|     \\___|         |_||_|    | |  $\n"
    "  \\_\\                                                                                                              /_/   $\n"
    "                                                                                                                         $",
)

# ── Test 12 — "Hello World 123" standard 
check_output_file(
    12,
    '"Hello World 123" lower + upper + spaces + numbers → file matches expected',
    'go run . --output=random_all.txt "Hello World 123" standard',
    "random_all.txt",
    " _    _          _   _                  _   _   _          ____    _       _        _            ____    _____   $\n"
    "| |  | |        | | | |                | | | | | |        |  _ \\  | |     | |      | |          |___ \\  |___ /   $\n"
    "| |__| |   ___  | | | |   ___          | | | | | |   ___  | |_) | | |     | |      | |            __) |   |_ \\   $\n"
    "|  __  |  / _ \\ | | | |  / _ \\         | | | | | |  / _ \\ |  _ <  | |     | |      | |           |__ <    ___) |  $\n"
    "| |  | | |  __/ | | | | | (_) |        \\ \\_/ / | | | (_) || |_) | | |____ | |____  | |____       (___) |  (___) |  $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/          \\___/  |_|  \\___/ |____/  |______||______| |______|     |____/  |_____/   $\n"
    "                                                                                                                    $\n"
    "                                                                                                                    $",
)

# ── Test 13 — no flag (plain stdout) 
def check_stdout(test_num, description, cmd, expected):
    global passed, failed
    stdout, _ = run_cmd(cmd)
    actual = stdout.rstrip("\n")
    expected = expected.rstrip("\n")
    if actual == expected:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        print(f"  Expected:\n{expected}")
        print(f"  Got:\n{actual}")
        failed += 1

check_stdout(
    13,
    'No flag — "hello" still prints to stdout',
    'go run . "hello" | cat -e',
    " _              _   _          $\n"
    "| |            | | | |         $\n"
    "| |__     ___  | | | |   ___   $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\  $\n"
    "| | | | |  __/ | | | | | (_) | $\n"
    "|_| |_|  \\___| |_| |_|  \\___/  $\n"
    "                               $\n"
    "                               $",
)

# ── Summary ─
print()
print(f"{passed} passed, {failed} failed out of {passed + failed} tests.")

# ── Cleanup ─
for f in created_files:
    if os.path.exists(f):
        os.remove(f)