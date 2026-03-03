# 01Edu Audit Scripts

This repo is a collection of scripts for the purpose of automating the process for running the audit checkpoints, at list the programmatic ones

## How to use it

Let's say you're an auditor for `go-reloaded`, you can copy the script in [go-reloaded.py](./go-reloaded.py) to the directory of the code you want to audit and run:

`python go-reloaded.py`

OR

`python3 go-reload.py`

You'd get a result looking like this:

```txt
PASS Test 1 - low/cap/up modifiers
PASS Test 2 - bin/hex number conversion
PASS Test 3 - punctuation spacing
PASS Test 4 - cap with count + a/an correction + punctuation

4/4 tests passed
```

## _Disclaimer_

Please read the scripts before running it. We try as much as possible to open and we have a number of maintainers reviewing the scripts and ensuring it's simple and effective.
