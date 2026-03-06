#!/usr/bin/env python3
import subprocess

passed = 0
failed = 0


def run(arg):
    result = subprocess.run(
        ["bash", "-c", f'go run . "{arg}"'],
        capture_output=True,
        text=True
    )
    return result.stdout


def check(test_num, description, arg, expected):
    global passed, failed

    actual = run(arg).rstrip("\n")
    expected = expected.rstrip("\n")

    if actual == expected:
        print(f"PASS Test {test_num} - {description}")
        passed += 1
    else:
        print(f"FAIL Test {test_num} - {description}")
        print(f"  Expected:\n{expected}")
        print(f"  Got:\n{actual}")
        failed += 1


# Test 1 - "hello"
check(1, '"hello" lowercase', "hello",
    " _              _   _          $\n"
    "| |            | | | |         $\n"
    "| |__     ___  | | | |   ___   $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\  $\n"
    "| | | | |  __/ | | | | | (_) | $\n"
    "|_| |_|  \\___| |_| |_|  \\___/  $\n"
    "                               $\n"
    "                               $"
)

# Test 2 - "HELLO"
check(2, '"HELLO" uppercase', "HELLO",
    " _    _   ______   _        _         ____   $\n"
    "| |  | | |  ____| | |      | |       / __ \\  $\n"
    "| |__| | | |__    | |      | |      | |  | | $\n"
    "|  __  | |  __|   | |      | |      | |  | | $\n"
    "| |  | | | |____  | |____  | |____  | |__| | $\n"
    "|_|  |_| |______| |______| |______|  \\____/  $\n"
    "                                             $\n"
    "                                             $"
)

# Test 3 - "HeLlo HuMaN"
check(3, '"HeLlo HuMaN" mixed case with space', "HeLlo HuMaN",
    " _    _          _        _                 _    _           __  __           _   _  $\n"
    "| |  | |        | |      | |               | |  | |         |  \\/  |         | \\ | | $\n"
    "| |__| |   ___  | |      | |   ___         | |__| |  _   _  | \\  / |   __ _  |  \\| | $\n"
    "|  __  |  / _ \\ | |      | |  / _ \\        |  __  | | | | | | |\\/| |  / _` | | . ` | $\n"
    "| |  | | |  __/ | |____  | | | (_) |       | |  | | | |_| | | |  | | | (_| | | |\\  | $\n"
    "|_|  |_|  \\___| |______| |_|  \\___/        |_|  |_|  \\__,_| |_|  |_|  \\__,_| |_| \\_| $\n"
    "                                                                                     $\n"
    "                                                                                     $"
)

# Test 4 - "1Hello 2There"
check(4, '"1Hello 2There" digits mixed with letters', "1Hello 2There",
    "     _    _          _   _                         _______   _                           $\n"
    " _  | |  | |        | | | |                ____   |__   __| | |                          $\n"
    "/ | | |__| |   ___  | | | |   ___         |___ \\     | |    | |__     ___   _ __    ___  $\n"
    "| | |  __  |  / _ \\ | | | |  / _ \\          __) |    | |    |  _ \\   / _ \\ | '__|  / _ \\ $\n"
    "| | | |  | | |  __/ | | | | | (_) |        / __/     | |    | | | | |  __/ | |    |  __/ $\n"
    "|_| |_|  |_|  \\___| |_| |_|  \\___/        |_____|    |_|    |_| |_|  \\___| |_|     \\___| $\n"
    "                                                                                         $\n"
    "                                                                                         $"
)

# Test 5 - "Hello\nThere" (newline in argument)
check(5, '"Hello\\nThere" newline separator', "Hello\\nThere",
    " _    _          _   _          $\n"
    "| |  | |        | | | |         $\n"
    "| |__| |   ___  | | | |   ___   $\n"
    "|  __  |  / _ \\ | | | |  / _ \\  $\n"
    "| |  | | |  __/ | | | | | (_) | $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/  $\n"
    "                                $\n"
    "                                $\n"
    " _______   _                           $\n"
    "|__   __| | |                          $\n"
    "   | |    | |__     ___   _ __    ___  $\n"
    "   | |    |  _ \\   / _ \\ | '__|  / _ \\ $\n"
    "   | |    | | | | |  __/ | |    |  __/ $\n"
    "   |_|    |_| |_|  \\___| |_|     \\___| $\n"
    "                                       $\n"
    "                                       $"
)

# Test 6 - "Hello\n\nThere" (double newline)
check(6, '"Hello\\n\\nThere" double newline (empty line between)', "Hello\\n\\nThere",
    " _    _          _   _          $\n"
    "| |  | |        | | | |         $\n"
    "| |__| |   ___  | | | |   ___   $\n"
    "|  __  |  / _ \\ | | | |  / _ \\  $\n"
    "| |  | | |  __/ | | | | | (_) | $\n"
    "|_|  |_|  \\___| |_| |_|  \\___/  $\n"
    "                                $\n"
    "                                $\n"
    "$\n"
    " _______   _                           $\n"
    "|__   __| | |                          $\n"
    "   | |    | |__     ___   _ __    ___  $\n"
    "   | |    |  _ \\   / _ \\ | '__|  / _ \\ $\n"
    "   | |    | | | | |  __/ | |    |  __/ $\n"
    "   |_|    |_| |_|  \\___| |_|     \\___| $\n"
    "                                       $\n"
    "                                       $"
)

# Test 7 - "{Hello & There #}"
check(7, '"{Hello & There #}" special characters', "{Hello & There #}",
    "   __  _    _          _   _                                _______   _                                    _  _    __    $\n"
    "  / / | |  | |        | | | |                 ___          |__   __| | |                                 _| || |_  \\ \\   $\n"
    " | |  | |__| |   ___  | | | |   ___          ( _ )            | |    | |__     ___   _ __    ___        |_  __  _|  | |  $\n"
    "/ /   |  __  |  / _ \\ | | | |  / _ \\         / _ \\/\\          | |    |  _ \\   / _ \\ | '__|  / _ \\        _| || |_    \\ \\ $\n"
    "\\ \\   | |  | | |  __/ | | | | | (_) |       | (_>  <          | |    | | | | |  __/ | |    |  __/       |_  __  _|   / / $\n"
    " | |  |_|  |_|  \\___| |_| |_|  \\___/         \\___/\\/          |_|    |_| |_|  \\___| |_|     \\___|         |_||_|    | |  $\n"
    "  \\_\\                                                                                                              /_/   $\n"
    "                                                                                                                         $"
)

# Test 8 - "hello There 1 to 2!"
check(8, '"hello There 1 to 2!" mixed', "hello There 1 to 2!",
    " _              _   _                 _______   _                                            _                           _  $\n"
    "| |            | | | |               |__   __| | |                                 _        | |                  ____   | | $\n"
    "| |__     ___  | | | |   ___            | |    | |__     ___   _ __    ___        / |       | |_    ___         |___ \\  | | $\n"
    "|  _ \\   / _ \\ | | | |  / _ \\           | |    |  _ \\   / _ \\ | '__|  / _ \\       | |       | __|  / _ \\          __) | | | $\n"
    "| | | | |  __/ | | | | | (_) |          | |    | | | | |  __/ | |    |  __/       | |       \\ |_  | (_) |        / __/  |_| $\n"
    "|_| |_|  \\___| |_| |_|  \\___/           |_|    |_| |_|  \\___| |_|     \\___|       |_|        \\__|  \\___/        |_____| (_) $\n"
    "                                                                                                                            $\n"
    "                                                                                                                            $"
)

# Test 9 - "MaD3IrA&LiSboN"
check(9, '"MaD3IrA&LiSboN"', "MaD3IrA&LiSboN",
    " __  __           _____            _____                              _        _    _____   _               _   _  $\n"
    "|  \\/  |         |  __ \\   _____  |_   _|            /\\       ___    | |      (_)  / ____| | |             | \\ | | $\n"
    "| \\  / |   __ _  | |  | | |___ /    | |    _ __     /  \\     ( _ )   | |       _  | (___   | |__     ___   |  \\| | $\n"
    "| |\\/| |  / _` | | |  | |   |_ \\    | |   | '__|   / /\\ \\    / _ \\/\\ | |      | |  \\___ \\  | '_ \\   / _ \\  | . ` | $\n"
    "| |  | | | (_| | | |__| |  ___) |  _| |_  | |     / ____ \\  | (_>  < | |____  | |  ____) | | |_) | | (_) | | |\\  | $\n"
    "|_|  |_|  \\__,_| |_____/  |____/  |_____| |_|    /_/    \\_\\  \\___/\\/ |______| |_| |_____/  |_.__/   \\___/  |_| \\_| $\n"
    "                                                                                                                   $\n"
    "                                                                                                                   $"
)

# Test 10 - "1a\"#FdwHywR&/()="
check(10, '"1a\"#FdwHywR&/()="', "1a\"#FdwHywR&/()=", "TODO")

# Test 11 - "{|}~"
check(11, '"{|}~"', "{|}~", "TODO")



# Test 13 - "RGB"
check(13, '"RGB"', "RGB", "TODO")

# Test 14 - ":;<=>?@"
check(14, '":;<=>?@"', ":;<=>?@", "TODO")

# Test 15 - '\!" #$%&'"'"'()*+,-./'
check(15, '\!" #$%&'"'"'()*+,-./', '\!" #$%&'"'"'()*+,-./', "TODO")

# Test 16 - "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
check(16, '"ABCDEFGHIJKLMNOPQRSTUVWXYZ" ', "ABCDEFGHIJKLMNOPQRSTUVWXYZ" , "TODO")

# Test 17 - "abcdefghijklmnopqrstuvwxyz"
check(17, '"abcdefghijklmnopqrstuvwxyz"', "abcdefghijklmnopqrstuvwxyz", "TODO")


# Test 18 - only standard packages check (informational)
def last_test():
    result = subprocess.run(["grep", "-r", "\"github.com", "."], capture_output=True, text=True)
    if result.stdout.strip() == "":
        print("PASS Test 18 - Only standard packages used")
        passed += 1
    else:
        print("FAIL Test 18 - Non-standard packages detected")
        print(f"  Found: {result.stdout.strip()}")
        failed += 1

    total = passed + failed
    print(f"\n{passed}/{total} tests passed")

    if failed > 0:
        exit(1)


last_test()