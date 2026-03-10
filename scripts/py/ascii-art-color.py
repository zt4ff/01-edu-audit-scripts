#!/usr/bin/env python3
import subprocess

# ************************************************#
# This script doesn't perform any "checks"        #
# It only prints the ascii art so you can         #
# manually view it                                #
# ************************************************#

def run(args):
    result = subprocess.run(
        ["bash", "-c", f"go run . {args}"],
        capture_output=True,
        text=True
    )
    return result.stdout

def show(test_num, args):
    print(f"Test {test_num}")
    print(f"go run . {args}")
    print(run(args))

# Test 1 - color a repeated substring
show(1, '--color=red car "car and car"')

# Test 2 - color substring within a word
show(2, '--color=red kit "a king kitten have kit"')

# Test 3 - whole string colored (no substring)
show(3, '--color=blue "Hello"')

# Test 4 - color only part of a word
show(4, '--color=green He "Hello"')

# Test 5 - yellow on mixed case
show(5, '--color=yellow ello "Hello World"')

# Test 6 - cyan on a longer string
show(6, '--color=cyan There "Hello There"')

# Test 7 - substring not present (no color expected)
show(7, '--color=red xyz "Hello"')

# Test 8 - invalid flag format (usage message expected)
show(8, '-color=red kit "a king kitten have kit"')
