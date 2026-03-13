#!/usr/bin/env python3
"""
Audit script for ascii-art-fs.
Asserts correct output for [STRING] [BANNER] usage.
"""

import subprocess

passed = 0
failed = 0


def run(args):
    result = subprocess.run(
        ["bash", "-c", f"go run . {args} | cat -e"],
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr


def check(test_num, description, args, expected):
    global passed, failed

    actual, stderr = run(args)
    actual = actual.rstrip("\n")
    expected = expected.rstrip("\n")

    if actual == expected:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        print(f"  Expected:\n{expected}")
        print(f"  Got:\n{actual}")
        if stderr.strip():
            print(f"  Stderr: {stderr.strip()}")
        failed += 1


def check_usage(test_num, description, args):
    """Assert that invalid usage prints the correct usage message."""
    global passed, failed

    result = subprocess.run(
        ["bash", "-c", f"go run . {args}"],
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    expected_usage = "Usage: go run . [STRING] [BANNER]"

    if expected_usage in output:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        print(f'  Expected output to contain: "{expected_usage}"')
        print(f"  Got: {output!r}")
        failed += 1


# ── Usage / error cases ───────────────────────────────────────────────

check_usage(1, "No arguments → usage message", "")

check_usage(2, "Too many arguments (4 args) → usage message", '"hello" standard extra arg')

check_usage(3, 'Unknown banner name → usage message', '"hello" unknownbanner')

# ── Single STRING argument (no banner → defaults to standard) ─────────

check(4, '"hello" single arg defaults to standard',
    '"hello"',
    " _              _   _          $\n"
    "| |            | | | |         $\n"
    "| |__     ___  | | | |   ___   $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\  $\n"
    "| | | | |  __/ | | | | | (_) | $\n"
    "|_| |_|  \\___| |_| |_|  \\___/  $\n"
    "                               $\n"
    "                               $",
)

# ── Standard banner ───────────────────────────────────────────────────

check(5, '"hello" standard',
    '"hello" standard',
    " _              _   _          $\n"
    "| |            | | | |         $\n"
    "| |__     ___  | | | |   ___   $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\  $\n"
    "| | | | |  __/ | | | | | (_) | $\n"
    "|_| |_|  \\___| |_| |_|  \\___/  $\n"
    "                               $\n"
    "                               $",
)

check(6, '"HELLO" standard',
    '"HELLO" standard',
    " _    _   ______   _        _         ____   $\n"
    "| |  | | |  ____| | |      | |       / __ \\  $\n"
    "| |__| | | |__    | |      | |      | |  | | $\n"
    "|  __  | |  __|   | |      | |      | |  | | $\n"
    "| |  | | | |____  | |____  | |____  | |__| | $\n"
    "|_|  |_| |______| |______| |______|  \\____/  $\n"
    "                                             $\n"
    "                                             $",
)

check(7, '"Hello There!" standard',
    '"Hello There!" standard',
    " _    _          _   _                 _______   _                           _  $\n"
    "| |  | |        | | | |               |__   __| | |                         | | $\n"
    "| |__| |   ___  | | | |   ___            | |    | |__     ___   _ __    ___  | | $\n"
    "|  __  |  / _ \\ | | | |  / _ \\           | |    |  _ \\   / _ \\ | '__|  / _ \\ | | $\n"
    "| |  | | |  __/ | | | | | (_) |          | |    | | | | |  __/ | |    |  __/ |_| $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/           |_|    |_| |_|  \\___| |_|     \\___| (_) $\n"
    "                                                                                  $\n"
    "                                                                                  $",
)

check(8, '"Hello\\nThere!" standard — newline splits into two banners',
    '"Hello\\nThere!" standard',
    " _    _          _   _          $\n"
    "| |  | |        | | | |         $\n"
    "| |__| |   ___  | | | |   ___   $\n"
    "|  __  |  / _ \\ | | | |  / _ \\  $\n"
    "| |  | | |  __/ | | | | | (_) | $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/  $\n"
    "                                $\n"
    "                                $\n"
    " _______   _                           _  $\n"
    "|__   __| | |                         | | $\n"
    "   | |    | |__     ___   _ __    ___  | | $\n"
    "   | |    |  _ \\   / _ \\ | '__|  / _ \\ | | $\n"
    "   | |    | | | | |  __/ | |    |  __/ |_| $\n"
    "   |_|    |_| |_|  \\___| |_|     \\___| (_) $\n"
    "                                           $\n"
    "                                           $",
)

check(9, '"Hello\\n\\nThere!" standard — double newline produces empty line',
    '"Hello\\n\\nThere!" standard',
    " _    _          _   _          $\n"
    "| |  | |        | | | |         $\n"
    "| |__| |   ___  | | | |   ___   $\n"
    "|  __  |  / _ \\ | | | |  / _ \\  $\n"
    "| |  | | |  __/ | | | | | (_) | $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/  $\n"
    "                                $\n"
    "                                $\n"
    "$\n"
    " _______   _                           _  $\n"
    "|__   __| | |                         | | $\n"
    "   | |    | |__     ___   _ __    ___  | | $\n"
    "   | |    |  _ \\   / _ \\ | '__|  / _ \\ | | $\n"
    "   | |    | | | | |  __/ | |    |  __/ |_| $\n"
    "   |_|    |_| |_|  \\___| |_|     \\___| (_) $\n"
    "                                           $\n"
    "                                           $",
)

check(10, 'Empty string "" standard — prints empty output',
    '"" standard',
    "$",
)

# ── Shadow banner ─────────────────────────────────────────────────────

check(11, '"hello" shadow',
    '"hello" shadow',
    "                                 $\n"
    "_|    _|   _|_|   _| _| _|_|_|  $\n"
    "_|    _| _|_|_|_| _| _| _|    _| $\n"
    "_|    _| _|       _| _| _|    _| $\n"
    "  _|_|_|   _|_|_| _| _| _|_|_|  $\n"
    "                                 $\n"
    "                                 $",
)

check(12, '"Hello There!" shadow',
    '"Hello There!" shadow',
    "                                                                                         $\n"
    "_|    _|          _| _|                _|_|_|_|_| _|                                  _| $\n"
    "_|    _|   _|_|   _| _|   _|_|             _|     _|_|_|     _|_|   _|  _|_|   _|_|   _| $\n"
    "_|_|_|_| _|_|_|_| _| _| _|    _|           _|     _|    _| _|_|_|_| _|_|     _|_|_|_| _| $\n"
    "_|    _| _|       _| _| _|    _|           _|     _|    _| _|       _|       _|          $\n"
    "_|    _|   _|_|_| _| _|   _|_|             _|     _|    _|   _|_|_| _|         _|_|_| _| $\n"
    "                                                                                         $\n"
    "                                                                                         $",
)

check(13, '"Hello\\nThere!" shadow — newline splits into two banners',
    '"Hello\\nThere!" shadow',
    "                           $\n"
    "_|    _|          _| _|   $\n"
    "_|    _|   _|_|   _| _|   $\n"
    "_|_|_|_| _|_|_|_| _| _|   $\n"
    "_|    _| _|       _| _|   $\n"
    "_|    _|   _|_|_| _| _|   $\n"
    "                           $\n"
    "                           $\n"
    "                                                  _| $\n"
    "_|_|_|_|_| _|                                  _|   $\n"
    "    _|     _|_|_|     _|_|   _|  _|_|   _|_|   _|   $\n"
    "    _|     _|    _| _|_|_|_| _|_|     _|_|_|_| _|   $\n"
    "    _|     _|    _| _|       _|       _|          $\n"
    "    _|     _|    _|   _|_|_| _|         _|_|_| _|   $\n"
    "                                                  _| $\n"
    "                                                  _| $",
)

# ── Thinkertoy banner ─────────────────────────────────────────────────

check(14, '"hello" thinkertoy',
    '"hello" thinkertoy',
    "                           $\n"
    "o  o     o o   o           $\n"
    "|  |     | |   |           $\n"
    "o--o o-o | | o-o           $\n"
    "|  | |-' | | | |           $\n"
    "o  o o-o o o o-o           $\n"
    "                           $\n"
    "                           $",
)

check(15, '"Hello There!" thinkertoy',
    '"Hello There!" thinkertoy',
    "                                                $\n"
    "o  o     o o           o-O-o o                o $\n"
    "|  |     | |             |   |                | $\n"
    "O--O o-o | | o-o         |   O--o o-o o-o o-o o $\n"
    "|  | |-' | | | |         |   |  | |-' |   |-'   $\n"
    "o  o o-o o o o-o         o   o  o o-o o   o-o O $\n"
    "                                                $\n"
    "                                                $",
)

check(16, '"Hello\\nThere!" thinkertoy — newline splits into two banners',
    '"Hello\\nThere!" thinkertoy',
    "                $\n"
    "o  o     o o   $\n"
    "|  |     | |   $\n"
    "O--O o-o | | o-o $\n"
    "|  | |-' | | | | $\n"
    "o  o o-o o o o-o $\n"
    "                $\n"
    "                $\n"
    "                                      $\n"
    "o-O-o o                o             $\n"
    "  |   |                |             $\n"
    "  |   O--o o-o o-o o-o o             $\n"
    "  |   |  | |-' |   |-'               $\n"
    "  o   o  o o-o o   o-o O             $\n"
    "                                      $\n"
    "                                      $",
)

check(17, '"2 you" thinkertoy',
    '"2 you" thinkertoy',
    "ooo                     $\n"
    "  |  o   o  o-o  o  o  $\n"
    " o   |   | | o   |  |  $\n"
    "|    o-o-o  o     oo   $\n"
    "ooo                    $\n"
    "                        $\n"
    "                        $",
)

#  Mixed / cross-banner sanity

check(18, '"123" standard — digits',
    '"123" standard',
    "     ____    _____   $\n"
    " _  |___ \\  |___ /   $\n"
    "/ |   __) |   |_ \\   $\n"
    "| |  |__ <    ___) |  $\n"
    "| |  ___) |  (___) |  $\n"
    "|_| |____/  |_____/   $\n"
    "                      $\n"
    "                      $",
)

check(19, '"RGB" standard',
    '"RGB" standard',
    " _____     _____   ____   $\n"
    "|  __ \\   / ____| |  _ \\  $\n"
    "| |__) | | |  __  | |_) | $\n"
    "|  _  /  | | |_ | |  _ <  $\n"
    "| | \\ \\  | |__| | | |_) | $\n"
    "|_|  \\_\\  \\_____| |____/  $\n"
    "                          $\n"
    "                          $",
)

check(20, '"MaD3IrA&LiSboN" standard',
    '"MaD3IrA&LiSboN" standard',
    " __  __           _____            _____                              _        _    _____   _               _   _  $\n"
    "|  \\/  |         |  __ \\   _____  |_   _|            /\\       ___    | |      (_)  / ____| | |             | \\ | | $\n"
    "| \\  / |   __ _  | |  | | |___ /    | |    _ __     /  \\     ( _ )   | |       _  | (___   | |__     ___   |  \\| | $\n"
    "| |\\/| |  / _` | | |  | |   |_ \\    | |   | '__|   / /\\ \\    / _ \\/\\ | |      | |  \\___ \\  | '_ \\   / _ \\  | . ` | $\n"
    "| |  | | | (_| | | |__| |  ___) |  _| |_  | |     / ____ \\  | (_>  < | |____  | |  ____) | | |_) | | (_) | | |\\  | $\n"
    "|_|  |_|  \\__,_| |_____/  |____/  |_____| |_|    /_/    \\_\\  \\___/\\/ |______| |_| |_____/  |_.__/   \\___/  |_| \\_| $\n"
    "                                                                                                                   $\n"
    "                                                                                                                   $",
)

# Summary
print()
print(f"{passed} passed, {failed} failed out of {passed + failed} tests.")